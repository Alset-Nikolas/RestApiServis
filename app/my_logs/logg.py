
import logging
import logging.config

log_config = {
    'version': 1,
    'formatters': {
        'my_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
    },
    'paths': {
        'file_handler_info': {
            'class': 'logging.FileHandler',
            'formatter': 'my_formatter',
            'filename': 'app/my_logs/info_log.log',
        },
        'file_handler_error': {
            'class': 'logging.FileHandler',
            'formatter': 'my_formatter',
            'filename': 'app/my_logs/error_log.log',
        },
    },
    'loggers': {
        'info_log': {
            'paths': ['file_handler_info'],
            'level': 'INFO',
        },
        'warning_log': {
            'paths': ['file_handler_error'],
            'level': 'WARNING',
        },
    },
}


logging.config.dictConfig(log_config)
info_log = logging.getLogger('info_log')
warning_log = logging.getLogger('warning_log')

