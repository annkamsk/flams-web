# FLAMS-web

## Install
Download this repository:
`git clone git@github.com:annkamsk/flams-web.git`

`cd flams-web`

Install dependencies:
`pip install -r requirements.txt --force-reinstall`

`--force-reinstall` is to force pip to get the version of flams that's up-to-date with main. 

## Run

`python -m flams_web.app`

## Adding new dependencies/updating old
We use [pip-tools](https://pypi.org/project/pip-tools/) to manage python dependencies. You can install it with:

`pip install pip-tools`

If you're adding a new dependency, add the package name to `requirements.in`.

Refresh `requirements.txt`:

`pip-compile requirements.in`