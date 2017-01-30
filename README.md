Steam Gauge
===========
**NOTE: This repository has been deprecated. Work on Steam Gauge is now tracked [here](https://github.com/jprusik/steam-gauge).**

[Steam Gauge](https://www.mysteamgauge.com) is a Python-based web app driven by [Flask](http://flask.pocoo.org/) that produces data-rich Steam account summaries. It makes use of Steam's Web API, Big Picture API, and metadata gathered using a (presently closed-source) Python app that scrapes data from the Steam Store pages (when necessary). That metadata is stored in a SQL database for easy retrieval by the Steam Gauge app. The app has undergone several revisions, including a migration from Python 2 to 3 and has subsequently been open-sourced. This repository being made available for reference and represents the final state of the work predating that migration (for security reasons, it does not include the full history of the original repo), and is no longer being developed.


Requirements
------------
- Python 2.7.5
- Package requirements can be found in `requirements.txt` and installed using pip


Usage
-----
- create `config.py` in the app directory and give values to your app constants
- if you're running locally, run app.py from the app directory. Otherwise, refer to documentation on setting up and using [Passenger](https://www.phusionpassenger.com/) with your server.
- access with your client at `http://127.0.0.1:5000` by default


Author
------
Jonathan Prusik @jprusik [www.classynemesis.com]
