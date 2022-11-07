# FLAMS-web

## Install
Download this repository:
`git clone git@github.com:annkamsk/flams-web.git`

Download FLAMS repository:
`git clone git@github.com:annkamsk/flams.git`

`cd flams-web`

Create symlink to flams inside flams-web:
`ln -s ../flams flams`

Install dependencies:
`pip install -r requirements.txt`

## Run

`python -m flams_web.app`

## Adding new dependencies/updating old
We use [pip-tools](https://pypi.org/project/pip-tools/) to manage python dependencies. You can install it with:

`pip install pip-tools`

If you're adding a new dependency, add the package name to `requirements.in`.

Refresh `requirements.txt`:

`pip-compile requirements.in`

The `requirements.txt` should get updated after that. However, in our `requirement.in` file we have a line `-e flams` (which instructs pip to install a flams package from a local directory). Due to a bug, this line will be translated to `-e your/local/system/path/flams` in `requirements.txt`. Just remove the local part, so the line is: `-e flams`.