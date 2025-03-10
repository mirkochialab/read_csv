# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 16:12:44 2025

@author: Mirko
"""
import sys
from read_csv import ReadCSV
from constant import DOCS_TYPES
# %%



clienti_path = r"G:\Il mio Drive\FILE UTILI\_PYTHON\ivapy"
sys.path.insert(1, clienti_path)
from _clienti import Cliente  # type: ignore


cliente_selected = Cliente.mongelli_giacinta

anno_iva = 2025
mese_iva = 2


# %%

rc = ReadCSV(cliente_selected, anno_iva, mese_iva)

rc._move_csv_to_client_folder()



dfs_corrispett = rc.process_corrispettivi()
rc.xlsx_corrispettivi(dfs_corrispett)


dfs_fte_emesse = rc.process_fte(DOCS_TYPES.FTE_EMESSE)
rc.xlsx_fte(dfs_fte_emesse)



dfs_fte_ricevu = rc.process_fte(DOCS_TYPES.FTE_RICEVUTE)
rc.xlsx_fte(dfs_fte_ricevu)