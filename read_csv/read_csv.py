# -*- coding: utf-8 -*-
""" 
Created on 2025/03/04 10:43:31
@author: Mirko
"""
import os

clienti_path = r"G:\Il mio Drive\FILE UTILI\_PYTHON\ivapy"
import sys
sys.path.insert(1, clienti_path)
from _clienti import Cliente # type: ignore



# Lista costante contenente i tipo di documenti 
DOCS_TYPE = [
    'FTE_EMESSE',
    'CORRISPETTIVI'
    ]

class ReadCSV:
    def __init__(self, anno_iva, cliente_selected):

        self.anno_iva = anno_iva
        self.cliente_selected = cliente_selected





        # path file
        self.lettera_gdrive = "G"
        self.path_gdrive = os.path.join(self.lettera_gdrive + ":\\", "Il mio Drive")
        self.path_client = os.path.join(self.path_gdrive, "CLIENTI", self.cliente_selected['folder_name'])
        self.path_folder_iva = os.path.join(self.path_client, "IVA", str(self.anno_iva))
        

        print(self.path_folder_iva)


    def load_csv(self):
        '''
        I file csv sono salvati nella cartella del cliente selezionato
        nella specifica cartella relativamente all'anno iva selezionato
        e suddivisi in ulteriori cartelle per tipo di documento:
        - FTE_ACQUISTO
        - FTE_VENDITA
        - CORRISPETTIVI
        - FTE_MESSE_A_DISPOSIZIONE
        

        '''

        pass


cliente_selected = Cliente.mongelli_giacinta

rc = ReadCSV(2024, cliente_selected)
