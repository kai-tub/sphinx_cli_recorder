env-cmd := "pdm run"
node-dir := ".nodeenv"
package-dir := "sphinx_cli_recorder"
asciinema-player-bundle := "node_modules/asciinema-player/dist/bundle"
set dotenv-load := false

install: install_python_deps copy-assets

install_python_deps:
    pdm install

install_node_deps:
    {{env-cmd}} nodeenv --python-virtualenv --force
    {{env-cmd}} npm install

copy-assets: install_node_deps
    cp {{justfile_directory()}}/{{asciinema-player-bundle}}/asciinema-player.css \
        {{justfile_directory()}}/src/{{package-dir}}/
    cp {{justfile_directory()}}/{{asciinema-player-bundle}}/asciinema-player.min.js \
        {{justfile_directory()}}/src/{{package-dir}}/

# rm -rf {{justfile_directory()}}/docs/_build
build:
    {{env-cmd}} sphinx-build {{justfile_directory()}}/docs {{justfile_directory()}}/docs/_build/

serve-docs:
	{{env-cmd}} serve-sphinx-docs

test:
	{{env-cmd}} test
