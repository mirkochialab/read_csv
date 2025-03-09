# -*- coding: utf-8 -*-
"""
Created on Sat Mar  8 07:37:14 2025

@author: Mirko
"""
import os
import shutil
import datetime

def _move_csv_to_client_folder(self):

    list_csv_downloads = [
        i for i in os.listdir(self.path_download)
        if i.endswith('.csv') and i.startswith(("FTE", "CORRISPETTIVI"))
    ]

    for file_csv in list_csv_downloads:

        # Estrazione dei dati dal nome file
        dfn = file_csv.split('__')
        doc_type, cliente, anno_iva = dfn[0], dfn[1], dfn[2].split('-')[0]

        # Percorsi
        full_path_file_csv_src = os.path.join(self.path_download, file_csv)
        path_folder_dest = os.path.join(self.path_folder_iva, doc_type, 'csv')
        fullpath_file_csv_dest = os.path.join(path_folder_dest, file_csv)

        print(f"Percorso destinazione: {fullpath_file_csv_dest}")

        # Controlla se il file appartiene al cliente
        if cliente != self.cliente_folder:
            print(f"⚠️ ALERT: il file {file_csv} non è di {self.cliente_folder}")
            continue  # Se necessario puoi fermare qui o continuare al prossimo file

        # Controllo esistenza file
        if os.path.exists(fullpath_file_csv_dest):
            print("⚠️ File già presente nella cartella destinazione.")

            path_folder_oldcsv = os.path.join(path_folder_dest, 'oldcsv')
            os.makedirs(path_folder_oldcsv, exist_ok=True)
            print(f"📁 Cartella oldcsv verificata: {path_folder_oldcsv}")

            fullpath_file_csv_oldcsv = os.path.join(path_folder_oldcsv, file_csv)
            shutil.move(fullpath_file_csv_dest, fullpath_file_csv_oldcsv)
            print(f"🔄 File precedente spostato in oldcsv: {fullpath_file_csv_oldcsv}")

            # Rinomina con timestamp
            nowstring = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
            new_filename_file_csv = f"{file_csv.split('.')[0]}_oldcsv_{nowstring}.csv"

            os.rename(
                fullpath_file_csv_oldcsv,
                os.path.join(path_folder_oldcsv, new_filename_file_csv)
            )
            print(f"🔖 File rinominato: {new_filename_file_csv}")

        # Sposta sempre il file nuovo nel percorso finale
        shutil.move(full_path_file_csv_src, fullpath_file_csv_dest)
        print(f"✅ File spostato correttamente: {fullpath_file_csv_dest}")

            