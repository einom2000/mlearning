import threading
import time

t_lock = threading.Lock()


def timer(name, delay, repeat):
    print('Timer ' + name + ' Started:')
    t_lock.acquire()
    print(name + 'has acquired a lock.')
    while repeat > 0:
        time.sleep(delay)
        print(name + ': ' + str(time.ctime(time.time())))
        repeat -= 1
    t_lock.release()
    print(name + 'is releasing the lock')
    print('Timer ' + name + ' completed.')


def main():
    t1 = threading.Thread(target=timer, args=('Timer1', 1, 5))
    t2 = threading.Thread(target=timer, args=('Timer2', 2, 5))
    t1.start()
    t2.start()

    print('main completed!')


if __name__ == '__main__':
    main()

