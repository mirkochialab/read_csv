# -*- coding: utf-8 -*-
""" 
Created on 2025/03/04 10:43:31
@author: Mirko
"""

import os
import pandas as pd
from pathlib import Path





# import warnings

# warnings.filterwarnings('ignore')


class ReadCSV:
    def __init__(self,
                 cliente,
                 anno_iva,
                 mese_iva
                 ):

        # Parametri cliente
        self.cliente = cliente
        self.cliente_folder = cliente['folder_name']
        self.periodicity_iva = cliente['periodicity_iva'][str(anno_iva)]

        # Parametri IVA
        self.anno_iva = anno_iva
        self.mese_iva = mese_iva
        self.dt_chiusura_iva = pd.to_datetime(
            f'{anno_iva}-{mese_iva}-01').to_period('M').end_time

        # Parametri file CSV
        self.lettera_gdrive = "G"
        self.path_gdrive = os.path.join(
            self.lettera_gdrive + ":\\", "Il mio Drive")
        self.path_cliente = os.path.join(
            self.path_gdrive, "CLIENTI", self.cliente['folder_name'])
        self.path_folder_iva = os.path.join(
            self.path_cliente, "IVA", str(self.anno_iva))

        # Cartella download file csv
        self.path_download = str(Path.home() / "Downloads")

    def _get_path_folder_csv(self, doc_type):

        return os.path.join(self.path_folder_iva, doc_type, 'csv')

    def _check_file_coerence(self, path_folder_csv, file_csv):

        fullpath_file_csv = os.path.join(path_folder_csv, file_csv)

        # Utilizzo della funzione Path per le statistiche sul file CSV
        file_csv_stat = Path(fullpath_file_csv).stat()
        dt_create_csv = pd.to_datetime(file_csv_stat.st_ctime_ns)

        # ### Controllo di coerenza sui file
        # Ricavo le date di competenza di ogni singolo file CSV dal nome
        date_from_csv_filename = file_csv.replace('.csv', '').split("__")[2]
        dt_csv_quarter_ini = pd.to_datetime(date_from_csv_filename)
        dt_csv_quarter_end = dt_csv_quarter_ini.to_period('Q').end_time

        # print(file)
        # print("-->", "Data creazione file:", dt_create_csv)
        # print("-->", "Data inizio periodo:", dt_csv_quarter_ini)
        # print("-->", "Data fine   periodo:", dt_csv_quarter_end)
        # print("-->", "Data chiusura IVA  :", self.dt_chiusura_iva)

        # # Segnala file non aggiornato con errore
        file_deprecated = False

        # Caso 1 (data di chiusura inferiore a fine trimestre)
        if self.dt_chiusura_iva <= dt_csv_quarter_end:
            # Se la data del file è inferiore della chiusura è deprecato
            if dt_create_csv <= self.dt_chiusura_iva:
                file_deprecated = True

            # Crea ALERT offsettando di 5 giorni
            if dt_create_csv <= (self.dt_chiusura_iva.floor('ms') + pd.DateOffset(days=5)):
                print(
                    "Attenzione la data del file è antecedente i 5 giorni successivi al termine del trimestre!")

        # Caso 2 (data di chiusura superiore a fine trimestre)
        if self.dt_chiusura_iva >= dt_create_csv:
            # Se la data del file è inferiore alla fine del quarter è deprecato
            if dt_create_csv <= dt_csv_quarter_end:
                file_deprecated = True

            # Crea alert offsettando di 5 giorni
            if dt_create_csv <= (dt_csv_quarter_end.floor('ms') + pd.DateOffset(days=5)):
                print(
                    "Attenzione la data del file è antecedente i 5 giorni successivi alla data di chiusura IVA!")

        # Se il file è deprecato vai in errore
        if file_deprecated:
            raise ("ATTENZIONE! il file:", file_csv, "è troppo vecchio!")
        else:
            pass
            # print(f"{file_csv} formalmente corretto!")

    def _load_csv(self, doc_type):

        # Ottieni la path della cartella dei csv relativi ai documenti IVA
        path_folder_csv = self._get_path_folder_csv(doc_type)

        # Ottieni la lista di tutti i file CSV nella cartella
        files_csv = [f for f in os.listdir(
            path_folder_csv) if f.endswith('.csv')]

        # Lista per contenere i DataFrame
        dataframes = []

        # Itera i file CSV
        for file_csv in files_csv:

            # Percorso completo del file CSV
            fullpath_file_csv = os.path.join(path_folder_csv, file_csv)

            # Effettua un controllo di coerenza tra date file e chiusura
            self._check_file_coerence(path_folder_csv, file_csv)

            if 'DATI_ASSENTI' in file_csv:
                continue

            # Apertura del file csv
            dataframe = pd.read_csv(fullpath_file_csv, sep=";")

            # Seleziona le colonne che hanno nel testo la parola 'Data' o 'Periodo'
            date_columns = dataframe.filter(regex='Data|Periodo').columns

            # Converti tutte le colonne della lista usando apply()
            format_datetime = '%d/%m/%Y'

            if doc_type == 'CORRISPETTIVI':
                format_datetime = '%d/%m/%Y %H:%M:%S'

            dataframe[date_columns] = dataframe[date_columns].apply(
                pd.to_datetime, format=format_datetime)

            # Adeguamento delle celle con formato numero
            numeric_columns = dataframe.filter(regex='euro').columns

            dataframe[numeric_columns] = dataframe[numeric_columns].replace(
                ",", ".", regex=True).astype(float)

            # Appendi i dataframe dei vari file csv
            dataframes.append(dataframe)

        # ###-> Concatenazione di tutti i DataFrame in un unico DataFrame

        # Se la lista dataframes NON è vuota concatena i Dataframe e vai oltre
        if dataframes:
            df = pd.concat(dataframes, ignore_index=True)

            if doc_type == 'CORRISPETTIVI':
                df['Amm_Vendite'] = df[df.filter(regex='Ammontare').columns]

            df['Imponibile'] = df[df.filter(regex='Imponibile').columns]
            df['IVA'] = df[df.filter(regex='Imposta').columns]
            df['TOTALE'] = df[['Imponibile', 'IVA']].sum(axis=1)

        else:
            # Altrimenti crea un Dataframe vuoto
            df = pd.DataFrame()

        return df

    from _csv_manager import _move_csv_to_client_folder

    from _process_corrispettivi import process_corrispettivi
    from _process_fte import process_fte
    from _xlsx_corrispettivi import xlsx_corrispettivi
    from _xlsx_fte import xlsx_fte
    from _utils import make_filename_xlsx

