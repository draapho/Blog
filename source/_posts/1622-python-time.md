---
title: python 延时及超时
date: 2016-11-28
categories: python
tags: [python, timeout]
description: 如题.
---

# 实用的例子

## `time.sleep` 单线程阻塞延时

``` python
import time

def time_sleep():
    for i in range(10):
        print i
        time.sleep(1)       # delay 1s, not that accurate

if __name__ == "__main__":
    start = time.time()
    time_sleep()
    end = time.time()
    print "run time: {}".format(end - start)
```

## `time.time` 单线程非阻塞延时/超时

通过比较时间戳实现, 多用于循环中的延时/超时判断

``` python
import time

def time_compare():
    timeout = time.time() + 10  # 10s delay
    for i in range(20):
        print i
        time.sleep(1)
        if timeout < time.time(): # compare the timestamps
            break
    print "time out !"

if __name__ == "__main__":
    start = time.time()
    time_compare()
    end = time.time()
    print "run time: {}".format(end - start)
```

## `threading.Timer` 多线程非阻塞延时

这个例子中, 会先执行完 `threading_main`. 5s后, 才会执行 `threading_sub`
子线程函数可以带参 `threading.Timer(interval, function, args=[], kwargs={})`

``` python
import time
import threading

def threading_main():
    print "main thread: start"
    thrd = threading.Timer(5.0, threading_sub, args = ["sub thread"])
    thrd.start()
    print "main thread: end"

def threading_sub(name):
    print name + ": hello"

if __name__ == "__main__":
    start = time.time()
    threading_main()
    end = time.time()
    print "run time: {}".format(end - start)
```

## `threading.Timer` + `threading.join` 多线程阻塞延时

使用 `join` 语句, 让主线程等待子线程完成后才继续执行
子线程函数可以带参 `threading.Timer(interval, function, args=[], kwargs={})`

``` python
import time
import threading

def threading_main():
    print "main thread: start"
    thrd = threading.Timer(5.0, threading_sub, args = ["sub thread"])
    thrd.start()
    print "main thread: wait"
    thrd.join()     # add this line
    # thrd.join(timeout=2)  # just wait 2s then continue
    print "main thread: end"

def threading_sub(name):
    print name + ": hello"

if __name__ == "__main__":
    start = time.time()
    threading_main()
    end = time.time()
    print "run time: {}".format(end - start)
```

# 装饰器

## 装饰器, 使用`KThread,.localtrace`结束线程. (通用性最好, 性能较低)

``` python
import sys
import threading

class Timeout(Exception):
    """function run timeout"""

class KThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        # Force the Thread to install our trace.
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

def timeout(timeout, default=None, try_except=False):
    """Timeout decorator, parameter in timeout."""
    def timeout_decorator(func):
        def new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        """Wrap the original function."""
        def func_wrapper(*args, **kwargs):
            result = []
            # create new args for _new_func, because we want to get the func
            # return val to result list
            new_kwargs = {
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }

            thd = KThread(target=new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(timeout)
            # timeout or finished?
            isAlive = thd.isAlive()
            thd.kill()

            if isAlive:
                if try_except is True:
                    raise Timeout("{} Timeout: {} seconds.".format(func, timeout))
                return default
            else:
                return result[0]

        func_wrapper.__name__ = func.__name__
        func_wrapper.__doc__ = func.__doc__
        return func_wrapper

    return timeout_decorator

if __name__ == "__main__":
    import time

    @timeout(5)
    def count(name):
        for i in range(10):
            print("{}: {}".format(name, i))
            time.sleep(1)
        return "finished"

    try:
        print count("thread1")
        print count("thread2")
    except Timeout as e:
        print e
```

将上面的例子, 改为函数调用模式, 这样timeout参数可灵活设置!

``` python
import sys
import threading

class Timeout(Exception):
    """function run timeout"""

class KThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        # Force the Thread to install our trace.
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

def timeout_call(timeout, func, args=(), kwargs=None, default=None, try_except=False):
    def new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

    result = []
    kwargs = {} if kwargs is None else kwargs
    # create new args for _new_func, because we want to get the func
    # return val to result list
    new_kwargs = {
        'oldfunc': func,
        'result': result,
        'oldfunc_args': args,
        'oldfunc_kwargs': kwargs
    }

    thd = KThread(target=new_func, args=(), kwargs=new_kwargs)
    thd.start()
    thd.join(timeout)
    # timeout or finished?
    isAlive = thd.isAlive()
    thd.kill()

    if isAlive:
        if try_except is True:
            raise Timeout("{} Timeout: {} seconds.".format(func, timeout))
        return default
    else:
        return result[0]

if __name__ == "__main__":
    import time

    def count(name):
        for i in range(10):
            print("{}: {}".format(name, i))
            time.sleep(1)
        return "finished"

    try:
        print timeout_call(5, count, ["thread1"])
        print timeout_call(5, count, ["thread2"])
    except Timeout as e:
        print e
```


## 装饰器, 使用`thread.interrupt_main()`结束线程. (仅可用于主线程)

``` python
import thread
import threading

def timeout_quit(fn_name):
    thread.interrupt_main()     # raises KeyboardInterrupt

def timeout(s):
    '''
    use as decorator to exit process if
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, timeout_quit, args=[fn.__name__])
            timer.start()
            try:
                result = fn(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return inner
    return outer

if __name__ == "__main__":
    import time

    @timeout(5)
    def processNum(num):
        time.sleep(2)
        return num

    try:
        print processNum(1)
    except KeyboardInterrupt:
        print "timeout"
```


# 学习过程中的例子

## `threading.Timer` + `threading.join` 多线程阻塞延时

使用 `join` 语句, 让主线程等待子线程完成后才继续执行
子线程函数可以带参 `threading.Timer(interval, function, args=[], kwargs={})`


