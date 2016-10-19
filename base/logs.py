import logging

class Logger(object):

    def init_app(self, app):
        self.LOG_FILENAME = app.config['LOG_FILENAME']
        from logging.handlers import RotatingFileHandler
        from logging import Formatter
        app.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            self.LOG_FILENAME,
            maxBytes=1024 * 1024 * 100,
            backupCount=20
            )
        handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '))
        app.logger.addHandler(handler)