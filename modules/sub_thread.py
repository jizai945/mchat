import threading, inspect, ctypes

# 在线程中抛出异常，使线程退出
def async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    try:
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as e:
        print(e)
        pass

# 线程运行
def thread_run(cb, *args,**kwargs):
    
    thread = threading.Thread(target=cb, args=args, kwargs=kwargs)
    thread.setDaemon(True) # 将子线程设置成守护线程 防止主线程退出子线程还在运行
    thread.start()
    return thread

# 线程退出
def thread_exit(thread):
    async_raise(thread.ident, SystemExit)