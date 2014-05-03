# Penelophant

[![Build Status](https://travis-ci.org/kevinoconnor7/penelophant.png?branch=master)](https://travis-ci.org/kevinoconnor7/penelophant)

Penelophant is RESTful auction service that provides modular auction types, payment gateways, and authentication systems.

## Install

### Requirements
  * Python 2.7 or 3.3
  * SQLAlchemy Compatible Database (PostgreSQL, MariaDB, SQLite, etc.)

### Getting Started
  1. Duplicate the penelophant.config.DefaultConfig class and give it a
     name for your local config
  2. Ensure your local config subclasses DefaultConfig
  3. Create your virtualenv: ```virtualenv env```
  4. Enter your virtualenv: ```source env/bin/activate```
  5. Install packages: ```pip install -r requirements/dev.txt``` (```pip3.3``` or ```pip-3.3```--whichever works)
  6. Inititalize the database: ```python manage.py -c "penelophant.config.LocalConfig.LocalConfig" initdb``` (```python3```)
  7. Run the server: ```python manage.py -c "penelophant.config.LocalConfig.LocalConfig" runserver``` (```python3```)
  8. To exit your virtualenv when you are done: ```deactivate```

## Heroku
This application can be installed directly to Heroku by switching to the heroku branch ```git checkout heroku```. Then run ```heroku create``` and ```git push heroku heroku:master```. You'll need to set some config settings using environment variables. The config keys to be set can be found in ```EnvConfig.py```. You can use ```heroku config:set KEY=value``` to set these.

## License
We are using the Apache Licence, version 2.0. For the full license
text, please see the included LICENSE file.

