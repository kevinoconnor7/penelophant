# Penelophant

[![Build Status](https://travis-ci.org/kevinoconnor7/penelophant.png?branch=master)](https://travis-ci.org/kevinoconnor7/penelophant)

Penelophant is RESTful auction service that provides modular auction types, payment gateways, and authentication systems.

## Install

### Requirements
  * Python 2.7
  * SQLAlchemy Compatible Database (Postgres, MySQL, SQlite, etc.)

### Create Config
  1. Duplicate the penelophant.config.DefaultConfig class and give it a name for your local config
  2. Ensure your local config subclasses DefaultConfig
  3. Create your virtualenv: ```virtualenv env```
  4. Install packages: ```pip install -r requirements/dev.txt```
  5. Inititalize the database: ```python manage.py -c "penelophant.config.LocalConfig" initdb```
  6. Run the server: ```python manage.py -c "penelophant.config.LocalConfig" runserver```

## License
For the full license text, please see the included LICENSE file.

