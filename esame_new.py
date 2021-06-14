import sys
from os import error
from custom_class.db import Db
from custom_class.dipartimento import Dipartimento
from custom_class.modello import Modello
from custom_class.relazione import Relazione
from random import randint

print("################ UTILIZZO DB SQLITE3 ###################\n")
# Imposto il salvataggio dei dati tramite Database Sqlite3
############################################################################################################
##### NELLA PRIMA PARTE ELIMINO LE TABELLE DEL DB E LE RICOSTRUISCO PER NON AVERE UN DB TROPPO PESANTE #####
############################################################################################################
##### Per creare la tabelle utilizzo un dizionario con il nome della tabella, campo 'name' e la lista  #####
##### dei campi che voglio inserire nella tabella, campo 'fields'. Inserisco una chiave primaria       #####
##### chiamata 'id', auto incrementante che mi servirà per istanziare gli oggetti da database          #####
#####                                                                                                  #####
##### Sono presenti 2 campi relativi all'oggetto 'Dipartimento                                         #####
#####   - id: chiave promaria autoincrementante                                                        #####
#####   - name: il nome del catalogo                                                                   #####
#####                                                                                                  #####
##### Sono prensenti 4 campi relativi all'oggetto 'Modello':                                           #####
#####   - id: chiave promaria autoincrementante                                                        #####
#####   - name: il nome del modello                                                                    #####
#####   - descrizione: la descrizione del modello                                                      #####
#####   - dipartimento: l'id del dipartimento di appartenenza                                          #####
#####                                                                                                  #####
##### Sono presenti 3 campi relativi alla relazione tra catalogo e immobile:                           #####
#####   - id: chiave promaria autoincrementante                                                        #####
#####   - dipartimento: l'id del dipartimento di appartenenza                                          #####
#####   - modello: l'id del modello associato al dipartimento                                          #####
#####                                                                                                  #####                   
############################################################################################################
############################################################################################################

# ELIMINO LA TABELLA dipartimenti, modelli e relazioni, SE ESISTONO E LE CREO NUOVAMENTE
# nel metodo strutturaDB delle rispettive classi è presente il dizionario utilizzato per creare le tabelle
Db.deleteTable(Dipartimento.getTable())
Db.createTable(Dipartimento.strutturaDB())
Db.deleteTable(Modello.getTable())
Db.createTable(Modello.strutturaDB())
Db.deleteTable(Relazione.getTable())
Db.createTable(Relazione.strutturaDB())

########################################################################
################## INSERIMENTO DEI DIPARTIMENTI NEL DB   ##################
################## DOPO L'INSERIMENTO INSTANZIO TUTTI ################## 
################## GLI OGGETTI DIPARTIMENTO CREATI        ##################
########################################################################
dipartimenti = [{"name":"Dipartimento 1"},
             {"name":"Dipartimento 2"},
             {"name":"Dipartimento 3"},
             {"name":"Dipartimento 4"}]

for item in dipartimenti:
    # utilizzo il metodo add della classe Catalogo per inserire i cataloghi nel database
    Dipartimento.add(item)

print("######################### STAMPA DIPARTIMENTI PRESENTI #############################:\n")
Dipartimento.stampaTutti()
print("######################### FINE STAMPA DIPARTIMENTI PRESENTI ########################:\n")
# ISTANZIO GLI OGGETTI 'Catalogo' 
try:
    dip1 = Dipartimento(1)
    dip2 = Dipartimento(2)
    dip3 = Dipartimento(3)
    dip4 = Dipartimento(4)
except ValueError as err:
    print(err)
except Exception as err:
    print(err)

#############################################################################
################## INSERIMENTO DEI MODELLI NEL DB            ##################
################## DOPO L'INSERIMENTO INSTANZIO TUTTI      ################## 
################## GLI OGGETTI MODELLO CREATI              ##################
#############################################################################
modelli = []

for item in range(1,11):
    modello = {'name': 'Modello ' + str(item), 'descrizione': 'Descrizione modello ' +str(item), 'dipartimento': randint(1, 4) }
    modelli.append(modello)

for item in modelli:
    Modello.add(item)

# ISTANZIO GLI OGGETTI 'Modello'
try:
    mod1 = Modello(1)
    mod2 = Modello(2)
    mod3 = Modello(3)
    mod4 = Modello(4)
    mod5 = Modello(5)
    mod6 = Modello(6)
    mod7 = Modello(7)
    mod8 = Modello(8)
    mod9 = Modello(9)
    mod10 = Modello(10)
except ValueError as err:
    print(err)
except Exception as err:
    print(err)

