import logging.config
import sys

from app.config import settings

LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        'root': {
            'level': 'WARNING' if not settings.DEBUG else 'DEBUG',
            'handlers': ['console'],
        },
        'converter': {
            'level': 'INFO' if not settings.DEBUG else 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'error_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stderr,
        },
    },
    formatters={
        'generic': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
            'class': 'logging.Formatter',
        },
        'verbose': {
            'format': '%(asctime)s [%(process)d/%(threadName)s] [%(levelname)-5.8s] %(message)s (%(name)s:%(module)s:%(lineno)s)',
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
            'class': 'logging.Formatter',
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)-5.8s] %(message)s'
        },

    },
)


logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
logger = logging.getLogger('api')


def run():
    import uvicorn
    from app.application import server

    uvicorn.run(
        'app.application:server' if settings.DEBUG else server,
        host=settings.HTTP_HOST.host, port=settings.HTTP_PORT,
        reload=settings.DEBUG,
    )


if __name__ == '__main__':
    run()
