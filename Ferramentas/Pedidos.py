"""
Created on 16 de maio de 2016

@author: Pedro Vaz
"""
import json
import os
from time import strftime
from tkinter import END, DISABLED, NORMAL, Checkbutton, IntVar
from tkinter import Frame, Label, Toplevel, Entry, Button, StringVar
from tkinter import Spinbox, Grid, messagebox
from tkinter.ttk import Combobox

from Ferramentas.Config import get_secret
from Ferramentas.Functions import functions
from Manutencao.Constantes import ENCODING


class pedidos(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.func = functions(self)
        self.pathLocation = get_secret("MAIN_PATH")
        self.matriz = StringVar()
        self.solicitante = StringVar()
        self.produto = StringVar()
        self.pedido = []
        self.index = IntVar()

    def addPedido(self, logoObject):

        # Frame de adicionar pedidos.
        self.frameAdd = Toplevel(self)
        for col in range(8):
            Grid.columnconfigure(self.frameAdd, col, weight=1)

        self.frameAdd.wm_title("Adicionar Novo Pedido")
        self.frameAdd.bind("<Escape>", lambda _: self.frameAdd.destroy())
        logoFrame = Frame(self.frameAdd)

        logoFrame.grid(row=0, column=0, columnspan=7, pady=(20, 0), sticky='N')
        labelImagem = Label(logoFrame)
        labelImagem['image'] = logoObject
        labelImagem.image = logoObject
        labelImagem.pack()

        # Algumas declarações.

        listLabel = []
        listaProdutos = self.func.lerProdutos()
        data = StringVar()
        data.set(strftime("%d/%m/%y"))
        check = IntVar()
        check.set(1)
        spinBox = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]

        self.pedido.clear()

        self.produto.set(listaProdutos[0])

        self.matriz.set(int(self.func.getCI_Atual()) + 1)

        self.index.set(0)

        # Tratamento de erros na leitura de arquivos.
        if listaProdutos == "Error" or self.matriz.get() == "-666":
            self.frameAdd.destroy()
        else:

            # Labels para Entrada de dados.

            del listLabel[:]

            for _ in range(7):
                listLabel.append(Label(self.frameAdd))

            listLabel[0]['text'] = "C.I Matriz"
            listLabel[0].grid(row=1, column=0, pady=(10, 0), padx=(10, 0), sticky='N')

            listLabel[1]['text'] = "C.I Filial"
            listLabel[1]['fg'] = 'red'
            listLabel[1].grid(row=1, column=1, pady=(10, 0), sticky='N')

            listLabel[2]['text'] = "Loja"
            listLabel[2]['fg'] = 'red'
            listLabel[2].grid(row=1, column=2, pady=(10, 0), sticky='N')

            listLabel[3]['text'] = "Solicitante"
            listLabel[3]['fg'] = 'red'
            listLabel[3].grid(row=1, column=3, pady=(10, 0), sticky='N')

            listLabel[4]['text'] = "Data de Envio"
            listLabel[4]['fg'] = 'red'
            listLabel[4].grid(row=1, column=4, pady=(10, 0), sticky='N')

            listLabel[5]['text'] = "Quantidade"
            listLabel[5]['fg'] = 'red'
            listLabel[5].grid(row=1, column=5, pady=(10, 0), sticky='N')

            listLabel[6]['text'] = "Produto"
            listLabel[6]['fg'] = 'red'
            listLabel[6].grid(row=1, column=6, pady=(10, 0), padx=(0, 10), sticky='N')

            # O proprio sistema quem identifica e
            # coloca o valor do C.I da matriz!
            self.entryMatriz = Entry(self.frameAdd)
            self.entryMatriz['textvariable'] = self.matriz
            self.entryMatriz['width'] = 4
            self.entryMatriz['state'] = DISABLED
            self.entryMatriz['takefocus'] = False
            self.entryMatriz.grid(row=2, column=0, padx=(40, 0), sticky='N')

            def verfNumero(flag):
                if flag == 1:
                    self.entryFilial.insert(0, "S/Nº")
                    self.entryFilial.config(state=DISABLED)
                    self.entryLoja.focus()
                elif flag == 0:
                    self.entryFilial.config(state=NORMAL)
                    self.entryFilial.delete(0, END)
                    self.entryFilial.focus()

            self.entryFilial = Entry(self.frameAdd)
            self.entryFilial['width'] = 5
            self.entryFilial.insert(0, "S/Nº")
            self.entryFilial.config(state=DISABLED)
            self.entryFilial.bind("<Tab>", self.setNext)
            self.entryFilial.grid(row=2, column=1, sticky='N')

            self.checkBox = Checkbutton(self.frameAdd)
            self.checkBox['text'] = "Sem Número"
            self.checkBox['variable'] = check
            self.checkBox['command'] = lambda: verfNumero(check.get())
            self.checkBox['onvalue'] = 1
            self.checkBox['offvalue'] = 0
            self.checkBox.grid(row=3, column=1, sticky='N')

            self.entryLoja = Entry(self.frameAdd)
            self.entryLoja['width'] = 4
            self.entryLoja.focus()
            self.entryLoja.grid(row=2, column=2, sticky='N')

            self.listaSolicitantes = Combobox(self.frameAdd)
            self.listaSolicitantes['postcommand'] = self.localizaLoja
            self.listaSolicitantes['state'] = 'readonly'
            self.listaSolicitantes.grid(row=2, column=3, rowspan=3, padx=(20, 10), pady=(7, 0), sticky='N')

            # A data de envio é obtida automaticamente.

            self.entryDataEnvio = Entry(self.frameAdd)
            self.entryDataEnvio['textvariable'] = data
            self.entryDataEnvio['width'] = 8
            self.entryDataEnvio['state'] = DISABLED
            self.entryDataEnvio['takefocus'] = False
            self.entryDataEnvio.grid(row=2, column=4, sticky='N')

            self.spinQuantidade = Spinbox(self.frameAdd)
            self.spinQuantidade['width'] = 3
            self.spinQuantidade['values'] = spinBox
            self.spinQuantidade.bind("<Return>", self.setNext)
            self.spinQuantidade.grid(row=2, column=5, sticky='N')

            self.selecionarProdutos = Combobox(self.frameAdd)
            self.selecionarProdutos['values'] = listaProdutos
            self.selecionarProdutos.grid(row=2, column=6, padx=(0, 20), sticky='N')
            self.selecionarProdutos.current(0)

            # Botões

            button_avancar = Button(self.frameAdd)
            button_avancar['width'] = 15
            button_avancar['text'] = "Avançar"
            button_avancar['command'] = self.func.salvarPedido
            button_avancar.bind("<Return>", lambda _: self.func.salvarPedido())
            button_avancar.grid(row=6, column=1, columnspan=3, pady=(0, 20), sticky='N')

            cancelButton = Button(self.frameAdd)
            cancelButton['width'] = 15
            cancelButton['text'] = "Cancelar"
            cancelButton['command'] = self.frameAdd.destroy
            cancelButton.bind("<Return>", lambda _: self.frameAdd.destroy())
            cancelButton.grid(row=6, column=5, columnspan=3, pady=(0, 20), sticky='N')

    def localizaLoja(self):
        loja = self.entryLoja.get().upper()
        _path = os.path.abspath(os.path.join(self.pathLocation, "Filiais.json"))
        with open(_path, 'r', encoding=ENCODING) as fp:
            filiais = json.load(fp)

        if loja in filiais:
            self.listaSolicitantes['state'] = NORMAL
            self.listaSolicitantes['values'] = []

            _path = os.path.abspath(os.path.join(self.pathLocation, "Lojas", f"{loja}.json"))
            with open(_path, 'r+', encoding=ENCODING) as file:

                self.listaSolicitantes['values'] = json.load(file)
                self.listaSolicitantes.current(0)

            self.listaSolicitantes.grid(row=2, column=3, rowspan=3, padx=(20, 10), pady=(7, 0), sticky='N')

        else:
            self.listaSolicitantes.set('')
            self.listaSolicitantes['values'] = []
            self.listaSolicitantes['state'] = 'readonly'
            message = """Filial "%s" nao econtrada no sistema!
                    \nVerifique o nome da filial e tente novamente.""" % loja

            messagebox.showwarning("ERRO", message, parent=self.frameAdd)
            self.entryLoja.focus()

    def getPedido(self):
        flag = True
        # Obetem as entradas e as coloca em ordem em uma lista.

        self.pedido.append(self.entryMatriz.get().rstrip())
        self.pedido.append(self.entryFilial.get().rstrip())
        self.pedido.append(self.listaSolicitantes.get().rstrip())
        self.pedido.append(self.entryLoja.get().upper().rstrip())
        self.pedido.append(self.entryDataEnvio.get().rstrip())
        self.pedido.append(self.spinQuantidade.get().rstrip())
        self.pedido.append(self.selecionarProdutos.get().rstrip())

        for verify in self.pedido:
            if verify == '' or verify == ():
                flag = False
                break

        if flag is True:

            # Limpa os campos de entrada.
            self.entryMatriz.delete(0, END)
            self.entryFilial.delete(0, END)
            self.solicitante.set('')
            self.entryLoja.delete(0, END)
            self.entryDataEnvio.delete(0, END)
            self.spinQuantidade.delete(0, END)
            self.produto.set("Cilindro DR-3302")
            self.frameAdd.destroy()
            return self.pedido
        else:
            self.pedido.clear()
            return "ERROR"

    def getFrame(self):
        return self.frameAdd

    def getMatriz(self):
        return self.matriz.get()

    @staticmethod
    def setNext(event):
        print(event.widget.tk_focusNext())
        event.widget.tk_focusNext().focus()
        return "break"
