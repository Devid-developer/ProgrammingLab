value = 0.0
f = open('shampoo_sales.csv')
for line in f:
    elements = line.split(',')
    if elements[0] !='Date':
        value += float(elements[1])
print(int(value))

