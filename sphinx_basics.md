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
  - Needs to set `has_content = True` as a class method
  -
