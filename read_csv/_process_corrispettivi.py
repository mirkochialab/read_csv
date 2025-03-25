# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 17:32:01 2025

@author: Mirko
"""
import os
import pandas as pd
from constant import DOCS_TYPES


def process_corrispettivi(self, 
                          doc_type=DOCS_TYPES.CORRISPETTIVI, 
                          path_folder_csv=None):
    
    # Se non viene fornito un path, utilizza quello di default
    if path_folder_csv == None:
        # Path default csv
        path_folder_csv = os.path.join(self.path_folder_iva, doc_type, 'csv')
    
    # Carica il file csv dell'Ade
    df = self._load_csv(doc_type, path_folder_csv)
       
    # Linea
    print()
    print()
    print("📟", doc_type.ljust(100, '-'))
    
    if not df.empty:
        # Controlla e segnala eventuali dati duplicati prima dell'eliminazione
        duplicates = df[df.duplicated(subset=['Id invio'], keep=False)]
        if not duplicates.empty:
            print(f"ATTENZIONE: trovati {duplicates.shape[0]} record duplicati che verranno rimossi.")

        # Rimuovi i dati duplicati
        df.drop_duplicates(subset=['Id invio'], keep='first', inplace=True)

        # Nuovo controllo post-eliminazione
        duplicates_post = df[df.duplicated(subset=['Id invio'], keep=False)]
        if duplicates_post.empty:
            print("Nessun record duplicato trovato dopo la pulizia.")

        
        # Ordina per Data emissione (già datetime)
        df.sort_values('Data e ora rilevazione', inplace=True)

        
        # ### Raggruppa i dati per MESE
        df_mth_sum = df[['Imponibile', 'IVA', 'TOTALE', 'Data e ora rilevazione']].groupby(
            pd.Grouper(key='Data e ora rilevazione', freq='ME')).sum().reset_index()

        # Crea un dataframe con i dati cumulati 
        df_mth_cumsum = df_mth_sum.copy()
        df_mth_cumsum[['Imponibile', 'IVA', 'TOTALE']] = df_mth_cumsum[['Imponibile', 'IVA', 'TOTALE']].cumsum()
        
        # Aggiungi una colonnna ricavando imponibile dall'importo IVA per le fatture con importi esenti
        df_mth_cumsum['imp_fiva_22'] = df_mth_cumsum['IVA'] / .22


        
        # ### Raggruppa i dati per ANNO
        df_year_sum = df[['Imponibile', 'IVA', 'TOTALE', 'Data e ora rilevazione']].groupby(
            pd.Grouper(key='Data e ora rilevazione', freq='YE')).sum().reset_index()
        


        # Stampa il dataframe con i dati raggruppati per mese
        print()
        print("Riepilogo mensile dell'IVA dei corrispettivi")
        print(df_mth_sum.to_string(index=False))
        
        # Dataframe IVA mese - CUMULATO
        print()
        print("Riepilogo mensile dell'Imponibile e IVA dei corrispettivi - CUMULATO")
        print(df_mth_cumsum.to_string(index=False))
        
        # Stampa eventuali note contenute nella cartella
        print()
        self.print_note(doc_type)
        
        
        
        return {'all_data': df, 
                'df_mensile': df_mth_sum, 
                'df_mensile_cumulato': df_mth_cumsum, 
                'df_annuale': df_year_sum
                }
                
    
    else:
        print("DataFrame vuoto, nessun dato da elaborare.")
        return None