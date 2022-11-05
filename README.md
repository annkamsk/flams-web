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