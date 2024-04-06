import inspect
import logging


def init(name: str):
    """Initialize the logger."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(asctime)s :: %(message)s',
        filename=f'{name}.log',
        filemode='a+',
        datefmt='%d/%m/%Y %H:%M:%S')


def _log_message(level: str, message: str):
    """Log a message at the specified logging level."""
    frame, filename, _, func_name, _, _ = inspect.stack()[2]
    calling_module = inspect.getmodulename(filename)
    class_name = frame.f_locals.get('self', None).__class__.__name__
    if class_name:
        func_name = f'{class_name}.{func_name}'
    getattr(logging, level)(f'{calling_module}.py - {func_name} - {message}')


def sdebug(message: str):
    _log_message('debug', message)


def sinfo(message: str):
    _log_message('info', message)


def swarning(message: str):
    _log_message('warning', message)


def serror(message: str):
    _log_message('error', message)


def scritical(message: str):
    _log_message('critical', message)
