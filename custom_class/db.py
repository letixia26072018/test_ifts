
import sqlite3

class Db():

    # variabile che identifica la connessione
    conn = False

    @staticmethod
    def getCursor():
        """ Metodo che restituisce il cursore dopo la connessione """
        return __class__.conn.cursor()

    @staticmethod
    def getConnection():
        """ Metodo per effettuare la connessione al database """
        __class__.conn = sqlite3.connect("agenzia.db")
        # utilizzo la seguente riga per 
        __class__.conn.row_factory = sqlite3.Row
        # se la connessione è andata a buon fine la restiuisco
        # altrimenti lancio un'eccezione
        if __class__.conn:
            return __class__.conn
        else:
            raise ValueError("Connessione al DB non presente")

    @staticmethod
    def close():
        __class__.conn.close()

    @staticmethod
    def createTable(campi): 
        conn = Db.getConnection()        
        cursor = Db.getCursor()       
        tableName = campi['name']
        fields = ""
        separatore = ""
        for item in campi['fields']:
            if item != None:
                fields += separatore + item['name']+ " " + item['type']
                if item['pkey']:
                    fields += " PRIMARY KEY"
                if item['nonull']:
                    fields += " NOT NULL"  
                if item['ai']:
                    fields += " AUTOINCREMENT"
                separatore = ", "     
        query = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(tableName,fields)
        cursor.execute(query)

    @staticmethod
    def deleteTable(table):
        conn = Db.getConnection()        
        cursor = Db.getCursor()   
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table + "'")
        #se il conteggio è 1 la tabella esiste e posso eliminarla
        if int(cursor.fetchone()[0]) == 1: 
            cursor.execute("DROP table " + table) 
            conn.commit()
        else:
            print("La tabella '" + table + "' non esiste!")
        
    @staticmethod
    def truncateTable(table):
        conn = Db.getConnection()        
        cursor = Db.getCursor()   
        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + table + "'")
        #se il conteggio è 1 la tabella esiste e posso eliminarla
        if int(cursor.fetchone()[0]) == 1: 
            cursor.execute("DELETE FROM " + table) 
            conn.commit()
        else:
            print("La tabella '" + table + "' non esiste!")  

    @staticmethod
    def showTables():
        conn = Db.getConnection()        
        cursor = Db.getCursor()   
        cursor.execute("""SELECT name FROM sqlite_master  
                          WHERE type='table';""")
        for item in [v[0] for v in cursor.fetchall() if v[0] != "sqlite_sequence"]:
            print(item)

    @staticmethod
    def describeTables(table):
        conn = Db.getConnection()        
        cursor = Db.getCursor()   
        cursor.execute("SELECT * FROM " + table)
        col_name_list = [tuple[0] for tuple in cursor.description]
        print(col_name_list)





