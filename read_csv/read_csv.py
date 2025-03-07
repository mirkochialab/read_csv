# -*- coding: utf-8 -*-
""" 
Created on 2025/03/04 10:43:31
@author: Mirko
"""
import os
import pandas as pd
from pathlib import Path
import json


clienti_path = r"G:\Il mio Drive\FILE UTILI\_PYTHON\ivapy"
import sys
sys.path.insert(1, clienti_path)
from _clienti import Cliente # type: ignore





# Lista costante contenente i tipo di documenti 
class DOCS_TYPES:
    FTE_EMESSE = 'FTE_EMESSE'
    FTE_RICEVUTE = 'FTE_RICEVUTE'
    FTE_MESSE_A_DISPOSIZIONE = 'FTE_MESSE_A_DISPOSIZIONE'
    CORRISPETTIVI = 'CORRISPETTIVI'

    @classmethod
    def as_list(cls):
        """Restituisce tutti i tipi come lista"""
        return [
            cls.FTE_EMESSE,
            cls.FTE_RICEVUTE,
            cls.FTE_MESSE_A_DISPOSIZIONE,
            cls.CORRISPETTIVI
        ]


class ReadCSV:
    def __init__(self, 
                 cliente,
                 anno_iva,
                 mese_iva
                 
                 ):

        # Parametri cliente
        self.cliente = cliente
        
        # Parametri IVA
        self.anno_iva = anno_iva
        self.mese_iva = mese_iva
        self.dt_chiusura_iva = pd.to_datetime(f'{anno_iva}-{mese_iva}-01').to_period('M').end_time



        # Parametri file CSV 
        self.lettera_gdrive = "G"
        self.path_gdrive = os.path.join(self.lettera_gdrive + ":\\", "Il mio Drive")
        self.path_cliente = os.path.join(self.path_gdrive, "CLIENTI", self.cliente['folder_name'])
        self.path_folder_iva = os.path.join(self.path_cliente, "IVA", str(self.anno_iva))
        

        

    def _get_csv_path(self, doc_type, quarter):

        # Costruisce il nome del file
        filename = f"{doc_type}__{self.cliente['folder_name']}__{quarter}.csv"
        # Costruisce il percorso completo
        # full_path = os.path.join(self.path_folder_iva, doc_type, 'csv', filename)
        return filename


    def load_csv(self, doc_type):
        
        '''FAI LE COSE SEMPLICI'''
        
        path_folder_csv = os.path.join(self.path_folder_iva,
                                       doc_type,
                                       'csv')
        
        
        # Ottieni la lista di tutti i file CSV nella cartella
        files_csv = [f for f in os.listdir(path_folder_csv) if f.endswith('.csv')]
        
        # Itera i file CSV
        for file in files_csv:

            # Percorso completo del file CSV
            path_file_csv = os.path.join(path_folder_csv, file)

            # Utilizzo della funzione Path per le statistiche sul file CSV
            file_csv_stat = Path(path_file_csv).stat()
            dt_create_csv = pd.to_datetime(file_csv_stat.st_ctime_ns)
            
            # ### Controllo di coerenza sui file 
            # Ricavo le date di competenza di ogni singolo file CSV dal nome
            date_from_csv_filename = file.replace('.csv','').split("__")[2]
            dt_csv_quarter_ini = pd.to_datetime(date_from_csv_filename)
            dt_csv_quarter_end = dt_csv_quarter_ini.to_period('Q').end_time
            
            print(file)
            print("-->", "Data creazione file:", dt_create_csv)
            print("-->", "Data inizio periodo:", dt_csv_quarter_ini)
            print("-->", "Data fine   periodo:", dt_csv_quarter_end)
            print("-->", "Data chiusura IVA  :", self.dt_chiusura_iva)
            
            # # Segnala file non aggiornato con errore
            file_deprecated = False
            
            # Caso 1 (data di chiusura inferiore a fine trimestre)
            if self.dt_chiusura_iva <= dt_csv_quarter_end:
                # Se la data del file è inferiore della chiusura è deprecato
                if dt_create_csv <= self.dt_chiusura_iva:
                    file_deprecated = True
                
                # Crea ALERT offsettando di 5 giorni
                if dt_create_csv <= (self.dt_chiusura_iva.floor('ms') + pd.DateOffset(days=5)):
                    print("offset")
                
            # Caso 2 (data di chiusura superiore a fine trimestre)
            if self.dt_chiusura_iva >= dt_create_csv:
                # Se la data del file è inferiore alla fine del quarter è deprecato
                if dt_create_csv <= dt_csv_quarter_end:
                    file_deprecated = True
                
                
                # Crea alert offsettando di 5 giorni
                if dt_create_csv <= (dt_csv_quarter_end.floor('ms') + pd.DateOffset(days=5)):
                    print("offset")
                
            # Se il file è deprecato vai in errore
            if file_deprecated:
                raise("ATTENZIONE! il file:", file, "è troppo vecchio!")
            else:
                print("-->", 'Data file coerente!')

        


cliente_selected = Cliente.mongelli_giacinta

rc = ReadCSV(cliente_selected, 2025, 2)

data = rc.load_csv(DOCS_TYPES.FTE_EMESSE)

data = rc.load_csv(DOCS_TYPES.FTE_RICEVUTE)