# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 11:04:16 2025

@author: Mirko
"""
import pandas as pd


class FatFelCSV:
    def __init__(self, cliente, anno_iva):
        
        self.cliente = cliente
        self.cf_cli = cliente['cf']
        self.anno_iva = anno_iva
    
        
    def load(self):
    
        # Carica il CSV
        file_name = r"G:/Il mio Drive/FILE UTILI/_PYTHON/ivapy_beta/read_csv/read_csv/read_csv/FATFELCSV.csv"
       
        try:
            df_ffc = pd.read_csv(file_name, sep=";", encoding="latin-1")
            # Continua con l'elaborazione del dataframe
        except Exception as e:
            print(f"Errore durante la lettura del file: {e}")
    
        # Pulizia dei nomi delle colonne: rimuove spazi iniziali e finali
        df_ffc.columns = df_ffc.columns.str.strip()
        
        # Seleziona le colonne che contengono 'Data' o 'Periodo'
        dt_cols = df_ffc.filter(regex='Data|Periodo|Dt.').columns
        
        # Definisce il formato della data
        format_datetime = '%d/%m/%Y'
        
        # Pulizia e conversione delle date
        df_ffc[dt_cols] = df_ffc[dt_cols].apply(lambda col: pd.to_datetime(
            col.str.strip().replace("", None), format=format_datetime, errors='coerce'
        ))
        
        # Pulisci la colonna "Identificativo SDI" togliendo la "ID-" da "ID-013895659518" e trasforma in un int
        # Rimuove il prefisso "ID-" e converte in intero, gestendo eventuali errori
        df_ffc["Identificativo SDI"] = df_ffc["Identificativo SDI"].str.replace("ID-", "", regex=True).astype(float).astype("Int64")

        
        # Filtra i record che contengono il codice fiscale nella colonna "Cod.fiscale Ditta"
        df_ffc_cliente = df_ffc[df_ffc["Cod.fiscale Ditta"].str.contains(f"CF-{self.cf_cli}", na=False)]

        # Filtra per anno iva sulla base della colonna di Data registrazione che deve essere uguale all'anno 2025
        df_ffc_cliente = df_ffc_cliente[df_ffc_cliente["Data registrazione"].dt.year == self.anno_iva]
        
        return df_ffc_cliente
        
    def get_fte_attive(self):

        df = self.load()        
        
        # Fatture attive
        df_att = df[df["Tipo fattura"].str.strip().eq("Fat. Attiva")]
        
        df_att_mini = df_att[
            ['Cod.fiscale Ditta', 'Ditta', 'Rag.sociale', 'Tipo fattura',
             # 'Data sistema', 'HHMMSS', 
             'Identificativo SDI',
             # 'Tipo estrazione', 'Codice cli/for', 'Cod. ditta contabil.', 'Sezionale', 'Codice SDI',
             # 'Partita IVA cli/for', 'Cod.fiscale cli/for', 
             'Data registrazione', 'N.docum.originale', 'Data documento', 'Protocollo MIVA',
             # 'Numero Linea', 'Prog. Linea', 'HUB-ID', 'Tipo documento FEL',
             # 'Causale trasporto', 'Utente', 'Utente Contabiliz.',
             # 'Data Contabilizz.', 'Flusso', 'Data notifica', 'Codice Anagen.',
             'Rag.soc. cli/for FE', 'Totale Ivato', 
             # 'Totale pagato', 'Differenza',  'Contabilizzazione', 'Tipo registraz. Iva', 'Dt.doc.registraz.Iva',
             'N.doc.registraz.Iva', 
             # 'Causale registraz.Iva', 'Descrizione riga',
             # 'Quantità riga', 'Prezzo riga', 'Al. IVA riga', 'Importo riga',
             # 'IdCodice Cedente', 'IdCodice Cessionario', 'Data Ddt', 'Numero Ddt',
             # 'Data Ddt2', 'Numero Ddt2', 'Conservato', 'Data ultimo stato',
             # 'Ora ultimo stato', 'Solo esterometro', 'CoGe Auto', 'Data contab.',
             # 'Sconto', '%Sconto', 'Sc.Importo'
             ]
            ]
        
        return df_att_mini

    def get_fte_passive(self):

        df = self.load()        
        
        # Fatture attive
        df_pass = df[df["Tipo fattura"].str.strip().eq("Fat. Passiva")]
        
        df_pass_mini = df_pass[
            ['Cod.fiscale Ditta', 'Ditta', 'Rag.sociale', 'Tipo fattura',
             # 'Data sistema', 'HHMMSS', 
             'Identificativo SDI',
             # 'Tipo estrazione', 'Codice cli/for', 'Cod. ditta contabil.', 'Sezionale', 'Codice SDI',
             # 'Partita IVA cli/for', 'Cod.fiscale cli/for', 
             'Data registrazione', 'N.docum.originale', 'Data documento', 'Protocollo MIVA',
             # 'Numero Linea', 'Prog. Linea', 'HUB-ID', 'Tipo documento FEL',
             # 'Causale trasporto', 'Utente', 'Utente Contabiliz.',
             # 'Data Contabilizz.', 'Flusso', 'Data notifica', 'Codice Anagen.',
             'Rag.soc. cli/for FE', 'Totale Ivato', 
             # 'Totale pagato', 'Differenza',  'Contabilizzazione', 'Tipo registraz. Iva', 'Dt.doc.registraz.Iva',
             'N.doc.registraz.Iva', 
             # 'Causale registraz.Iva', 'Descrizione riga',
             # 'Quantità riga', 'Prezzo riga', 'Al. IVA riga', 'Importo riga',
             # 'IdCodice Cedente', 'IdCodice Cessionario', 'Data Ddt', 'Numero Ddt',
             # 'Data Ddt2', 'Numero Ddt2', 'Conservato', 'Data ultimo stato',
             # 'Ora ultimo stato', 'Solo esterometro', 'CoGe Auto', 'Data contab.',
             # 'Sconto', '%Sconto', 'Sc.Importo'
             ]
            ]
        
        return df_pass_mini
