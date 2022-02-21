__version__ = "0.1.0"

from docutils import nodes
from docutils.parsers.rst import Directive
from typing import List, Dict, Any, Optional
from sphinx.application import Sphinx
from sphinx.writers.html5 import HTML5Translator
import tempfile
from sphinx.util.fileutil import copy_asset
from pathlib import Path
from sphinx.application import Sphinx
import importlib

from sphinx.util import logging
import sphinx_auto_asciinema
from functools import partial

logger = logging.getLogger(__name__)

JS_RESOURCE = "asciinema-player.min.js"
CSS_RESOURCE = "asciinema-player.css"
TEST_RESOURCE = "test.rec"


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
            logger.warning(outdir)
            if exception is None:
                copy_asset(str(resource_path), str(outdir))


class asciinema(nodes.container):
    pass


def visit_asciinema_node(self: HTML5Translator, node: nodes.Element):
    # node.content would contain the commands to execute
    # with maybe some magic lines to configure the input/output
    # node.options would be passed to the template
    # options would be defined by Directive
    # id given by anchor tag
    self.body.append(self.starttag(node, "div", CLASS="asciinema"))
    self.body.append("</div>\n")
    template = (
        "<script>"
        "AsciinemaPlayer.create('/_static/test.rec', document.getElementById('asciinema-0'));"
        "</script>"
    )
    self.body.append(template)


def depart_asciinema_node(self: HTML5Translator, node: nodes.Element):
    pass
    # self.body.append("</div>\n")


class AsciinemaDirective(Directive):
    has_content = True

    def run(self) -> List[nodes.Node]:
        self.assert_has_content()
        text = "\n".join(self.content)
        # FUTURE: replace with self.env.new_serialno("asciinema")
        target_id = "asciinema-0"

        # in HTML the target_id is the anchor name!
        target_node = nodes.target(rawsource="", text="", ids=[target_id])

        asciinema_node = asciinema()
        # asciinema_node += nodes.title(rawsource="Title", text="Title")

        return [target_node, asciinema_node]


def setup(app: Sphinx) -> Dict[str, Any]:
    app.add_node(
        asciinema,
        html=(visit_asciinema_node, depart_asciinema_node),
    )
    copy_local_resources = partial(
        copy_resources, resources=[JS_RESOURCE, CSS_RESOURCE, TEST_RESOURCE]
    )
    app.connect("build-finished", copy_local_resources)
    # FUTURE: Only add js/css resources if Directive in page is found
    app.add_js_file(JS_RESOURCE)
    app.add_css_file(CSS_RESOURCE)
    app.add_directive("asciinema", AsciinemaDirective)
    return {}
