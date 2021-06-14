import sys
from sqlite3.dbapi2 import DatabaseError
from custom_class.db import Db
import peewee

class Framework(): 
    """ 
    Framework è una superclasse in cui ho inserito tutte le più importanti operazioni generiche collegate ad un oggetto.
    Tutte gli altri oggetti erediteranno da questa classe implementando, eventualmente, le customizzazioni ove necessario.
    I dati degli oggetti vengono sempre gestiti tramite un dizionario in modo di non dover creare una variabile per ogni dato.
    Per ottenere il valore di ogni chiave del dizionario, o meglio, per ottenere uno specifio dato associato all'oggetto,
    ho realizzato un metodo getter chiamato get(key), che restituisce il valore della chiave del dizionario passata come parametro. 
    Allo stesso modo per impostare i valori del dizionario e di conseguenza modificare il dato dell'oggetto ho realizzato un metodo setter chiamato
    set(key,value) che imposta la chiave passata come argomento al valore passato come argomento.

    __data è il dizionario utilizzato per la gestione dei dati degli oggetti
    __tablename è il nome della tabella sul database 
    id è l'id dell'oggetto sul database
    """
    __data = {}  # dizionario dei dati degli oggetti
    __tablename = False # nome della tabella sul database, impostata direttamente nelle classi che ereditano
    __modelli = [] # lista dei modelli
    __dipartimenti = [] #lista dei dipartimenti
    
    def __init__(self, id = None): 
        # utilizzo sempre il dizionario come base per restituire i dati dell'oggetto    
        self.__data['id'] = id  
        self.useDb() # ho diviso il recupero dei dati dell'oggetto per maggiore chiarezza

    def setData(self, fields = {}):
        """ Aggiorna i dati del dizionario """
        self.__data.update(fields)

    def getData(self):
        """ Restituisce i dati dell'oggetto salvati tramite dizionario """
        return self.__data      

    @classmethod
    def fetchOne(cls, query, args = None):
        """ 
        Il metodo permette di effettuare chiamate al database nel caso in cui si voglia 
        che venga restituito un solo record 
        - query: la query da eseguire 
        - args: la tupla con i parametri della query 
        """
        conn = Db.getConnection()        
        cursor = Db.getCursor()
        if args != None:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        return cursor.fetchone()

    @classmethod
    def fetchAll(cls, query, args = None):
        """ 
        Il metodo permette di effettuare chiamate al database nel caso in cui si voglia 
        che venga restituito un insieme di record 
        - query: la query da eseguire 
        - args: la tupla con i parametri della query 
        """
        conn = Db.getConnection()        
        cursor = Db.getCursor()
        if args != None:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def useDb(self):
        try:
            # ho bisogno di una connessione e di un cursore per eseguire le operazioni
            conn = Db.getConnection()        
            cursor = Db.getCursor()
            # compongo la query per istanziare l'oggetto e ottenere tutte le sue caratteristiche
            self.query = "SELECT * FROM " + self.__class__.getTable() + " WHERE id = ?"
            # eseguo la query
            cursor.execute(self.query, (self.__data['id'],))
            # ottengo i dati del record del database 
            row = cursor.fetchone()
            # trasformo l'oggetto restiuito in un dizionario
            if row:
                self.__data = dict(zip([c[0] for c in cursor.description], row))
            else:
                raise ValueError("ATTENZIONE: ID {0} non associato a nessun '{1}'!".format(self.__data['id'],self.__class__.__name__))
        except ConnectionError as err:
            print(err)        
    
    def get(self,key):
        """
        Permette di ottenere i dati associati all'oggetto salvati nel dizionario.
        Se la chiave che cerco è presente nel dizionario dei dati dell'oggetto
        restituisco il suo valore altrimenti se non esiste lancio un'eccezione
        """
        if key in self.__data:
            return self.__data[key]
        else:
            raise NameError("Il dato '{0}' cercato non esiste!\n".format(key))

    def set(self,key,value):
        """
        Permette di impostare, quindi modificare, i dati associati all'oggetto salvati nel dizionario.
        Se la chiave che cerco è presente nel dizionario dei dati dell'oggetto
        imposto il suo valore altrimenti se non esiste lancio un'eccezione
        """
        if key in self.__data:
            self.__data[key] = value
            self.edit(self.__data)
        else:
            raise NameError("Il dato cercato non esiste!")

    @classmethod
    def insert(cls, data):
        """
        E' il metodo associato alla classe che lo chiama che si preoccupa di fare gli inserimenti nel Database.
        Viene composta in primis la query a seconda dei paramentri passati dopo di che avviene la connessione al 
        database e l'esecuzione della query. Restiuisce l'id del record inserito.
        Posso passare al metodo o una lista di dizionari con chiave:valore a seconda del dato che voglio inserire  
        items = [{'dato1':'valore1','dato2':valore1},{'dato1':'valore2', 'dato2': valore2},{'dato1':'valore3','dato2':valore3}, ..........]
        oppure posso passare anche un singolo dizionario se voglio inserire un unico record
        item = {'dato1':'valore','dato2':valore, .........}
        Per inserire utilizzola seguente sintassi:
        classe.insert(item)
        dove classe è il nome della classe dell'oggetto che voglio inserire
        """
        # ho bisono di una connessione e di un cursore per eseguire le operazioni
        conn = Db.getConnection()
        cursor = Db.getCursor()
        keys = values = separatore = fields = ""
        # ciclo i le chiavi e i valori del dizionario data per ottenere 
        # i campi da inserire nel db e i valori associati
        for chiave, item in data.items():
            fields += separatore + ":" + chiave 
            keys += separatore + chiave
            values += separatore + "'" + str(item) + "'"              
            separatore = ", " 
        # eseguo la query 
        query = "INSERT INTO " +  cls.getTable() + " (" + keys + ") VALUES (" + values + ")"
        cursor.execute(query) 
        # salvo i dati
        conn.commit()
        #restituico l'id appena inserito
        return cursor.lastrowid


    def edit(self, data):
        """
        data è un dizionario le cui chiavi vengono utilizzate per indicare i campi da modificare e
        viene passato direttamente alla funzione execute
        obj.edit(data)
        """
        # ottengo una connessione e di un cursore per eseguire le operazioni
        conn = Db.getConnection()
        cursor = Db.getCursor()
        fields = separatore = ""
        # ciclo i le chiavi del dizionario data per ottenere 
        # i campi da modificare
        id = data['id']
        for chiave, valore in data.items():
            if chiave !='id':
                fields += separatore +  chiave + " = '" + str(valore) + "'"         
                separatore = ", "   
        # eseguo la query
        query = "UPDATE " + self.__class__.getTable() + " SET " + fields + " WHERE id = " + str(id) + " LIMIT 1"
        cursor.execute(query) #data
        # salvo i dati
        conn.commit()

    @classmethod
    def getTable(cls):
        """ Restituisce il nome della tabella del database dell'oggetto/classe """
        return cls.__tablename

    @classmethod
    def setTable(cls, tabella):
        """ Imposta il nome della tabella del database dell'oggetto/classe """
        cls.__tablename = tabella

    def stampa(self):
        """ 
        Metodo per stampare i dati di un oggetto.
        Posso usare il print(self) perchè ho riscritto nelle singole classi
        che ereditano da Framework il metodo speciale - attributo  __str__ in modo da 
        stampare direttamente l'oggetto 
        """
        if self:
            print(self)
        else:
            print(self)
            raise ValueError("ATTENZIONE: il valore '{0}' non è un'istanza valida di oggetto!".format(self))
    
    @classmethod
    def stampaTutti(cls):
        """ 
        Metodo per stampare tutti i dati di un oggetto identificato tramite la propria classe 
        """
        for item in cls.getObjects(): 
            obj = cls(item)
            print(obj)
 
 



   


