# Installation
Install the package with:
```
python -m pip install sphinx-cli-recorder
```


Then enable the extension in your [sphinx config (config.py)](https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration).

```python
# note that underscore `_` is used and not `-` as in the pip command!
extensions = [
    "sphinx_cli_recorder"
]
```
```{warning}
There will be **no** 🪟 Windows support in the foreseeable future.
See the [limitations](limitations) section for more details and possible workarounds.
```
