# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 17:32:01 2025

@author: Mirko
"""
import os
import pandas as pd
from constant import DOCS_TYPES


def process_corrispettivi(self):
    
    doc_type = DOCS_TYPES.CORRISPETTIVI
    
    df = self._load_csv(doc_type)
       
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

        
        df_mth_sum = df[['Imponibile', 'IVA', 'TOTALE', 'Data e ora rilevazione']].groupby(
            pd.Grouper(key='Data e ora rilevazione', freq='ME')).sum().reset_index()


        # Dataframe IVA mese
        print()
        print("Riepilogo mensile dell'IVA delle fatture EMESSE")
        print(df_mth_sum.to_string(index=False))
        
        # Crea un DataFrame cumulativo
        df_mth_cumsum = df_mth_sum.copy()
        df_mth_cumsum[['Imponibile', 'IVA', 'TOTALE']] = df_mth_cumsum[['Imponibile', 'IVA', 'TOTALE']].cumsum()
        
        # Ricava imponibile dall'importo IVA per le fatture con importi esenti
        df_mth_cumsum['imp_fiva_22'] = df_mth_cumsum['IVA'] / .22
        
        # Dataframe IVA mese - CUMULATO
        print()
        print("Riepilogo mensile dell'IVA delle fatture EMESSE - CUMSUM")
        print(df_mth_cumsum.to_string(index=False))
        
        return df, df_mth_sum, df_mth_cumsum
    
    else:
        print("DataFrame vuoto, nessun dato da elaborare.")
        return None