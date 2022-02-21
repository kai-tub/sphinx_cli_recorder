__version__ = "0.1.0"

from docutils import nodes

from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from typing import List, Dict, Any, Optional
from sphinx.application import Sphinx
from sphinx.writers.html5 import HTML5Translator
import tempfile
from sphinx.util.fileutil import copy_asset
from pathlib import Path
from sphinx.application import Sphinx
import importlib
from docutils.transforms import Transform

from sphinx.util import logging
import sphinx_auto_asciinema
from functools import partial
from asciinema.recorder import record
from sphinx.util.nodes import NodeMatcher

logger = logging.getLogger(__name__)

JS_RESOURCE = "asciinema-player.min.js"
CSS_RESOURCE = "asciinema-player.css"

# TODO: Always purge directory; should be configurable if desired to only update if document has changed
# TODO: Add options to player and recorder


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
        with tempfile.TemporaryDirectory(prefix="sphinx-asciinema") as tmpdirname:
            for node in self.document.traverse(matcher):
                output_name = node["fname"]
                output_fp = Path(tmpdirname) / f"{output_name}"
                record(output_fp, command=node["content"][0])
                copy_asset(str(output_fp), str(outdir))


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


class asciinema(nodes.container):
    pass


def visit_asciinema_node(self: HTML5Translator, node: nodes.Element):
    # node.content would contain the commands to execute

    # with maybe some magic lines to configure the input/output
    # node.options would be passed to the template
    # options would be defined by Directive

    self.body.append(self.starttag(node, "div", CLASS="asciinema"))
    self.body.append("</div>\n")
    template = "<script>\nAsciinemaPlayer.create('/_recs/{fname}', document.getElementById('{id}'));\n</script>"
    tag = template.format(id=node["id"], fname=node["fname"])
    self.body.append(tag)


def depart_asciinema_node(self: HTML5Translator, node: nodes.Element):
    pass


class AsciinemaDirective(SphinxDirective):
    has_content = True

    option_spec = {}
    optional_arguments = len(option_spec)

    def run(self) -> List[nodes.Node]:
        self.assert_has_content()

        _id = self.state.document.settings.env.new_serialno("asciinema")
        target_id = f"asciinema-{_id}"
        # in HTML the target_id is the class id value!
        # Future: Understand if/how to not repeat target_id and use it in two different parts
        # IndexDirective does it the same way
        target_node = nodes.target(rawsource="", text="", ids=[target_id])
        asciinema_node = asciinema(
            fname=f"{target_id}.rec",
            content=self.content,
            id=target_id,
        )
        return [target_node, asciinema_node]


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(
        asciinema,
        html=(visit_asciinema_node, depart_asciinema_node),
    )
    copy_local_resources = partial(
        copy_resources, resources=[JS_RESOURCE, CSS_RESOURCE]
    )
    app.connect("build-finished", copy_local_resources)
    app.add_transform(CommandRunner)
    # FUTURE: Only add js/css resources if Directive in page is found
    app.add_js_file(JS_RESOURCE)
    app.add_css_file(CSS_RESOURCE)
    app.add_directive("asciinema", AsciinemaDirective)
    return {}
