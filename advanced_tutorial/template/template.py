from string import  Template

class MyTemplate(Template):
    delimiter = '#'


def main():
    cart = []
    cart.append(dict(item='Coke', price=8, qty=2))
    cart.append(dict(item='Cake', price=14, qty=5))
    cart.append(dict(item='Fish', price=23, qty=8))

    t = MyTemplate('#qty * #item = #price')
    total = 0
    print('cart:')
    for data in cart:
        print(t.substitute(data))
        total += data['price']
    print('total: ' + str(total))


if __name__ == '__main__':
    main()
