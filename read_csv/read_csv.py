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
    def __init__(self, anno_iva, cliente):

        self.anno_iva = anno_iva
        self.cliente = cliente





        # path file
        self.lettera_gdrive = "G"
        self.path_gdrive = os.path.join(self.lettera_gdrive + ":\\", "Il mio Drive")
        self.path_cliente = os.path.join(self.path_gdrive, "CLIENTI", self.cliente['folder_name'])
        self.path_folder_iva = os.path.join(self.path_cliente, "IVA", str(self.anno_iva))
        

        print(self.path_folder_iva)

    def _get_csv_path(self, doc_type, quarter):

        # Costruisce il nome del file
        filename = f"{doc_type}__{self.cliente['folder_name']}__{quarter}.csv"
        # Costruisce il percorso completo
        full_path = os.path.join(self.path_folder_iva, doc_type, 'csv', filename)
        return filename


    def load_csv(self, doc_type):
        '''
        I file csv sono salvati nella cartella del cliente selezionato
        nella specifica cartella relativamente all'anno iva selezionato
        e suddivisi in ulteriori cartelle per tipo di documento:
        - FTE_EMESSE
        - FTE_RICEVUTE
        - CORRISPETTIVI
        - FTE_MESSE_A_DISPOSIZIONE
        
        '''

        obj = {
            'pathfolder_iva':
            }

        quarters  = pd.date_range(start=f'{self.anno_iva}-01-01', 
                                  end=f'{self.anno_iva}-12-31', 
                                  freq='QS')

        for i, q in enumerate(quarters):
            
            csv_filename = self._get_csv_path(doc_type, q.strftime('%Y-%m-%d'))
            
            csv_full_path = os.path.join(self.path_folder_iva, 
                                         doc_type, 
                                         'csv', 
                                         csv_filename)
            
            file_csv = Path(csv_full_path)
            
            file_csv_datetime_create = None
            
            file_check_update = None
            
            
            if file_csv.exists():

                stat = file_csv.stat()
                
                file_csv_datetime_create = pd.to_datetime(stat.st_ctime_ns).isoformat()
                
                # TODO CHECK FILE CREATO CON DATA COERENTE AL AI DATI CONTENUTI
            
            obj.update({f'{self.anno_iva}-Q{i+1}': {
                'csv_filename': csv_filename,
                'date_create': file_csv_datetime_create 
                }
                
                })
 
        print(json.dumps(obj, indent=4))           

        return  obj
        


cliente_selected = Cliente.mongelli_giacinta

rc = ReadCSV(2025, cliente_selected)

data = rc.load_csv(DOCS_TYPES.FTE_EMESSE)