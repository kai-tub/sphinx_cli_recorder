from __future__ import annotations


__version__ = "0.1.0"
import itertools

from enum import Enum, auto
import asyncer
from docutils import nodes

from docutils.parsers.rst import directives
from pydantic import BaseModel
from sphinx.util.docutils import SphinxDirective
from typing import List, Dict, Any, Optional, Union
from sphinx.application import Sphinx
from sphinx.writers.html5 import HTML5Translator
from icecream import ic
import tempfile
from sphinx.util.fileutil import copy_asset
from pathlib import Path
from sphinx.application import Sphinx
import importlib
from docutils.transforms import Transform

from sphinx.util import logging
import sphinx_auto_asciinema
from functools import partial

from sphinx_auto_asciinema.scripted_asciicast_runner import (
    scripted_asciicasts_runner,
)
from sphinx.util.nodes import NodeMatcher
from sphinx_auto_asciinema.asciinema_block_parser import (
    scripted_cmd_interaction_parser,
    timed_cmd_interaction_parser,
)
from sphinx_auto_asciinema.asciinema_player_settings import (
    AsciinemaPlayerSettings,
    AsciinemaRecorderSettings,
)

from sphinx_auto_asciinema.scripted_cmds import SleepTimes

logger = logging.getLogger(__name__)

JS_RESOURCE = "asciinema-player.min.js"
CSS_RESOURCE = "asciinema-player.css"


class InteractionMode(Enum):
    DirectExecution = auto()
    Scripted = auto()
    Timed = auto()


class SphinxAutoAsciinemaSettingNames(BaseModel):
    player_settings = "sphinx_auto_asciinema_player_settings"
    sleep_times_settings = "sphinx_auto_asciinema_sleep_times_settings"
    cmd_runner_settings = "sphinx_auto_asciinema_cmd_runner_settings"


# TODO: Always purge directory; should be configurable if desired to only update if document has changed
# No purge necessary, because I do not have a global cache... I think
# I think the recs should be cleared every-time, except for when the
# configuration says that it is not necessary


def copy_resources(app: Sphinx, exception, resources: Optional[List[str]] = None):
    """
    Copy the local `resources` from the Python package to the
    Sphinx output directory `_static`.
    Note that these `resources` must be in the top-level of the package
    next to `__init__.py`.
    Should be wrapped with `partial` before connecting to `Sphinx` event.

    Args:
        app (Sphinx): Sphinx application
        exception: Do no run if exception is processed.
        resources (Optional[List[str]], optional): Optional list of resource names.
        If none are given, will return. Defaults to None.

    Raises:
        ValueError: If an unknown resource is given raise a `ValueError`.
    """
    if resources is None:
        return

    for resource in resources:
        if not importlib.resources.is_resource(sphinx_auto_asciinema, resource):
            raise ValueError(f"{JS_RESOURCE} is an unknown resource!")
        with importlib.resources.path(sphinx_auto_asciinema, resource) as resource_path:
            outdir = Path(app.outdir) / "_static"
            if exception is None:
                copy_asset(str(resource_path), str(outdir))


class CommandRunner(Transform):
    default_priority = 600

    @property
    def app(self) -> Sphinx:
        return self.env.app

    @property
    def env(self):
        return self.document.settings.env

    # Will be called for every document
    # Which makes it extremely inefficient...
    # This should not be a transform
    def apply(self, **_kwargs):
        ic()
        matcher = NodeMatcher(asciinema)
        outdir = Path(self.app.outdir) / "_recs"
        # FUTURE: Allow to skip files if they already exist
        # would require the setting an :cache: option to the directive
        # which would require me to create a unique-hash for the command
        # input, because it must be re-run if any other options changes
        outdir.mkdir(exist_ok=True)
        for old_rec in outdir.glob("*.rec"):
            if old_rec.is_file():
                old_rec.unlink()

        with tempfile.TemporaryDirectory(prefix="sphinx-asciinema") as tmpdirname:
            tmpdir_p = Path(tmpdirname)
            matching_nodes = [node for node in self.document.traverse(matcher)]
            commands = [node["command"] for node in matching_nodes]
            output_fps = [tmpdir_p / str(node["fname"]) for node in matching_nodes]
            expect_groups = [node["expects"] for node in matching_nodes]
            send_groups = [node["sends"] for node in matching_nodes]
            sleep_times_groups = [node["sleep_times"] for node in matching_nodes]
            recorder_settings_list = [
                node["recorder_settings"] for node in matching_nodes
            ]

            asyncer.syncify(scripted_asciicasts_runner, raise_sync_error=False)(
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
    template = "<script>\nAsciinemaPlayer.create('/_recs/{fname}', document.getElementById('{id}'), {options});\n</script>"
    tag = template.format(id=node["id"], fname=node["fname"], options=js_player_options)
    self.body.append(tag)


def depart_asciinema_node(self: HTML5Translator, node: nodes.Element):
    pass


class AsciinemaBaseDirective(SphinxDirective):
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
            raise NotImplementedError("Do not call AsciinemaBaseDirective directly!")
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
        # self.options may contain more keys than only those of player_options
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
        # Future: Understand if/how to not repeat target_id and use it in two different parts
        # IndexDirective does it the same way
        target_node = nodes.target(rawsource="", text="", ids=[target_id])
        # if direct mode
        asciinema_node = asciinema(
            fname=f"{target_id}.rec",
            sends=sends,
            expects=expects,
            recorder_settings=validated_recorder_settings,
            data="\n".join(self.content),
            command=self.arguments[0],
            player_options=validated_player_options,
            sleep_times=validated_sleep_times,
            id=target_id,
        )
        return [target_node, asciinema_node]


class AsciinemaRunDirective(AsciinemaBaseDirective):
    interaction_mode: InteractionMode = InteractionMode.DirectExecution


class AsciinemaScriptedCmdInteractionDirective(AsciinemaBaseDirective):
    interaction_mode: InteractionMode = InteractionMode.Scripted


class AsciinemaTimedCmdInteractionDirective(AsciinemaBaseDirective):
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

    app.connect("build-finished", copy_local_resources)
    app.add_transform(CommandRunner)
    # FUTURE: Only add js/css resources if Directive in page is found
    app.add_css_file(CSS_RESOURCE)
    # FUTURE: maybe think about re-naming asciinema to "record" prefix
    # for the directives because the user doesn't "need" to know that it
    # is using asciinema in the background
    app.add_directive("asciinema_run_cmd", AsciinemaRunDirective)
    app.add_directive(
        "asciinema_scripted_cmd_interaction", AsciinemaScriptedCmdInteractionDirective
    )
    app.add_directive(
        "asciinema_timed_cmd_interaction", AsciinemaTimedCmdInteractionDirective
    )
    return {
        "version": __version__,
        # FUTURE: Make some tests
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
