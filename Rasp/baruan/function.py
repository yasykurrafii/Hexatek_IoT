import threading

def up_thread(func, *args):
    thread = threading.Thread(target = func, args = tuple(args))
    thread.start()

def opening_file(filename : str, method : str, message : str or list):
    with open(filename, method) as f:
        command_method = {"w" : __writing_file(f, message)}
        try :
            return command_method[method]
        except:
            raise "your method only can 'w' or 'r'"

def __writing_file(file, message : str):
    file.write(message)


