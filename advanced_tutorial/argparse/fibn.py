import argparse


def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
        yield a


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true')
    group.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('num', help='The Fibonacci number '
                        + 'you wish to calculate.', type=int)
    parser.add_argument('-o', '--output', help='Output the result to a file', action='store_true')
    args = parser.parse_args()

    result = []
    sum = 0
    for num in fib(args.num):
        result.append(num)
        sum += num
    if args.verbose:
        print('The ' + str(args.num) + 'th fib number is :')
        print(result)
        print('The ' + str(args.num) + 'th fib number in total :' + str(sum))
    if args.quiet:
        print(result)

    if args.output:
        f = open('finbonacci.txt', 'a')
        f.write(str(result) + '\n')


if __name__ == '__main__':
    main()
