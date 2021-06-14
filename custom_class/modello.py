import sys
from custom_class.framework import Framework
from custom_class.db import Db

class Modello(Framework):
    """ La classe Modello permette di gestire oggetti di tipo Modello """
    __modelli = [] # lista di tutti i modelli
    def __init__(self, id):
        super().__init__(id)

    @classmethod
    def getTable(cls):
        """ Restituisce il nome della tabella del database per i cataloghi """
        return 'modelli'       

    @classmethod
    def getObjects(cls):
        """ 
        Restituisce la lista di tutti gli oggetti salvati.
        """
        # ho bisogno di una connessione e di un cursore per eseguire le operazioni
        conn = Db.getConnection()
        cursor = Db.getCursor()
        # eseguo la query per ottenere tutti gli id degli oggetti di interesse
        query = "SELECT id FROM " + cls.getTable()
        cursor.execute(query)
        # ciclo i risultati ottenuti inserendoli in una lista
        for item in cursor.fetchall():
            cls.__modelli.append(item[0])
        return  cls.__modelli
    
    @classmethod
    def add(cls, data):
        """ 
        Metodo di classe che permette di inserire un nuovo oggetto Modello
        """
        idModello = cls.insert(data)
        modello = Modello(idModello)
        # inserisco la relazione tra catalogo e immobile
        from custom_class.relazione import Relazione 
        Relazione.insert({'dipartimento' : modello.get('dipartimento'), 'modello' : modello.get('id')})
    
    def delete(self):
        conn = Db.getConnection()
        cursor = Db.getCursor()
        query = "DELETE FROM " + self.__class__.getTable() + " WHERE id = ?"
        cursor.execute(query, (self.get('id'),))
        from custom_class.relazione import Relazione 
        query = "DELETE FROM " + Relazione.getTable() + " WHERE modello = ?"
        cursor.execute(query, (self.get('id'),))
        conn.commit()
        print("Modello {0} eliminato!\n".format(self.get('name')))
        indice = self.__modelli.index(self.get('id'))          
        if indice:
            self.__modelli.remove(self.get('id'))
 
    @classmethod
    def search(cls,data):
        """
        Metodo di classe per la ricerca di un modello
        """
        conn = Db.getConnection()
        cursor = Db.getCursor()
        fields = separatore = ""
        # ciclo i le chiavi del dizionario data per ottenere 
        # i campi da modificare
        for chiave, valore in data.items():
            fields += separatore + " LOWER(" + chiave + ") = '" + str(valore.lower()) + "'"         
            separatore = " AND "   
        # eseguo la query
        query = "SELECT id FROM " + cls.getTable() + " WHERE " + fields
        cursor.execute(query) #data
        lista = []
        for item in cursor.fetchall():
            lista.append(item[0])
        
        print("Paramenti di ricerca:\n")
        for chiave, valore in data.items():
            print(" - {0} -> {1}\n".format(chiave,valore))
        
        if len(lista):
            
            print("Modelli trovati {0}:\n".format(len(lista)))
            for item in lista:
                modello = Modello(item)
                print(modello)
        else:
            print("Nessun modello trovato per i parametri passati!\n")


    def __str__(self):
        return "------------- Stampa Modello -------------\nId: {0}\nNome: {1}\nDescrizione: {2} \n".format(self.get('id'), self.get('name'),self.get('descrizione'))

    @classmethod
    def strutturaDB(cls):
        return {'name': 'modelli', 'fields': [{'name':'id','type':'INTEGER','pkey':True, 'nonull': False, 'ai':True},
                {'name':'name','type':'char(30)','pkey':False, 'nonull': False, 'ai':False},
                {'name':'descrizione','type':'char(100)','pkey':False, 'nonull': False, 'ai':False},
                {'name':'dipartimento','type':'INTEGER','pkey':False, 'nonull': False, 'ai':False}]}