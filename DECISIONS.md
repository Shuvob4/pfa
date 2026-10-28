# Personal Finance Assistant

### Why choose `uv` instead of `conda` or `pip`

- `uv` -> is a faster python package and environment manager; which, ensures every machine running the project gets the exact same software setup. To make this repo installed in any machine (macOS, Linux, Windows), needed something which installs `python` itself, builds virtual environment(`.venv`) and handle all dependencies in one command. when executing `uv add`, it generates a `uv.lock` file which contains the exact version and checksums of every library. This ensures the absolute reproducibility on any operating machine.

- `Why not conda` -> `conda` is slow, heavy and lacks a cross-platform lockfile. One of the constraints of the project is to use a locla LLM  and to run everything on most machines, 8 GB RAM was set as a requirement and `conda` with `local LLM` becomes too bulky to run smoothly. 

- `Why not pip?` -> while `pip` installs packages and it requires separate tools to manage the virtual environment and doesn't natively enforce strict cross-platform lockfiles. 

By using `uv` able to replace multiple manual setup steps and thus anyone can run this tool within 15 mins and with the help of `README.md`