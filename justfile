env-cmd := "poetry run"
node-dir := ".nodeenv"
package-dir := "sphinx_auto_asciinema"
asciinema-player-bundle := "node_modules/asciinema-player/dist/bundle"

install:
    poetry install
    {{env-cmd}} nodeenv {{node-dir}} --force
    echo 'May need to re-open terminal to access `npm`!'

copy-assets:
    cp {{justfile_directory()}}/{{asciinema-player-bundle}}/asciinema-player.css \
        {{justfile_directory()}}/{{package-dir}}/
    cp {{justfile_directory()}}/{{asciinema-player-bundle}}/asciinema-player.min.js \
        {{justfile_directory()}}/{{package-dir}}/

build: copy-assets
    rm -rf {{justfile_directory()}}/docs/_build
    sphinx-build {{justfile_directory()}}/docs {{justfile_directory()}}/docs/_build/

serve: build
    {{env-cmd}} python {{justfile_directory()}}/serve.py
