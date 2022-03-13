# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("./asciinema_sphinx"))


# -- Project information -----------------------------------------------------

project = "sphinx-cli-recorder"
copyright = "2022, Kai Norman Clasen"
author = "Kai Norman Clasen"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_cli_recorder",
    "myst_parser",
    "sphinx_external_toc",
    "sphinx_inline_tabs",
    "sphinx_comments",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mermaid",
    "sphinx_design",
]
external_toc_path = "_toc.yml"

comments_config = {"hypothesis": True}

myst_enable_extensions = [
    # "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    # "html_admonition",
    # "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    # "strikethrough",
    "substitution",
    "tasklist",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# target, inventory
intersphinx_mapping = {
    "pexpect": ("https://pexpect.readthedocs.io/en/stable/", None),
    "rich": ("https://rich.readthedocs.io/en/stable/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
myst_url_schemes = [
    "http",
    "https",
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
# pygments_light_style = "monokai"
# pygments_dark_style = "monokai"

# TODO: Fix the ignored load!
sphinx_cli_recorder_player_settings = {"rows": 20}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
