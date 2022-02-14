class Model():

    def __init__(self):
        pass

    def fit(self, data):
        raise NotImplementedError("Metodo non implementato")

    def prediction(self, data):
        raise NotImplementedError("Metodo non implementato")

class IncrementModel(Model):
    def prediction(self, data):
        somma = 0
        elementoPrecedente = data[0]
        for element in data[1:]:
            somma += element - elementoPrecedente
            elementoPrecedente = element
        return (somma/len(data[:-1]))+elementoPrecedente

my_model = IncrementModel()
print("Predizione: {}".format(my_model.prediction([50,52,60])))


