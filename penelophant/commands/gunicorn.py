# import sys
# from flask_script import Command, Option, warnings

# class Gunicorn(Command):
#     description = 'Runs production server with gunicorn'

#     def __init__(self, host='127.0.0.1', port=5000, **options):
#         self.port = port
#         self.host = host
#         self.server_options = options

#     def get_options(self):
#         options = (
#             Option('--gunicorn-host',
#                    dest='host',
#                    default=self.host),

#             Option('--gunicorn-port',
#                    dest='port',
#                    type=int,
#                    default=self.port),

#             Option('--gunicorn-config',
#                    dest='gconfig',
#                    type=str,
#                    required=True))

#         return options

#     def handle(self, app, host, port, gconfig, **kwargs):
#         from configparser import ConfigParser
#         gc = ConfigParser()
#         gc.read(gconfig)
#         section = 'default'

#         bind = "%s:%s" % (host, str(port))
#         workers = gc.get(section, 'workers')
#         pidfile = gc.get(section, 'pidfile')
#         loglevel = gc.get(section, 'loglevel')

#         # Suppress argparse warnings caused by running gunicorn's argparser
#         # "inside" Flask-Script which imports it too...
#         warnings.filterwarnings("ignore", "^.*argparse.*$")

#         from gunicorn import version_info
#         if version_info >= (0, 9, 0):
#             from gunicorn.app.base import Application

#             class FlaskApplication(Application):
#                 def init(self, parser, opts, args):
#                     return {
#                         'bind': bind,
#                         'workers': workers,
#                         'pidfile': pidfile,
#                         'loglevel': loglevel
#                     }

#                 def load(self):
#                     return app

#             # Hacky! Do not pass any cmdline options to gunicorn!
#             #sys.argv = sys.argv[:2]

#             print("Logging to stderr with loglevel '%s'" % loglevel)
#             print("Starting gunicorn...")
#             FlaskApplication().run()
#         else:
#             raise RuntimeError("Unsupported gunicorn version! Required > 0.9.0")

from flask_script import Command, Option
from gunicorn.app.base import Application

class Gunicorn(Command):
  description = 'Run the app within Gunicorn'

  def __init__(self, host='127.0.0.1', port=8000, workers=6):
    self.port = port
    self.host = host
    self.workers = workers

  def get_options(self):
    return (
      Option('-t', '--host',
             dest='host',
             default=self.host),

      Option('-p', '--port',
             dest='port',
             type=int,
             default=self.port),

      Option('-w', '--workers',
             dest='workers',
             type=int,
             default=self.workers),
    )

  def handle(self, app, *args, **kwargs):

    host = kwargs['host']
    port = kwargs['port']
    workers = kwargs['workers']

    def remove_non_gunicorn_command_line_args():
      import sys
      args_to_remove = ['--port','-p','--appconfig']
      def args_filter(name_or_value):
        keep = not args_to_remove.count(name_or_value)
        if keep:
          previous = sys.argv[sys.argv.index(name_or_value) - 1]
          keep = not args_to_remove.count(previous)
        return keep
      sys.argv = list(filter(args_filter, sys.argv))

    remove_non_gunicorn_command_line_args()

    from gunicorn import version_info
    if version_info < (0, 9, 0):
      from gunicorn.arbiter import Arbiter
      from gunicorn.config import Config
      arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)),'workers': workers}), app)
      arbiter.run()
    else:
      class FlaskApplication(Application):
        def init(self, parser, opts, args):
          return {
            'bind': '{0}:{1}'.format(host, port),
            'workers': workers
          }

        def load(self):
          return app

    FlaskApplication().run()
