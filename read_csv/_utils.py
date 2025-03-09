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



    