from __future__ import annotations

import importlib.metadata

__version__ = importlib.metadata.version("sphinx_cli_recorder")

import importlib.resources
import itertools
import tempfile
import urllib.parse
from enum import Enum, auto
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import asyncer
from docutils import nodes
from docutils.parsers.rst import directives
from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.fileutil import copy_asset
from sphinx.writers.html5 import HTML5Translator

import sphinx_cli_recorder
from sphinx_cli_recorder.asciinema_block_parser import (
    scripted_cmd_interaction_parser,
    timed_cmd_interaction_parser,
)
from sphinx_cli_recorder.asciinema_player_settings import (
    AsciinemaPlayerSettings,
    AsciinemaRecorderSettings,
)
from sphinx_cli_recorder.scripted_asciinema_runner import scripted_asciinema_runners
from sphinx_cli_recorder.scripted_cmds import SleepTimes

logger = logging.getLogger(__name__)

JS_RESOURCE = "asciinema-player.min.js"
CSS_RESOURCE = "asciinema-player.css"


class SphinxCliRecorderEnvType(BuildEnvironment):
    """
    Sphinx build environment, including the attributes set by sphinx_cli_recorder.
    As the build environment is designed to be dynamically patched, there is no
    easy way to make the code mypy-ready.
    This solution makes mypy pass, but the environment always has to be checked
    if the attribute is available first!
    """

    sphinx_cli_recorder_commands: list


class InteractionMode(Enum):
    DirectExecution = auto()
    Scripted = auto()
    Timed = auto()


class SphinxAutoAsciinemaSettingNames(BaseModel):
    player_settings = "sphinx_cli_recorder_player_settings"
    sleep_times_settings = "sphinx_cli_recorder_sleep_times_settings"
    cmd_runner_settings = "sphinx_cli_recorder_cmd_runner_settings"


def purge_commands(app: Sphinx, env: SphinxCliRecorderEnvType, docname: str):
    if not hasattr(env, "sphinx_cli_recorder_commands"):
        return
    env.sphinx_cli_recorder_commands = [
        asciinema_command
        for asciinema_command in env.sphinx_cli_recorder_commands
        if asciinema_command["docname"] != docname
    ]


def copy_resources(app: Sphinx, exception, resources: Optional[List[str]] = None):
    """
    Copy the local `resources` from the Python package to the
    Sphinx output directory `_static`.
    Note that these `resources` must be in the top-level of the package
    next to `__init__.py`.
    Should be wrapped with `partial` before connecting to `Sphinx` event.

    Args:
        app (Sphinx): Sphinx application
        exception: Do not run if exception is processed.
        resources (Optional[List[str]], optional): Optional list of resource names.
        If none are given, will return. Defaults to None.

    Raises:
        ValueError: If an unknown resource is given raise a `ValueError`.
    """
    if resources is None:
        return

    for resource in resources:
        if not importlib.resources.is_resource(sphinx_cli_recorder, resource):
            raise ValueError(
                f"{JS_RESOURCE} is an unknown resource! Something went wrong in the packaging!"
            )
        with importlib.resources.path(sphinx_cli_recorder, resource) as resource_path:
            outdir = Path(app.outdir) / "_static"
            if exception is None:
                copy_asset(str(resource_path), str(outdir))


