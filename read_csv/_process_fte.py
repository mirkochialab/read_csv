# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 07:19:04 2025

@author: Mirko
"""

import os
import pandas as pd
from constant import DOCS_TYPES
from read_fatfelcsv import FatFelCSV



def process_fte(self, doc_type):
    
    
    df_csv_ade = self._load_csv(doc_type)
       
    # Linea
    print()
    print()
    print(doc_type.ljust(100, '-'))
    
    if not df_csv_ade.empty:
        # Controlla e segnala eventuali dati duplicati prima dell'eliminazione
        duplicates = df_csv_ade[df_csv_ade.duplicated(subset=['Sdi/file'], keep=False)]
        if not duplicates.empty:
            print(f"ATTENZIONE: trovati {duplicates.shape[0]} record duplicati che verranno rimossi.")

        # Rimuovi i dati duplicati
        df_csv_ade.drop_duplicates(subset=['Sdi/file'], keep='first', inplace=True)

        # Nuovo controllo post-eliminazione
        duplicates_post = df_csv_ade[df_csv_ade.duplicated(subset=['Sdi/file'], keep=False)]
        if duplicates_post.empty:
            print("Nessun record duplicato trovato dopo la pulizia.")

        
        # ### Abbina il file csv dell'Ade al csv FATFELCSV
        
        ffc = FatFelCSV(self.cliente, self.anno_iva)
        
        if doc_type == DOCS_TYPES.FTE_EMESSE:
            
            df_ffc = ffc.get_fte_attive()
        else:
            df_ffc = ffc.get_fte_passive()


        # Unione dei DataFrame sulla colonna "Identificativo SDI" e "Sdi/file"
        df = df_csv_ade.merge(df_ffc, left_on="Sdi/file", right_on="Identificativo SDI", how="outer", indicator=True)

        # Identifica i record non abbinati
        non_abbinati = df[df["_merge"] != "both"]

        # Se ci sono record non abbinati, restituisci un alert
        if not non_abbinati.empty:
            print("⚠️ ATTENZIONE: Alcuni record non sono stati abbinati correttamente!")
            print()
            print("Ecco i dettagli dei record mancanti:")
            print(non_abbinati[["Sdi/file", "Identificativo SDI", "_merge"]].to_string(index=False))  # Stampa i record mancanti
        else:
            print("✅ Tutti i record sono stati abbinati correttamente!") 



        
        # Ordina per Data emissione (già datetime)
        df.sort_values('Protocollo MIVA', inplace=True)

        # Raggruppa per mese utilizzando pd.Grouper
        if doc_type == DOCS_TYPES.FTE_EMESSE:
            key_grouper = 'Data emissione'
        else:
            key_grouper = 'Data ricezione'
        
        df_mth_sum = df[['Imponibile', 'IVA', 'TOTALE', key_grouper]].groupby(
            pd.Grouper(key=key_grouper, freq='M')).sum().reset_index()
        
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
        
        return {doc_type: [df, df_mth_sum, df_mth_cumsum]}

    else:
        print("DataFrame vuoto, nessun dato da elaborare.")
        return None
    
    