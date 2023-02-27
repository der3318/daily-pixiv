# -*- coding: utf-8 -*-

# standard libs
from time import sleep

# third party libs
from rich import inspect    # pip install rich


class RetryOnFailure(object):

    # max iterations to try the action
    trials = 10

    # interval in seconds
    cooldown = 30

    def __call__(self, func):
        def wrappee(*args, **kwargs):
            exception = None
            for trial in range(RetryOnFailure.trials):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    exception = e
                    sleep(RetryOnFailure.cooldown)
            inspect(exception)
            raise exception
        return wrappee

