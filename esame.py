import os

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
        if self.name is not None and not isinstance(self.name, list):
            if os.path.isfile(self.name):
                time_series = []
                recorded_dates = []
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
                        if line != '\n' and line[0] == '1' or line[0] == '2' and ',' in line:
                            tmp_time_series = []
                            elem = line.rstrip().split(',')
                            elem[0] = str(elem[0])
                            #sanity check della data
                            if '-' not in elem[0]:
                                pass
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
                                    if tmp_date[0] < 1910:
                                        pass
                                        #raise ExamException("Riscontrata data antecedente all'era dell'aviazione")
                                    elif tmp_date[0] < last_date[0]:
                                        raise ExamException("Riscontrata data non ordinata")
                                    #controllo finale ordine crescente data
                                    elif tmp_date[0] <= last_date[0] and tmp_date[1] <= last_date[1]:
                                        raise ExamException("Riscontrata data non ordinata")
                                    #controllo[1] che i mesi siano scritti correttamente
                                    elif tmp_date[1] < 1 or tmp_date[1] > 12:
                                        pass
                                        #raise ExamException("Mese non coerente con gli standard internazionali")
                                    #controllo che la data esaminata non sia duplicata
                                    elif tmp_date in recorded_dates:
                                        raise ExamException("Duplicato nella riga {}".format(line+1))
                                    else:
                                        recorded_dates.append(tmp_date)
                                        last_date[0] = tmp_date[0]
                                        last_date[1] = tmp_date[1]
                                        tmp_time_series.append(str(elem[0]))
                                        #sanity check valore n passeggeri
                                        tmp_value = -1
                                        int_value_check = True
                                        #se la conversione a intero è subito disponibile vado avanti, altrimenti verifico che non ci siano dati in più dopo il valore dei passeggeri
                                        try:
                                            clean_value = int(elem[1])
                                        except ValueError:
                                            #se il primo elemento è un numero non nullo il dato è considerato valido sino all'ultima cifra consecutiva
                                            dirt_value = str(elem[1])
                                            dirt_value = dirt_value.rstrip()
                                            aux = ['1','2','3','4','5','6','7','8','9']
                                            if dirt_value[0] not in aux:
                                                #type non congruo
                                                int_value_check = False
                                            else:
                                                clean_value = ''
                                                for c in dirt_value:
                                                    try:
                                                        c = int(c)
                                                        still_int = True
                                                    except ValueError:
                                                        still_int = False
                                                    if still_int:
                                                        clean_value = clean_value + str(c)
                                                    else:
                                                        break
                                                clean_value = int(clean_value)
                                        #se ho a che fare con un intero verifico che sia positivo e non nullo
                                        #facendo dei calcoli a spanne 333.333.333 è un numero sopra il quale è attualmente impossibile andare
                                        if int_value_check:
                                            if clean_value < 1 or clean_value > 333333:
                                                clean_value = -1
                                            tmp_value = clean_value
                                        tmp_time_series.append(tmp_value)
                                        time_series.append(tmp_time_series)
                    return time_series
            else:
                raise ExamException('ERROR: file non leggibile o inesistente')
        else:
            raise ExamException('ERROR: il file da leggere è None o è una lista')

def existance_years(time_series, years):
    year_in_file = []
    for element in time_series:
        #controllo gli elementi della ts e da ognuno estrapolo l'anno e lo salvo in una lista di soli anni
        element = element[0].split('-')
        tmp_year = element[0]
        year_in_file.append(int(tmp_year))
    #se entrambi gli anni sono nella lista ok    
    if years[0] in year_in_file and years[1] in year_in_file:
        return True
    else:
        return False

