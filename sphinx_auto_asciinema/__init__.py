from __future__ import annotations


__version__ = "0.1.0"

from enum import Enum, auto
import json
import asyncer
from docutils import nodes

from docutils.parsers.rst import directives
from pydantic import BaseSettings, BaseModel, PositiveFloat, PositiveInt
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

# from asciinema.recorder import record
from sphinx_auto_asciinema.scripted_asciicast_runner import (
    scripted_asciicast_runner,
    scripted_asciicasts_runner,
)
from sphinx.util.nodes import NodeMatcher
from sphinx_auto_asciinema.asciinema_block_parser import (
    scripted_cmd_interaction_parser,
    timed_cmd_interaction_parser,
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
    cmd_runner_settings = "sphinx_auto_asciinema_cmd_runner_settings"


# does not include rows/cols:
# According to documentation this should be set to the values of
# of the file; in other words, these values should be overwritten
# from the recorder settings
# rows could be changed to fine-tune the output...
# The options will be converted to lower in the Directive options class
# To keep it consistent I will also use the same style.
# I don't know why, but the options javascript <script> tag from asciinema
# doesn't care if it is lower/upper case
class AsciinemaPlayerSettings(BaseModel):
    autoplay: bool = False
    rows: PositiveInt = 24
    cols: PositiveInt = 80
    preload: bool = False
    loop: bool = False
    # create correct validator
    startat: Union[str, int] = 0
    # could also be int
    speed: PositiveFloat = 1.0


# class ExpectSendsGroup(BaseModel):


# TODO: Always purge directory; should be configurable if desired to only update if document has changed
# TODO: Add options to player and recorder


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

    def apply(self, **kwargs):
        matcher = NodeMatcher(asciinema)
        # FUTURE: Execute the command asynchroneously or in parallel
        outdir = Path(self.app.outdir) / "_recs"
        outdir.mkdir(exist_ok=True)
        # parse the nodes to a list that can be passed to scripted asciicast runner
        commands = []
        output_fps = []
        expect_groups = []
        send_groups = []
        # Could run multiple node matches before calling async code
        #
        with tempfile.TemporaryDirectory(prefix="sphinx-asciinema") as tmpdirname:
            for node in self.document.traverse(matcher):
                # TODO: Add sleeptimes options!
                output_name = node["fname"]
                output_fp = Path(tmpdirname) / f"{output_name}"
                command = node["command"]
                # TODO: Merge this to a single list-comprehension
                # And then use zip to build correct inputs
                commands.append(command)
                output_fps.append(output_fp)
                expect_groups.append(node["expects"])
                send_groups.append(node["sends"])

            asyncer.syncify(scripted_asciicasts_runner, raise_sync_error=False)(
                cmds=commands,
                expect_groups=expect_groups,
                send_groups=send_groups,
                output_fps=output_fps,
                sleep_time=SleepTimes(),
            )

            for output_fp in output_fps:
                copy_asset(str(output_fp), str(outdir))


class asciinema(nodes.container):
    pass


def visit_asciinema_node(self: HTML5Translator, node: nodes.Element):
    js_player_options = node["player_options"].json()
    self.body.append(self.starttag(node, "div", CLASS="asciinema"))
    self.body.append("</div>\n")
    template = "<script>\nAsciinemaPlayer.create('/_recs/{fname}', document.getElementById('{id}'), {options});\n</script>"
    tag = template.format(id=node["id"], fname=node["fname"], options=js_player_options)
    self.body.append(tag)


def depart_asciinema_node(self: HTML5Translator, node: nodes.Element):
    pass


class AsciinemaBaseDirective(SphinxDirective):
    has_content: bool = True
    # postpone validation; will use pydantic to validate
    option_spec = {
        "cols": directives.unchanged,
        "rows": directives.unchanged,
        "autoplay": directives.unchanged,
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

        player_options = self.env.config[self.setting_names.player_settings]
        player_options = {**self.options, **player_options}
        validated_player_options = AsciinemaPlayerSettings(**player_options)

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
            data="\n".join(self.content),
            command=self.arguments[0],
            player_options=validated_player_options,
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
    app.add_config_value(player_settings, {}, rebuild="html")
    app.connect("build-finished", copy_local_resources)
    app.add_transform(CommandRunner)
    # FUTURE: Only add js/css resources if Directive in page is found
    app.add_js_file(JS_RESOURCE)
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
    return {}
