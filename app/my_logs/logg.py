import logging.config
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },

    'loggers': {
        'my_logger': {
            'handlers': ['stream_handler'],
            'level': 'WARNING',
            'propagate': True
        },
        'my_logger_error': {
            'handlers': ['stream_handler'],
            'level': 'WARNING',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
info_log = logging.getLogger('my_logger')

warning_log = logging.getLogger('my_logger_error')

# warning_log = logging.getLogger('warning_log')
# warning_log.setLevel(logging.ERROR)
#
# logging.warning('dd')