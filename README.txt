Art Mirror
==========

Art Mirror is an interactive system that matches a user's pose to an artwork containing a similar pose.

Art Mirror was developed in Spring 2021 as Project 2 for CPSC 484 (Introduction to HCI) at Yale College: 
https://cpsc484-584-hci.gitlab.io/s21/project2/


Installation
============
1. To install the dependencies for Art Mirror, navigate to the root of this repository and create a Python virtual environment.

    $ python3 -m venv venv

2. Then, activate the virtual environment.

    $ source venv/bin/activate

3. Within the virtual environment, upgrade pip and install the dependencies

    $(venv) pip install --upgrade pip
    $(venv) pip install -r requirements.txt


How to run
==========

1. First, navigate to the root of the repository and activate the virtual environment. Then, run the command:

    $(venv) python -m src.artmirror --websocket-server 172.29.41.16:8888 --local-port 6677

2. Finally, navigate to [http://localhost:6677](http://localhost:6677) in a web browser to preview the prototype.


Dependencies
============
Art Mirror requires (and includes) JQuery v3.5.1 and Bulma v0.9.2

Additional dependencies installed by pip are Tornado Web Server v6.1 and NumPy v1.20.2
sci-kit learn v0.24.1 is installed only for legacy purposes, and may not be required in the most recent iteration of Art Mirror.