"""
Created on 16 de maio de 2016

@author: Pedro Vaz
"""

import json
import os
from re import compile, escape
from time import strftime
from tkinter import Label, Button, Toplevel
from tkinter import messagebox

from Ferramentas.Config import get_secret
from Ferramentas.CustomBox import customBox
from Manutencao.Constantes import ENCODING


class functions:

    def __init__(self, Pedido):
        self.pedido = Pedido
        self.ano = strftime("%Y")
        self.pathLocation = get_secret("MAIN_PATH")
        self.meses = {
            "January": "Janeiro",
            "February": "Fevereiro",
            "March": "Março",
            "April": "Abril",
            "May": "Maio",
            "June": "Junho",
            "July": "Julho",
            "August": "Agosto",
            "September": "Setembro",
            "October": "Outubro",
            "November": "Novembro",
            "December": "Dezembro"
        }

    def salvarPedido(self):
        save = self.pedido.getPedido()

        if save != "ERROR":
            _path = os.path.abspath(os.path.join(self.pathLocation, self.ano, f"{self.meses[strftime('%B')]}.cfg"))
            with open(_path, 'a', encoding=ENCODING) as file:
                for ped in save:
                    file.write(f"{ped} ")
                file.write("\n")

            self.atualizaCI()

            # Verificar se deve ser impresso ou não, a Comunicação Interna
            customBox(self.pedido, save).printBox()

        else:
            messagebox.showwarning("CAMPOS OBRIGATORIOS!",
                                   "Algum campo não foi preenchido!",
                                   parent=self.pedido.getFrame()
                                   )

    def lerProdutos(self):
        flag = False
        while flag is False:

            try:
                _path = os.path.abspath(os.path.join(self.pathLocation, "Produtos.json"))
                with open(_path, 'r', encoding=ENCODING) as file:
                    produtos = json.load(file)

                produtos.sort()
                return produtos
            except IOError:

                message = """Arquivo "Produtos.json" não localizado!"""
                if messagebox.askretrycancel(parent=self.pedido.getFrame(),
                                             title="Erro!", message=message
                                             ):
                    # Retry
                    flag = False

                else:
                    # Cancel
                    return "ERROR"

    def getCI_Atual(self):
        flag = False
        while flag == False:

            try:
                _path = os.path.abspath(os.path.join(self.pathLocation, self.ano, f"{self.meses[strftime('%B')]}.cfg"))
                with open(_path, 'r', encoding=ENCODING) as file:
                    atual = file.readline().rstrip()

                return atual
            except IOError:

                message = """Arquivo "%s" não localizado na pasta "%s"!""" % (
                    self.meses[strftime("%B")],
                    self.ano
                )
                if messagebox.askretrycancel(parent=self.pedido.getFrame(),
                                             title="Erro!", message=message):
                    # Retry
                    flag = False

                else:
                    # Cancel
                    # C.I sempre será um numero positivo,
                    # por isso retorna negativo para ERROR!!
                    return -667

    def getMes(self, month):
        return self.meses[month]

    def atualizaCI(self):
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro",
                 "Dezembro"
                 ]
        index = meses.index(self.meses[strftime("%B")])

        for idx in range(index, 12):
            _path = os.path.abspath(os.path.join(self.pathLocation, self.ano, f"{meses[idx]}.cfg"))
            with open(_path, 'r+', encoding=ENCODING) as fileCI:
                atual = fileCI.readline()
                text = compile(escape(atual), 0)
                atual = text.sub(self.pedido.getMatriz() + "\n", atual)
                fileCI.seek(0)
                fileCI.write(atual)