def check_years(years):
    #years deve essere una lista di interi, non nulla, formata da 2 anni successivi e di cui possiedo i dati
    if years is None:
        raise ExamException('La lista degli anni è vuota')
    else:
        flag = False
        try:
            years[0] = int(years[0])
            years[1] = int(years[1])
            flag = True
        except ValueError:
            raise ExamException('I parametri forniti non sono di tipo intero')
        if flag:
            #si è optato per prendere per buone anche date ordinate decrescentemente
            years.sort()
            succ = years[0] + 1
            if succ != years[1]:
                raise ExamException('Gli anni forniti non sono consecutivi')
            elif years[0] < 1910:
                raise ExamException('Anno non valido, i primi voli passeggeri risalgono al 1910!')
            else:
                return True
    return False

def check_timeseries(time_series):
    #la timeseries è data dalla funzione get_data() e si presuppone corretta, qualora non fosse però passata essa per parametro si prova a bloccare il parametro con dei controlli stringenti
    if time_series is not None and isinstance(time_series, list):
        for item in time_series:
            if type(item[0]) == str and type(item[1]) == int:
                return True
            else:
                raise ExamException('Formato della timeseries non compatibile')
    else:
        raise ExamException('Timeseries vuota o non è una lista')
    return False

def mv_check(month_value):
    #se nel file dei dati alcune righe mancano o sono errate/incomplete bisogna riempire i mesi dell'anno mancanti (ovv. con valore -1)
    if len(month_value) == 12:
        pass
    else:
        i = 1
        for item in month_value:
            #controllo che il mese i sia l'elemento i
            if item[0] == i:
                pass
            else:
                #inserisco nella lista in posizione i-1 il mese i con valore -1
                month_value.insert(i-1,[i, -1])
            i += 1
    return month_value

def detect_similar_monthly_variations(time_series, years):
    month_value_1 = []
    month_value_2 = []
    if check_timeseries(time_series):
        #controllo che years sia una lista, altrimenti gli altri controlli vengono bucati
        if isinstance(years, list):
            pass
        else:
            raise ExamException('il parametro years non è di tipo lista')
        if len(years) == 2:
            pass
            #numero giusto di elementi
        elif len(years) < 2:
            raise ExamException('Per effettuare un confronto bisogna avere almeno 2 dati a disposizione')
        else:
            years = [yeras[0], years[1]]
            #tentativo di accettare comunque la lista degli anni
        if check_years(years):
            if existance_years(time_series, years):
                first_year = years[0]
                succ_year = years[1]
                for item in time_series:
                    #passaggi per ottenere un intero con l'anno da ['2002-06',21]
                    elem = str(item[0])
                    elem = elem.rstrip().split('-')
                    elem = [int(elem[0]), int(elem[1])]
                    #inserisco il mese e il valore in una lista rappresentante l'anno corretto
                    if elem[0] == first_year:
                        month_value_1.append([elem[1], item[1]])
                    if elem[0] == succ_year:
                        month_value_2.append([elem[1], item[1]])
                
                month_value_1 = mv_check(month_value_1)
                month_value_2 = mv_check(month_value_2)

                #listcomprehension per estrarre solo il valore dei mesi
                value_1 = [v[1] for v in month_value_1]
                value_2 = [v[1] for v in month_value_2]
                ris = []
                #ciclo per calcolare la differenza tra i mesi
                for item in range(11):
                    #se ho valori -1 metto false come da specifiche
                    if value_1[item] == -1 or value_2[item] == -1 or value_1[item+1] == -1 or value_2[item+1] == -1:
                        ris.append(False)
                    else:
                        val_first = abs(value_1[item] - value_1[item+1])
                        val_succ = abs(value_2[item] - value_2[item+1])
                        if val_first < val_succ:
                            val_first, val_succ = val_succ, val_first
                        if val_first - val_succ <= 2:
                            ris.append(True)
                        else:
                            ris.append(False)
                return ris
            else:
                raise ExamException('Gli anni inseriti non sono presenti nella timeseries')
        else:
            raise ExamException('Anni non validi')
    else:
        raise ExamException('Timeseries non valida')