from custom_class.framework import Framework
from custom_class.db import Db

class Relazione(Framework):
    _tablename = 'relazioni'
    def __init__(self, id):
        super().__init__(id)
    
    @classmethod
    def getTable(cls):
        """ Restituisce il nome della tabella del database per i cataloghi """
        return 'relazioni'

    @classmethod
    def strutturaDB(cls):
        return {'name': 'relazioni', 'fields': [{'name':'id','type':'INTEGER','pkey':True, 'nonull': False, 'ai':True}, 
                {'name':'dipartimento','type':'INTEGER','pkey':False, 'nonull': False, 'ai':False}, 
                {'name':'modello','type':'INTEGER','pkey':False, 'nonull': False, 'ai':False}]}