``` python
import time
import threading

def threading_main():
    print "main thread: start"
    thrd = threading.Timer(5.0, threading_sub, args = ["sub thread"])
    thrd.start()
    print "main thread: wait"
    thrd.join()     # add this line
    # thrd.join(timeout=2)  # just wait 2s then continue
    print "main thread: end"

def threading_sub(name):
    print name + ": hello"

if __name__ == "__main__":
    start = time.time()
    threading_main()
    end = time.time()
    print "run time: {}".format(end - start)
```

## `join(timeout=10)` 多进程超时判断

`multiprocessing`的本质是进程, 但是提供了类似于`threading`的一系列方法.
使用 `multiprocessing.terminate` 语句, 让主线程可以杀死子线程
子进程函数可以带参 multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})
multiprocessing 没有 `Timer()` 方法的, 无法方便的延时执行.


注意, 这里没有办法使用 threading 类来实现. 因为没有 `terminate()` 方法,
而如果用`signal`方法来结束线程, 有两个限制. 1, windows不支持. 2, 子线程不支持

``` python
import time
import multiprocessing
import logging

def processing_main():
    print "main process: start"
    prcs = multiprocessing.Process(
        target=processing_sub, args=["sub process"])
    prcs.start()
    print "main process: wait"
    prcs.join(timeout=10)

    # If thread is still active
    if prcs.is_alive():
        print "main process: kill"
        prcs.terminate()
        prcs.join()
    print "main process: end"

def processing_sub(name):
    for i in range(100):
        # if use print, can not show immediately in the console.
        logging.error("{}: {}".format(name, i))
        time.sleep(1)

if __name__ == "__main__":
    start = time.time()
    processing_main()
    end = time.time()
    print "run time: {}".format(end - start)
```


## `multiprocessing.pool` 实现超时判断

说说python下的 thread 和 process.
thread, 提供了signal结束方式, 但是windows不支持, 仅主线程可用! 换句话说, 终止线程很繁琐
process, 提供了terminate结束方式, 但是参数传递限制条件很多, (必须可以是pickle的...)

**下面的代码是有问题的!!!**

``` python
import multiprocessing.pool
import functools

def timeout(timeout, default=None, try_except=False):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            # pool = multiprocessing.pool.Pool(processes=1) ## raise error about pickle problem!!!
            try:
                async_result = pool.apply_async(item, args, kwargs)
                val = async_result.get(timeout)
            except multiprocessing.TimeoutError:
                pool.terminate() ## not work here, because it is acutally thread, not process!!!
                val = default
                if try_except is True:
                    raise multiprocessing.TimeoutError
            else:
                pool.close()
                pool.join()
            return val
        return func_wrapper
    return timeout_decorator

if __name__ == "__main__":
    import time

    @timeout(5)
    def count(name):
        for i in range(10):
            print("{}: {}".format(name, i))
            time.sleep(1)
        return "finished"

    start = time.time()
    print count("thread1")
    print count("thread2")  ## you can find problem here, thread1 is still running...
    end = time.time()
    print "run time: {}".format(end - start)
```

``` python
import multiprocessing

def timeout_call(timeout, func, args=(), kwargs=None, default=None, try_except=False):
    kwargs = {} if kwargs is None else kwargs
    pool = multiprocessing.Pool(processes=1)
    try:
        async_result = pool.apply_async(func, args, kwargs)
        val = async_result.get(timeout)
    except multiprocessing.TimeoutError:
        pool.terminate()
        val = default
        if try_except is True:
            raise multiprocessing.TimeoutError
    else:
        pool.close()
        pool.join()
    return val

################### example ##########
import logging
import time

def count(name):
    for i in range(10):
        logging.error("{}: {}".format(name, i))
        time.sleep(1)
    return "finished"

if __name__ == "__main__":
    ## if count function is here, will raise error!!!

    start = time.time()
    print timeout_call(5, count, ["process1"])
    print timeout_call(5, count, ["process2"])
    end = time.time()
    print "run time: {}".format(end - start)
```

## 第三方方案
- [timeoutcontext 1.1.1](https://pypi.python.org/pypi/timeoutcontext/1.1.1)
  - 基于signal实现, 不支持windows系统, 不支持子线程
- [timeout-decorator 0.3.2](https://pypi.python.org/pypi/timeout-decorator/0.3.2)
  - signal或Multithreading可选
  - 使用signal时, 不支持windows, 不支持子线程
  - 使用Multithreading时, 无法返回不能pickle的数据(因为需要通过pickle来跨进程交换数据)
- [stopit 1.1.1](https://pypi.python.org/pypi/stopit#stopit-threading-timeoutable)
  - threading或signal可选
  - 计时误差太大, 不可接受(翻倍的误差)


## 使用gevent协程

参考 [gevent程序员指南之超时](http://xlambda.com/gevent-tutorial/#_6)
参考 [gevent 延时、定时、超时、io等待、动态添加任务](https://my.oschina.net/1123581321/blog/208671)

``` python
import gevent
from gevent import Timeout

time_to_wait = 5 # seconds

class TooLong(Exception):
    pass

with Timeout(time_to_wait, TooLong):
    gevent.sleep(10)
```




# 参考资料

- [Timeout on a function call](http://stackoverflow.com/questions/492519/timeout-on-a-function-call), 关于此问题的讨论(signal / multiprocessing)
- [论 Python 装饰器控制函数 Timeout 的正确姿势](https://my.oschina.net/leejun2005/blog/607741), 装饰器方式, 性能较低
- [gevent程序员指南](http://xlambda.com/gevent-tutorial/)
- [gevent 延时、定时、超时、io等待、动态添加任务](https://my.oschina.net/1123581321/blog/208671)


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***