import re
a = 'a + b + c + ? = 10^@#@0 [10,90]'
temp = re.sub('[a-zA-Z!"#$%&\'().:;@\\^_`{|}~ \t\n\r\x0b\x0c]', '', a).replace(' ','')
temp_index = temp.find('[')
temp1 = temp[:temp_index]
temp2 = temp[temp_index + 1: -1].split(',')
try:
    temp2[0] = int(temp2[0])
    temp2[1] = int(temp2[1])
except ValueError:
    print('Error!')
print(temp1)
print(temp1.find('='))
print(temp[temp.find('=') + 1 :temp.find('[')])
print(temp[temp.find('[') + 1 :temp.find(']')].split(','))
