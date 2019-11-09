import time
import queue

def task(name, queue):
    while not queue.empty():
        delay = queue.get()
        t = time.time()
        print(f'Task {name} running')
        time.sleep(delay)

        print(f'Task {name}')


