import threading
import time

class Asyc_write(threading.Thread):
    def __init__(self, text, out):
        threading.Thread.__init__(self)
        self.text = text
        self.out = out

    def run(self):
        f = open(self.out, 'a')
        f.write(self.text + '\n')
        f.close()
        time.sleep(2)
        print('finished backgourd file write to ' + self.out)

def main():
    message = input('Enter a string to store:')
    backgroud = Asyc_write(message, 'out.txt')
    backgroud.start()
    print('the program can continue to run while it write in another thread.')
    print(100 + 500)

    backgroud.join()
    print('wait the program to finish.')

if __name__ == '__main__':
    main()

