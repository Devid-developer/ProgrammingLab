#classe eccezioni riportata come da direttive
class ExamException(Exception):
    pass


class CSVTimeSeriesFile():
    def __init__(self, name=None):
        #primo controllo sul tipo di parametro passato in input
        if type(name) == str:
            self.name = name
        else:
            raise ExamException("Il valore inserito non e' di tipo stringa")
    
    def get_data(self):
        #serie di controlli atta a verificare che il parametro interessato sia effettivamente un file
        if self.name is not None and is not isinstance(self.name, list):
            if os.path.isfile(self.name):
                time_series = []
                recorded_dates []
                last_date = [0, 0]

                try:
                    file = open(self.name)
                except Exception:
                    raise ExamException("Errore durante l'apertura del file")

                #procedo con la lettura delle righe del file
                if os.stat(self.name).st_size == 0:
                    raise ExamException("Errore, il file e'vuoto")
                else:
                    for line in file:
                        #controllo che la riga da esaminare abbia come primo elemento una data valida, inoltre che ci sia la virgola a separare date e value
                        if line[0] != 1 and line[0] != 2 and ',' is not in line:
                            elem = line.rstrip().split(',')
                            elem[0] = str(elem[0])
                            #sanity check della data
                            if '-' not in elem[0]:
                                #raise ExamException("Errore nel formato della data nella riga {}".format(line+1))
                            else:
                                tmp_date = elem[0].rstrip().split('-')
                                #controllo che le date siano manipolabili
                                try:
                                    tmp_date[0] = int(tmp_date[0])
                                    tmp_date[1] = int(tmp_date[1])
                                    int_check = True
                                except ValueError:
                                    #raise ExamException("La data a riga {} contiene degli errori".format(line+1))
                                    int_check = False
                                if int_check:
                                    #i primi voli di linea risalgono al 1910
                                    #non puo' l'anno corrente essere minore dell'ultimo preso in analisi
                                    if tmp_date[0] < 1910 or tmp_date[0] < last_date[0]:
                                        raise ExamException("Riscontrata data non ordinata o antecedente all'era dell'aviazione")
                                    #controllo finale ordine crescente data
                                    elif tmp_date[0] <= last_date[0] and tmp_date[1] <= last_date[1]:
                                        raise ExamException("Riscontrata data non ordinata")
                                    #controllo che i mesi siano scritti correttamente
                                    elif tmp_date[1] < 1 or tmp_date > 12:
                                        #raise ExamException("Mese non coerente con gli standard internazionali")
                                    #controllo che la data esaminata non sia duplicata
                                    elif tmp_date in recorded_dates:
                                        raise ExamException("Duplicato nella riga {}".format(line+1))
                                    else:
                                        recorded_dates.append(tmp_date)
                                        last_date[0] = tmp_date[0]
                                        last_date[1] = tmp_date[1]

                                        #sanity check valore n passeggeri
                                

                                    
                            
                                



