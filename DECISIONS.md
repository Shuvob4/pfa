# Personal Finance Assistant

### Environment Management

**Chose:** `uv` with a committed `uv.lock` file.

**Rejected:** `conda`

**Why:** `uv` provides a single, exceptionally fast tool that installs Python itself, builds the virutal environment, and manage dependencies across different operating systems. It generates a strict cross-platform lockfile (`uv.lock`), which ensures absolute reproducibility. `Conda` is slower, lacks standard cross-platform lockfile, and it's a separate installation.


### Configuration and Data Paths

**Chose:** Dynamic OS-standard directories using *Python's* `platformdirs` library.

**Rejected:** Hard-coded absolute paths(e.g. `/Users/janedoe/`) and storing configuration/data files directly inside the Git repository.

**Why:** Hard-coded paths breaks instantly on another person's machine due to folder structure. Storing config files in the repo creates major securtiy risks of accidentally committing sensitive personal settings. Also, when a python project is packaged and installed on a server it runs from a read-only system directory and doesn't have localized `repo folder` to read or write to. `platformdirs` makes the pipeline fully portable by automatically locating the correct writeable app directories for the specific operating system it runs on. 

### Configuration Validation

**Chose:** Pydantic with `extra="forbid"`

**Rejected:** Pydantic's default behavior, which silently ignores unknown keys.

**Why:** If a user makes a typo error in their config file(e.g. typing `modle` instead of `model`), default Pydantic will silently drop the invalid key and apply the default setting, which will be annoying at the time of debugging as the user might believe they have changed a setting but the program ingores it. Using `extra="forbid"` enforces the principal of falling loudly and provifing an immediate, clear error message.

### Template Packaging

**Chose:** Placing `fpa.example.toml` inside the `src/fpa/` package directory and reading it with `importlib.resources`

**Rejected:** Storing the template at the repository root.

**Why:** When a python project is installed by an end user, only the files explicitly inside the package directory(`src/`) are bundled into the installation. If the template is left at the root, a user who installs the tool will not receive the file and commands like `fpa init` will crash because they cannot find the template to copy.

### Repository Visibility

**Chose:** Public GitHub repo.

**Rejected:** Private GitHub repo.

**Why:** To ensure true cross-platform compatibility, the project must be tested on macOS, Windows, and Linux runners. GitHub Actions provides free, unlimited runner minutes for public repositories, whereas Mac and Windows runners deplete private repo minute allowances very quickly.  `.gitignore` explicitly blocks personal PDF's, local databases, and the `fpa.toml` personal settings from being uploaded.