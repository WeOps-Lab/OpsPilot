from threading import Thread


def async_fun(f):
    """异步非阻塞函数装饰器

    Args:
        f (Function): 需要异步非阻塞属性的函数
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
