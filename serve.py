from livereload import Server, shell

server = Server()
run_cmd = shell("just build")
for watch_dir in [
    "docs/*.py",
    "docs/*.rst",
    "docs/*.py",
    "sphinx_auto_asciinema/*.py",
    "sphinx_auto_asciinema/_static/*",
]:
    server.watch(watch_dir, run_cmd)

server.serve(root="docs/_build/")
