""" Penelophant Views """

from penelophant import app

@app.route('/')
def index():
  """ Place holder index page """
  return "Hello World!"
