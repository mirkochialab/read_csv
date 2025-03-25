# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 12:32:56 2025

@author: Mirko
"""
import os


def make_filename_xlsx(self, doc_type):
    
    return "{}_{}_{}_{}.xlsx".format(self.anno_iva,
                                         doc_type,
                                         self.cliente_folder,
                                         self.dt_chiusura_iva.strftime("%Y_%m")
                                         )



def print_note(self, doc_type):
    
    try:
        path_file_note = os.path.join(self.path_folder_iva, doc_type, 'NOTE.txt')
        
        f = open(path_file_note)
        content = f.read()
        f.close()
        
        print()
        print(doc_type.ljust(13, ' '), "NOTE:")
        print(content)
    except:
        print()
        print(doc_type.ljust(13, ' '), "NON CI SONO NOTE!")    