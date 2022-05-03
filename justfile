env-cmd := "poetry run"
node-dir := ".nodeenv"
package-dir := "sphinx_cli_recorder"
asciinema-player-bundle := "node_modules/asciinema-player/dist/bundle"
set dotenv-load := false

install: install_python_deps install_ipykernel install_node_deps

install_python_deps:
    poetry install

install_ipykernel:
	{{env-cmd}} python -m ipykernel install --user

install_node_deps: copy-assets
    {{env-cmd}} nodeenv --python-virtualenv --force
    {{env-cmd}} npm install

copy-assets:
    cp {{justfile_directory()}}/{{asciinema-player-bundle}}/asciinema-player.css \
        {{justfile_directory()}}/{{package-dir}}/
    cp {{justfile_directory()}}/{{asciinema-player-bundle}}/asciinema-player.min.js \
        {{justfile_directory()}}/{{package-dir}}/

# rm -rf {{justfile_directory()}}/docs/_build
build: install_ipykernel
    {{env-cmd}} sphinx-build {{justfile_directory()}}/docs {{justfile_directory()}}/docs/_build/

serve-docs: build
	{{env-cmd}} python {{justfile_directory()}}/serve_docs.py

test:
	{{env-cmd}} pytest tests/