print("######################### TEST STAMPA DATI ASSOCIATO AD UN OGGETTO MODELLO #############################:\n")
try:
    print("IL NOME DELl'OGGETTO MODELLO mod1 è {0}\n".format(mod1.get('name')))
    print("LA DESCRIZIONE DELl'OGGETTO MODELLO mod1 è {0}\n".format(mod1.get('descrizione')))
    print("VERIFICO UNA CARATTERISTICA DELL'OGGETTO MODELLO mod1 che non esiste: {0}".format('DatoNonPresente!'))
    mod1.get("DatoNonPresente!")
except NameError as err:
    print(err)
except Exception as err:
    print(err)
# STAMPA I MODELLI PRESENTI NEL DB
print("######################### STAMPA MODELLI PRESENTI #############################:\n")
Modello.stampaTutti()
print("######################### FINE STAMPA MODELLI PRESENTI ########################:\n")

print("####### STAMPA MODELLI DIPARTIMENTO '{0}' ########\n".format(dip1.get('name')))
dip1.stampaModelli()
print("####### STAMPA MODELLI DIPARTIMENTO '{0}' ########\n".format(dip2.get('name')))
dip2.stampaModelli()
print("####### STAMPA MODELLI DIPARTIMENTO '{0}' ########\n".format(dip3.get('name')))
dip3.stampaModelli()
print("####### STAMPA MODELLI DIPARTIMENTO '{0}' ########\n".format(dip4.get('name')))
dip4.stampaModelli()

# MODIFICO IL PREZZO DELL'IMMOBILE
print("####### MODIFICA NOME MODELLO E STAMPA MODELLO MODIFICATO #########:\n")
# STAMPO I VECCHI VALORI DEL MODELLO
mod1.stampa()
print("Vecchio nome immobile: {0}".format(mod1.get('name')))
nuovoNome = "MODELLO 1 CON NOME MODIFICATO"
print("Nuovo nome modello: {0}\n".format(nuovoNome))
mod1.set('name',nuovoNome)
# STAMPO I NUOVI VALORI DEL MODELLO
mod1.stampa()

# MODIFICO IL PREZZO DELL'IMMOBILE
print("####### MODIFICA DESCERIZIONE MODELLO E STAMPA MODELLO MODIFICATO #########:\n")
# STAMPO I VECCHI VALORI DEL MODELLO
print("Vecchio nome immobile: {0}".format(mod1.get('descrizione')))
nuovaDescrizione = "MODELLO 1 CON DESCRIZIONE MODIFICATA"
print("Nuova descrizione modello: {0}\n".format(nuovaDescrizione))
mod1.set('descrizione',nuovaDescrizione)
# STAMPO I NUOVI VALORI DEL MODELLO
mod1.stampa()

print("####### INIZIO SEZIONE RICERCA  ########\n")
# PROVO AD EFFETTUARE UNA RICERCA PER NOME DEL MODELLO
print("####### TEST RICERCA MODELLO PER NOME ########\n")
Modello.search({'name': 'Modello 2'})

# PROVO AD EFFETTUARE UNA RICERCA PER DESCRIZIONE DEL MODELLO
print("####### TEST RICERCA MODELLO PER DESCRIZIONE ########\n")
Modello.search({'descrizione': 'Descrizione modello 3'})

# PROVO AD EFFETTUARE UNA RICERCA PER NOME E DESCRIZIONE DEL MODELLO
print("####### TEST RICERCA MODELLO PER NOME E DESCRIZIONE ########\n")
Modello.search({'name' :'Modello 3', 'descrizione': 'Descrizione modello 3'})

# PROVO AD EFFETTUARE UNA RICERCA PER NOME DEL MODELLO
print("####### TEST RICERCA MODELLO PER NOME SENZA RISULTATI ########\n")
Modello.search({'name': 'Modello non esistente'})

# PROVO AD EFFETTUARE UNA RICERCA PER DESCRIZIONE DEL MODELLO
print("####### TEST RICERCA MODELLO PER DESCRIZIONE SENZA RISULTATI ########\n")
Modello.search({'descrizione': 'Descrizione modello non esistente'})

# PROVO AD EFFETTUARE UNA RICERCA PER NOME E DESCRIZIONE DEL MODELLO
print("####### TEST RICERCA MODELLO PER NOME E DESCRIZIONE  SENZA RISULTATI  ########\n")
Modello.search({'name' :'Modello non esistente', 'descrizione': 'Descrizione modello non esistente'})
print("####### FINE SEZIONE RICERCA  ########\n")

# ELIMINO UN IMMOBILE DAL CATALOGO CASA VACANZA
# Per eliminare un modello devo eliminarlo dalla tabella modelli e devo
# eliminare anche la relazione con il dipartimento di appartenenza 

print("############### TEST ELIMINAZIONE MODELLO #############\n")
mod5.delete()
print("############### STAMPA MODELLI PER VERIFICARE L'ELIMINAZIONE APPENA AVVENUTA #############\n")
Modello.stampaTutti()
print("################################################################")
print("######################## FINE PROGRAMMA ########################")
sys.exit("################################################################")


