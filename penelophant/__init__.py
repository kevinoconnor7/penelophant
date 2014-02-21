""" Penelophant Backend App """
from flask import Flask
import penelophant.settings as settings

app = Flask(__name__)
app.config.from_object(settings)

# HACK: see https://github.com/twilio/flask-restful/issues/8
#       and https://github.com/twilio/flask-restful/pull/9
saved_handlers = app.handle_exception, app.handle_user_exception
app.handle_exception, app.handle_user_exception = saved_handlers

import penelophant.views
import penelophant.models