def run_cmds(app: Sphinx, env: SphinxCliRecorderEnvType):
    """
    Function that access the extension-cache from within `env`.
    The function will execute all commands in an asynchronous loop.

    Currently, this is also the spot where the directory is cleaned
    from all the previous output recordings.
    """
    outdir = Path(app.outdir) / "_recs"
    # FUTURE: Allow to skip files if they already exist
    # would require the setting an :cache: option to the directive
    # which would require me to create a unique-hash for the command
    # input, because it must be re-run if any other options changes
    # FUTURE: Delete files when name changed for example
    outdir.mkdir(exist_ok=True)
    for old_rec in outdir.glob("*.rec"):
        if old_rec.is_file():
            old_rec.unlink()
    if not hasattr(env, "sphinx_cli_recorder_commands"):
        return

    with tempfile.TemporaryDirectory(prefix="sphinx-asciinema") as tmpdirname:
        tmpdir_p = Path(tmpdirname)
        asciinema_nodes = [entry["node"] for entry in env.sphinx_cli_recorder_commands]
        commands = [node["command"] for node in asciinema_nodes]
        expect_groups = [node["expects"] for node in asciinema_nodes]
        output_fps = [tmpdir_p / node["fname"] for node in asciinema_nodes]
        send_groups = [node["sends"] for node in asciinema_nodes]
        sleep_times_groups = [node["sleep_times"] for node in asciinema_nodes]
        recorder_settings_list = [node["recorder_settings"] for node in asciinema_nodes]

        asyncer.syncify(scripted_asciinema_runners, raise_sync_error=False)(
            cmds=commands,
            expect_groups=expect_groups,
            send_groups=send_groups,
            output_fps=output_fps,
            sleep_times_groups=sleep_times_groups,
            recorder_settings_list=recorder_settings_list,
        )

        for output_fp in output_fps:
            copy_asset(str(output_fp), str(outdir))


class asciinema(nodes.container):
    pass


def visit_asciinema_node(self: HTML5Translator, node: nodes.Element):
    self.body.append(self.starttag(node, "div", CLASS="asciinema"))
    self.body.append("</div>\n")
    js_player_options = node["player_options"].json()
    # add_js_file always uses _static
    # https://github.com/sphinx-doc/sphinx/blob/f38bd8e9529d50e5cceffe3ca55be4b758529ff7/sphinx/builders/html/__init__.py#L332
    # FUTURE: Figure out how to lazy load the JS file at the end of body
    # But still only run the AsciinemaPlayer code once the script has been loaded
    js_script_loader = f"<script src=_static/{JS_RESOURCE}></script>"
    self.body.append(js_script_loader)
    template = "<script>\nAsciinemaPlayer.create('_recs/{fname}', document.getElementById('{id}'), {options});\n</script>"
    tag = template.format(id=node["id"], fname=node["fname"], options=js_player_options)
    self.body.append(tag)


def depart_asciinema_node(self: HTML5Translator, node: nodes.Element):
    pass


def merge_cmds(
    _app: Sphinx,
    env: SphinxCliRecorderEnvType,
    docnames: Set[str],
    other: SphinxCliRecorderEnvType,
):
    """
    Merge the extension-cache of sphinx_cli_recorder.
    This is only run when parallel-write is enabled.
    """
    if not hasattr(env, "sphinx_cli_recorder_commands"):
        env.sphinx_cli_recorder_commands = []
    if hasattr(other, "sphinx_cli_recorder_commands"):
        env.sphinx_cli_recorder_commands.extend(other.sphinx_cli_recorder_commands)


