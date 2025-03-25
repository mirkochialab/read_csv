# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 07:19:04 2025

@author: Mirko
"""
import os
import pandas as pd
from constant import DOCS_TYPES



def process_fte(self, doc_type, path_folder_csv=None):
    
    # Se non viene fornito un path, utilizza quello di default
    if path_folder_csv == None:
        # Path default csv
        path_folder_csv = os.path.join(self.path_folder_iva, doc_type, 'csv')
    
    # Carica il file csv dell'Ade
    df_csv_ade = self._load_csv(doc_type, path_folder_csv)
       
    # Linea
    print()
    print()
    print(doc_type.ljust(100, '-'))
    
    if not df_csv_ade.empty:
        # Controlla e segnala eventuali dati duplicati prima dell'eliminazione
        duplicates = df_csv_ade[df_csv_ade.duplicated(subset=['Sdi/file'], keep=False)]
        if not duplicates.empty:
            print(f"⚠️ ATTENZIONE: trovati {duplicates.shape[0]} record duplicati che verranno rimossi.")

        # Rimuovi i dati duplicati
        df_csv_ade.drop_duplicates(subset=['Sdi/file'], keep='first', inplace=True)

        # Nuovo controllo post-eliminazione
        duplicates_post = df_csv_ade[df_csv_ade.duplicated(subset=['Sdi/file'], keep=False)]
        if duplicates_post.empty:
            print("✅ Nessun record duplicato trovato dopo la pulizia.")

        
        # ### Abbina il file csv dell'Ade al csv FATFELCSV
        # Carica i dati - parametro 'solo_contabilizzate=True'
        ffc = self._load_ffc().df_ffc
        
        if doc_type == DOCS_TYPES.FTE_EMESSE:
            
            df_ffc = ffc['df_att']
        else:
            df_ffc = ffc['df_pas']

        
        # ### FIX.BUG Teamsystem mancata presenza di Identificativo SDI
        # # Verifica che in df_ffc non ci siano record con Identificativo SDI == 0 o NaN
        if df_ffc["Identificativo SDI"].isna().sum() > 0 or (df_ffc["Identificativo SDI"] == 0).sum() > 0:
            
            print("⚠️ ATTENZIONE: Trovati record con Identificativo SDI == 0 in FATFELCSV.")
            
            # Obiettivo: per i record di df_ffc che hanno Identificativo SDI = 0 o NaN,
            # recuperiamo il valore giusto da df_csv_ade usando Numero fattura e Data emissione.

            # 1) Crea un dataframe che contiene solo i record con Identificativo SDI = 0 o NaN.
            df_ffc_sdi_zero = df_ffc[
                (df_ffc["Identificativo SDI"].isna()) | (df_ffc["Identificativo SDI"] == 0)
            ].copy()

            # 2) Itera i record che richiedono il fix.
            for idx, row in df_ffc_sdi_zero.iterrows():
                
                # Ricava numero fattura e data documento da df_ffc
                numero_ffc = row["N.docum.originale"]   # <-- Adatta al nome effettivo della colonna in df_ffc
                data_ffc = row["Data documento"]        # <-- Adatta al nome effettivo della colonna in df_ffc
                
                # Convertiamo la data in stringa per un confronto più semplice
                data_ffc_str = data_ffc.strftime("%Y-%m-%d")
                
                # 3) Proviamo a trovare in df_csv_ade il record corrispondente:
                #    - Stesso 'Numero fattura'
                #    - Stessa 'Data emissione'
                match = df_csv_ade[
                    (df_csv_ade["Numero fattura / Documento"].str.replace("'", "") == numero_ffc) &  # <-- Adatta al nome effettivo in df_csv_ade
                    (df_csv_ade["Data emissione"].dt.strftime("%Y-%m-%d") == data_ffc_str)  # <-- Adatta al nome effettivo
                ]
                
                if not match.empty:
                    # Se troviamo una o più corrispondenze, prendiamo la prima
                    sdi_recuperato = match.iloc[0]["Sdi/file"]  # <-- Adatta al nome colonna ID su df_csv_ade
                    df_ffc.at[idx, "Identificativo SDI"] = sdi_recuperato


        
        # ### Una volta effettuato il fix dell'Identificativo SDI procedi al confronto!!!

        # Unione dei DataFrame sulla colonna "Identificativo SDI" e "Sdi/file"
        df = df_csv_ade.merge(df_ffc, left_on="Sdi/file", right_on="Identificativo SDI", how="outer", indicator=True)

        # Identifica i record non abbinati
        non_abbinati = df[df["_merge"] != "both"]

        # Se ci sono record non abbinati, restituisci un alert
        if not non_abbinati.empty:
            print("⚠️ ATTENZIONE: Alcuni record non sono stati abbinati correttamente!")
            print()
            print("😖 Ecco i dettagli dei record mancanti:")
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
            pd.Grouper(key=key_grouper, freq='ME')).sum().reset_index()
        
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
        
        return {doc_type: [df, df_mth_sum, df_mth_cumsum, non_abbinati, df_csv_ade, df_ffc]}

    else:
        print("DataFrame vuoto, nessun dato da elaborare.")
        return None
    
    