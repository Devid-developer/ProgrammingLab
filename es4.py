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

my_model = IncrementModel()
print("Predizione: {}".format(my_model.predict([50,60,70,80])))