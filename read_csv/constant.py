# -*- coding: utf-8 -*-
""" 
Created on 2025/03/05 06:40:56
@author: Mirko
"""

# Lista costante contenente i tipo di documenti 
class DOCS_TYPES:
    FTE_EMESSE = 'FTE_EMESSE'
    FTE_RICEVUTE = 'FTE_RICEVUTE'
    FTE_MESSE_A_DISPOSIZIONE = 'FTE_MESSE_A_DISPOSIZIONE'
    CORRISPETTIVI = 'CORRISPETTIVI'

    @classmethod
    def as_list(cls):
        """Restituisce tutti i tipi come lista"""
        return [
            cls.FTE_EMESSE,
            cls.FTE_RICEVUTE,
            cls.FTE_MESSE_A_DISPOSIZIONE,
            cls.CORRISPETTIVI
        ]