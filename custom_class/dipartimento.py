from custom_class.framework import Framework
from custom_class.db import Db
from custom_class.modello import Modello

class Dipartimento(Framework):
    __dipartimenti = []
    __tablename = 'dipartimenti'
    def __init__(self, fields = {}):
        self.__modelli = []
        super().__init__(fields)

    @classmethod
    def getTable(cls):
        """ Restituisce il nome della tabella del database per i cataloghi """
        return 'dipartimenti'

    @classmethod
    def add(cls, data):  
        """ Metodo di classe che permette di inserire un nuovo oggetto,
            alla lista di tutti gli oggetti di quel tipo"""                    
        idDipartimento = cls.insert(data)
        # restituisco l'oggetto immobile associato all'id appena creato
        return idDipartimento

  
    @classmethod
    def setObjects(cls, data):
        # Metodo di classe che permette di inserire un nuovo oggetto Dipartimento
        # ottengo l'id del catalogo e lo metto nel dizionario di inserimento          
        idDipartimento = cls.insert(data)
        # restituisco l'oggetto immobile associato all'id appena creato
        return idDipartimento


    @classmethod
    def getObjects(cls):
        """ 
        Restituisce la lista di tutti gli oggetti Catalogo inseriti
        """
        # ho bisogno di una connessione e di un cursore per eseguire le operazioni
        conn = Db.getConnection()
        cursor = Db.getCursor()
        # eseguo la query per ottenere tutti gli id degli oggetti di interesse
        query = "SELECT id FROM " + cls.getTable()
        cursor.execute(query)
        # ciclo i risultati ottenuti inserendoli in una lista
        for item in cursor.fetchall():
            cls.__dipartimenti.append(item[0]) # item[0]
        return  cls.__dipartimenti
  
    
    def getNumberModelli(self):

        row = Dipartimento.fetchOne("SELECT COUNT(id) FROM relazioni WHERE dipartimento = ?",(self.get('id'),))
        return row[0]


    def getModelli(self):
        """ Metodo che restituisce la lista dei modelli associata a un dipartimento,
        stampando ogni singolo modello con le sue caratteristiche """
        self.__modelli = []
        # gli immobili del catalogo sono ottenuti tramite database
        rows = Dipartimento.fetchAll("SELECT modello FROM relazioni WHERE dipartimento = ?", (self.get('id'),))
        for item in rows:
            self.__modelli.append(item[0])

    
    def stampaModelli(self):
        self.getModelli()
        if len(self.__modelli):
            print("Nunmero modelli presenti: {0}\n".format(len(self.__modelli)))
            for item in self.__modelli:
                modello = Modello(item)
                print(modello)
        else:
            print("Nessun modello presente nel dipartimento {0}!\n".format(self.get('name')))

    def __str__(self):
        return "------------- Dipartimento -------------\nId: {0}\nNome: {1}\n".format(self.get('id'), self.get('name'))
    
    @classmethod
    def strutturaDB(cls):
        return {'name': 'dipartimenti', 'fields': [{'name':'id','type':'INTEGER','pkey':True, 'nonull': False, 'ai':True}, 
                {'name':'name','type':'char(30)','pkey':False, 'nonull': False, 'ai':False}]}# nome del dipartimento
"""   
    def deleteImmobile(self, immobile):
        if Catalogo.getType() == None:
            print("Tentativo di eliminazione immobile Riferimento: {0} di {1} situato in {2} {3}!\n".format(immobile.get('riferimento'), immobile.get('proprietario'), immobile.get('indirizzo'), immobile.get('citta')))
            if immobile in self._immobili:
                self._immobili.remove(immobile)
                print("Immobile Eliminato!\n")
            else:
                print("Immobile non presente nel catalogo '{0}'!\n".format(self.get('name')))
        elif Catalogo.getType() == 'DB':
            pass
        elif Catalogo.getType() == 'ORM':
            pass    

    def search(self, indirizzo, citta):
        lista = []
        if Catalogo.getType() == None:   
            self.getImmobili()     
            for item in self.__immobili:
                immobile = Immobile(item)
                if immobile.get('indirizzo').lower() == indirizzo.lower() and immobile.get('citta').lower() == citta.lower():
                    lista.append(immobile)      
        elif Catalogo.getType() == 'DB':
            rows = Catalogo.fetchAll("SELECT * FROM cataloghi_rel WHERE catalogo = ?", (self.get('id'),))
            for item in rows:
                immobile = Immobile(item[2])
                if immobile.get('indirizzo').lower() == indirizzo.lower() and immobile.get('citta').lower() == citta.lower():
                    lista.append(immobile)
        elif Catalogo.getType() == 'ORM':
            pass
        else:
            pass
        print("Hai ricercato immobili nel catalogo '{0}' con i seguenti parametri di ricerca:\n\n - Indirizzo: {1} \n - Città: {2}\n".format(self.get('name'),indirizzo,citta))

        if len(lista):
            print("Gli immobili trovati sono: {0}\n".format(len(lista)))
            for immobile in lista:
                print(immobile)
            
        else:
            print("Nessun immobile con i parametri di ricerca forniti!\n")
    """
   
