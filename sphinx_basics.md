# Sphinx Documentation Generation Basics

The build phases:

0. Initialization:
  - Search for source files and see if cached results are available
1. Parse source files:
  - Read & Apply directives
  - Output: _doctree_ for _each_ source file stored on disk
    - For elements that aren't yet known, temporary nodes are created
2. Consistency check:
  - Check for errors
3. Resolving
  - Replace all temporary notes with the _actual_ nodes
  - The transformations from temporary to actual nodes ares called... _transformations_
4. Writing
  - Convert the final doctree to the desired output format

## Directive

- Needs a `run` function
  - Returns a list of `nodes`
- Does it need access to `content`?
  - If `Yes`: Needs to set `has_content = True` as a class method
- Has access to:
  - `content` is a list of strings, the directive content line by line
  - `lineno` is the line number of the first line of the directive
  - `block_test` is a string containing the entire directive
  -

## Nodes
- A [container](https://docutils.sourceforge.io/docs/ref/rst/directives.html#container) is _compound body element_
  - Contain specific subelements, like:
    - Caption, label
  - The `container` directive is equivalent to HTML's `<div>` element

## Notes
- `copy_asset_file`: https://github.com/sphinx-doc/sphinx/blob/2be06309518d9401a42880bb5b4321dfdd1e5e90/sphinx/util/fileutil.py#L57
  - For copying from my source to `self.outdir`
- `ensure_tempdir`: https://github.com/sphinx-doc/sphinx/blob/d82d37073920ce0e2940dccbd25f719cc92a3352/sphinx/ext/imgmath.py
  - For seeing how Sphinx works with temporary files
  - If build finished:  `app.connect('build-finished', cleanup_tempdir)`
