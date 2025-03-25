# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 16:12:44 2025

@author: Mirko
"""
import sys
from read_csv import ReadCSV
from constant import DOCS_TYPES



clienti_path = r"G:\Il mio Drive\FILE UTILI\_PYTHON\ivapy"
sys.path.insert(1, clienti_path)
from _clienti import Cliente  # type: ignore


cliente_selected = Cliente.moroni_jessica



anno_iva = 2025

mese_iva_start = 2

mese_iva_end = 2


# rc = ReadCSV(cliente_selected, anno_iva, mese_iva_end)

# cartella_provvisoria = r"C:\Users\cristina\Downloads\_corrispettivi_check"

# dfcm = rc.process_corrispettivi(path_folder_csv=cartella_provvisoria)


#%%




for m in range(mese_iva_start, mese_iva_end+1):
    
    rc = ReadCSV(cliente_selected, anno_iva, m)
    
    rc._check_folder_tree()

    rc._move_csv_to_client_folder()

        
    dfs_corrispett = rc.process_corrispettivi()
    # zz = dfs_corrispett[0]
    rc.xlsx_corrispettivi(dfs_corrispett)
    
    
    dfs_fte_emesse = rc.process_fte(DOCS_TYPES.FTE_EMESSE)
    # zz0 = dfs_fte_emesse['FTE_EMESSE'][4]
    # rc.xlsx_fte(dfs_fte_emesse)
    
    
    
    dfs_fte_ricevu = rc.process_fte(DOCS_TYPES.FTE_RICEVUTE)
    # rc.xlsx_fte(dfs_fte_ricevu)