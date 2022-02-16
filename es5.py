class Model():
    def __init__(self):
        pass
    
    def fit(self, data):
        raise NotImplementedError('Metodo non implementato')

    def predict(self, data):
        raise NotImplementedError('Metodo non implementato')

class IncrementModel(Model):
    def predict(self, data):
        somma = 0
        prec = data[0]
        for element in data[1:]:
            somma += element - prec
            prec = element
        return somma/(len(data)-1)+prec

class FitIncrementModel(IncrementModel):
    def __init__(self, data):
        self.total_data = data

    def fit(self, n):
        somma = 0
        prec = self.total_data[0]
        for element in self.total_data[1:(len(self.total_data)-n)]:
            somma += element - prec
            prec = element
        self.avg_increment = somma/(len(self.total_data)-n-1)

    def predict(self, data):
        self.fit(len(data))
        somma = 0
        prec = data[0]
        for element in data[1:]:
            somma += element - prec
            prec = element
        return ((somma/(len(data)-1)+self.avg_increment)/2)+prec


data = [8,19,31,41,50,52,60]
my_model = FitIncrementModel(data)
predict = my_model.predict([50,52,60])
print("Predizione: {}".format(predict))

from matplotlib import pyplot
pyplot.plot(data + [predict], color = 'tab:red')
pyplot.plot(data, color = 'tab:blue')
pyplot.show()