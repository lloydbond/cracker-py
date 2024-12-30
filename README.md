# cracker
A plain and simple termainl ui for exploring and starting tasks.

- [Requirements](#requirements)
- [Supports](#supports)
- [Installation Methods](#installation-methods)
  - [Install with cargo](#install-with-cargo)
  - [Manual Installation](#manual-installation)
- [Usage](#usage)
  - [Enable Log Messages](#enable-log-messages)
- [TODO](#todo)
- [Motivation](#motivation)
- [Who is this For](#who-is-this-for)

## Requirements

* [rust-lang](https://www.rust-lang.org/) >= 1.81.0

Be sure to add $HOME/.cargo/bin/ to your environment PATH variable.
## Supports

-   Linux
-  *macOS
-  *Windows Subsystem for Linux (WSL)

\* untested, should work.
## Installation Methods
### Install with python
If you haven't isntalled `python` yet, now's a good time.
Follow the python install instructions [here](https://www.python.org/downloads/)
Then run from your terminal.
```bash
cargo install ck-cracker
```

### Manual Installation
Ensure you have poetry installed from [here](https://python-poetry.org/docs/#installation)

Clone the repository:

```bash
git clone git@github.com:lloydbond/cracker-py.git
cd cracker-py
poetry env use 3.12.8
poetry shell
poetry install
poetry build
deactivate
pip install dist/cracker-`poetry version | cut -d ' ' -f 2`-py3-none-any.whl

```

## Usage

```bash
  cd /path/to/with/Makefile
  ck
```

### Enable Log messages
Log messages are limited for as the tool reaches a 1.0 release.
```bash
  ck --log=[warn|info|error|debug|critical]

  ck --log=debug
```
## TODO:
- [ ] Support additional task runner type build scripts
  - [x] npm
  - [ ] grunt
  - [ ] taskpy
  - [ ] etc.
- [ ] performance imporvements for something like `cat my_massive_200million_line.log`
    * probably not usefule but a known limitation *
- [ ] hx/vi compatible keymapping
- [ ] add to pypi.org
- [ ] CICD


## Motivation

### Who is this For
Quick and easy execution and monitoring of Makefile and other types of runners for your local project.
When you need to give a laymon commands to run and they are averse to typing in a terminal.

### ***Note from the maintainer***

Any improvements, code style, or feed back will go along way for this project. Any contributions or
additions to the supported Task runners as well as UI beautifcations or simplifications are greatly
welcomed and appreciated. Happy Coding!

