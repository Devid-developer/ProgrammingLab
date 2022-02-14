class CSVFile:
    def __str__(self, file, nome):
        self.name = nome
        self.file = file

    def get_data(self):
        data = []
        for line in self.file:
            if line != 'Date,Sales':
                data.append(line)
        return data

open('shampoo_sales.csv')


            