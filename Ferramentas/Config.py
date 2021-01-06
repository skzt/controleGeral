"""
Created on 26 de agosto de 2016

@author: Pedro Vaz
"""

import json
import os

from Manutencao.Constantes import ENCODING

BASE_DIR = os.path.abspath(".")

with open(os.path.join(BASE_DIR, 'config.json'), 'r', encoding=ENCODING) as secret_file:
    _secrets = json.load(secret_file)


def get_secret(configuracao, secrets=_secrets):
    """
    Obtêm a configuração secreta ou eleva um "IOError" erro

    :param configuracao:
    :param secrets:
    :return:
    """
    try:
        return secrets[configuracao]
    except KeyError:
        raise IOError(f"Não existe a configuração: '{configuracao}'")
