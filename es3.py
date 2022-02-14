class CSVFile:
    def __init__(self, file, nome):
        self.name = nome
        self.file = file

    def get_data(self):
        data = []
        for line in self.file:
            elements = line.split(',')
            if elements[0] != 'Date':
                tmp = [elements[0], float(elements[1])]
                data.append(tmp)
                
        return data

my_file = open('shampoo_sales.csv')
test = CSVFile(my_file, 'shampoo_sales')
print(test.get_data())
my_file.close()


            