import threading

# Function for Thread
def up_thread(func, *args):
    thread = threading.Thread(target=func, args=tuple(args))
    thread.start()
    return thread

def up_thread_daemon(func, *args):
    thread = threading.Thread(target=func, args=tuple(args))
    thread.setDaemon(True)
    thread.start()
    return thread