# checkpoint1
Introduction

Checkpoint 1 is a python Powered room allocation system.
It has the following features;
* Create rooms at a facility
* Add Fellows and Staff members to the facility
* Allows users to edit added details
* Add employees and allocate living rooms  at one of Andela’s facilities called The ~dojo.

The building blocks are:

* Python 3
* PostgreSQL or MySQL

## Setting Up for Development

These are instructions for setting up the room allocation system

* prepare directory for project code and virtualenv:

        $ mkdir -p ~/CP1
        $ cd ~/CP1

* prepare virtual environment

        $ virtualenv --python=python3 cp-venv
        $ source cp-venv/bin/activate
        $ cd/checkpoint1

* check out project code:

        $ git clone https://github.com/bmwachajr/checkpoint1.git

* install requirements into the virtualenv:

        $ pip install -r requirements.txt

* run the system:

        $ cd modules
        $ python main.py
