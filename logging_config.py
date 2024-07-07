import os


CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(process)d:%(threadName)-s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
            'formatter': 'default',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 2,
            'filename': 'unno-tech-api.log',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
            'propagate': False
        }
    }
}
