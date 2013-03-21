# -*- coding: utf-8 -*-
import time
import sys
from functools import wraps

def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck, e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print msg
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def limpia(antigua):
    antigua = antigua.replace('á','a');
    antigua = antigua.replace('é','e');
    antigua = antigua.replace('í','i');
    antigua = antigua.replace('ó','o');
    antigua = antigua.replace('ú','u');
    antigua = antigua.replace('ñ','n');
    antigua = antigua.replace("'",'*');
    return antigua

def limpia1(antigua):
    antigua = antigua.replace('(','');
    antigua = antigua.replace('*',' ');
    antigua = antigua.replace(')','');
    antigua = antigua.replace('í','i');
    antigua = antigua.replace('ó','o');
    antigua = antigua.replace('ú','u');
    antigua = antigua.replace('ñ','n');
    antigua = antigua.replace("'",'*');
    return antigua

def reorder_list(links, concurrent):
    aux = []
    for url in links:
        for item in concurrent:
            if url == item['url']:
                aux.append(item)
    return aux