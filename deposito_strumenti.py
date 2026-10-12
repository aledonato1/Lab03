from operator import attrgetter


class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return f"{self.id_strumento} - {self.tipo} {self.marca} (Anno: {self.anno_acquisto}, Valore: {self.valore}€)"


class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"[{self.id_prestito}] Strumento {self.id_strumento} in prestito a {self.cognome_allievo} dal {self.data}"


class DepositoStrumenti:
    def __init__(self, nome, responsabile):

        self.nome = nome
        self._responsabile = responsabile
        self.strumenti = {}  # Dizionario: ID strumento -> Oggetto Strumento
        self.prestiti = {}  # Dizionario: ID prestito -> Oggetto Prestito

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                for riga in file:
                    riga = riga.strip()
                    if not riga:
                        continue
                    campi = riga.split(',')
                    if len(campi) == 5:
                        id_str = campi[0].strip()
                        tipo = campi[1].strip()
                        marca = campi[2].strip()
                        anno = int(campi[3].strip())
                        valore = float(campi[4].strip())

                        strumento = Strumento(id_str, tipo, marca, anno, valore)
                        self.strumenti[id_str] = strumento
        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: il file '{file_path}' non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):

        max_id = 0
        for id_str in self.strumenti.keys():
            try:
                num = int(id_str[1:])
                if num > max_id:
                    max_id = num
            except ValueError:
                pass

        nuovo_id = f"S{max_id + 1}"
        nuovo_strumento = Strumento(nuovo_id, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_id] = nuovo_strumento
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):

        lista_strumenti = []
        for strumento in self.strumenti.values():
            lista_strumenti.append(strumento)

        lista_strumenti.sort(key=attrgetter('marca'))
        return lista_strumenti

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception(f"Errore: lo strumento {id_strumento} non è presente nel deposito.")

        for prestito in self.prestiti.values():
            if prestito.id_strumento == id_strumento:
                raise Exception(f"Errore: lo strumento {id_strumento} è già in prestito.")

        max_id = 0
        for id_prestito in self.prestiti.keys():
            try:
                num = int(id_prestito[1:])
                if num > max_id:
                    max_id = num
            except ValueError:
                pass

        nuovo_id = f"P{max_id + 1}"
        nuovo_prestito = Prestito(nuovo_id, data, id_strumento, cognome_allievo)
        self.prestiti[nuovo_id] = nuovo_prestito
        return nuovo_prestito

    def termina_prestito(self, id_prestito):

        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: nessun prestito in corso trovato con ID '{id_prestito}'.")

        del self.prestiti[id_prestito]