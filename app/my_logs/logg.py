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
            'level': 'INFO',
            'propagate': True
        },
        'my_logger_error': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
info_log = logging.getLogger('my_logger')
info_log.info('debug log')

warning_log = logging.getLogger('my_logger_error')
info_log.info('debug log')

# warning_log = logging.getLogger('warning_log')
# warning_log.setLevel(logging.ERROR)
#
# logging.warning('dd')