class RecordCliBaseDirective(SphinxDirective):
    has_content: bool = True
    # postpone validation; will use pydantic to validate
    # the option spec must still define all available options
    option_spec = {
        k: directives.unchanged
        for k in itertools.chain(
            AsciinemaPlayerSettings.__fields__,
            SleepTimes.__fields__,
            AsciinemaRecorderSettings.__fields__,
        )
    }  # options will be converted to lower!
    setting_names = SphinxAutoAsciinemaSettingNames()
    required_arguments: int = 1
    final_argument_whitespace: bool = True
    interaction_mode: InteractionMode | None = None

    # FUTURE: figure out how to cleanly refactor this
    # branchy code
    def run(self) -> List[nodes.Node]:
        if self.interaction_mode is None:
            raise NotImplementedError("Do not call RecordCliBaseDirective directly!")
        if self.interaction_mode == InteractionMode.DirectExecution:
            sends = None
            expects = None
        else:
            self.assert_has_content()
        content = "\n".join(self.content) if self.content else ""
        if self.interaction_mode == InteractionMode.Timed:
            send_strs = timed_cmd_interaction_parser(content)
            sends = [s.send for s in send_strs]
            expects = None
        if self.interaction_mode == InteractionMode.Scripted:
            wait_for_send_pairs = scripted_cmd_interaction_parser(content)
            sends = [p.send for p in wait_for_send_pairs]
            expects = [p.wait_for for p in wait_for_send_pairs]

        conf_player_options = self.env.config[self.setting_names.player_settings]
        local_player_options = {
            k: v
            for k, v in self.options.items()
            if k in AsciinemaPlayerSettings.__fields__
        }
        player_options = {**conf_player_options, **local_player_options}
        validated_player_options = AsciinemaPlayerSettings(**player_options)

        conf_sleep_times_options = self.env.config[
            self.setting_names.sleep_times_settings
        ]
        local_sleep_times_options = {
            k: v for k, v in self.options.items() if k in SleepTimes.__fields__
        }
        sleep_times = {**conf_sleep_times_options, **local_sleep_times_options}
        validated_sleep_times = SleepTimes(**sleep_times)

        recorder_settings = {
            k: v
            for k, v in self.options.items()
            if k in AsciinemaRecorderSettings.__fields__
        }
        validated_recorder_settings = AsciinemaRecorderSettings(**recorder_settings)

        id_ = self.state.document.settings.env.new_serialno("asciinema")
        target_id = f"asciinema-{id_}"
        # in HTML the target_id is the class id value!
        target_node = nodes.target(rawsource="", text="", ids=[target_id])

        # this _should_ be globally unique!
        fname = f"{self.env.docname}-{target_id}.rec"
        asciinema_node = asciinema(
            fname=urllib.parse.quote(fname, safe=""),
            sends=sends,
            expects=expects,
            recorder_settings=validated_recorder_settings,
            data="\n".join(self.content),
            command=self.arguments[0],
            player_options=validated_player_options,
            sleep_times=validated_sleep_times,
            id=target_id,
        )

        self.env: SphinxCliRecorderEnvType
        if not hasattr(self.env, "sphinx_cli_recorder_commands"):
            self.env.sphinx_cli_recorder_commands = []

        self.env.sphinx_cli_recorder_commands.append(
            {
                "node": asciinema_node.deepcopy(),
                "docname": self.env.docname,
            }
        )

        return [target_node, asciinema_node]


class RecordCliCmdDirective(RecordCliBaseDirective):
    interaction_mode: InteractionMode = InteractionMode.DirectExecution


class RecordScriptedCliInteractionDirective(RecordCliBaseDirective):
    interaction_mode: InteractionMode = InteractionMode.Scripted


class RecordTimedCliInteractionDirective(RecordCliBaseDirective):
    interaction_mode: InteractionMode = InteractionMode.Timed


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(
        asciinema,
        html=(visit_asciinema_node, depart_asciinema_node),
    )
    copy_local_resources = partial(
        copy_resources, resources=[JS_RESOURCE, CSS_RESOURCE]
    )
    player_settings = SphinxAutoAsciinemaSettingNames().player_settings
    sleep_times_settings = SphinxAutoAsciinemaSettingNames().sleep_times_settings
    app.add_config_value(player_settings, {}, rebuild="html")
    app.add_config_value(sleep_times_settings, {}, rebuild="html")

    # FUTURE: Better document this
    app.connect("build-finished", copy_local_resources)
    app.connect("env-updated", run_cmds)
    app.connect("env-merge-info", merge_cmds)
    app.connect("env-purge-doc", purge_commands)
    app.add_css_file(CSS_RESOURCE)
    app.add_directive("record_cli_cmd", RecordCliCmdDirective)
    app.add_directive(
        "record_scripted_cli_interaction", RecordScriptedCliInteractionDirective
    )
    app.add_directive(
        "record_timed_cli_interaction", RecordTimedCliInteractionDirective
    )
    return {
        "version": __version__,
        # FUTURE: Make some tests
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
