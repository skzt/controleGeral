'''
Created on 25 de jun de 2018

@author: GYN-CPD-PEDRO
'''

import os
import tkinter as tk

from Ferramentas.Config import get_secret
from Manutencao.PopUp import popUP


class ValidaCI(tk.Frame):
    def __init__(self, parent, *arg, **kwarg):
        tk.Frame.__init__(self, parent, *arg, **kwarg)

        verifFrame = tk.LabelFrame(self, text="Verificar")
        verifFrame.grid(row=0, column=0, padx=(150, 0))
        validFrame = tk.LabelFrame(self, text="Validar")
        validFrame.grid(row=1, column=0, sticky='nes', padx=(150, 0))

        verifButton = tk.Button(verifFrame)
        validButton = tk.Button(validFrame)

        self.entryList = [tk.Entry(verifFrame),
                          tk.Entry(validFrame),
                          tk.Entry(validFrame)]

        self.varList = [tk.StringVar(),
                        tk.StringVar(),
                        tk.StringVar()]

        self.labelList = [tk.Label(verifFrame),
                          tk.Label(validFrame),
                          tk.Label(validFrame)]

        # =======================================================================
        # Botões
        # =======================================================================

        verifButton['text'] = "Verificar"
        verifButton['relief'] = 'groove'
        verifButton['bd'] = '6'
        verifButton['command'] = self.verificar
        verifButton.bind("<Return>", lambda _: self.verificar())
        verifButton.grid(row=2, column=0, padx=(0, 0), pady=(10, 10))

        validButton['text'] = "Validar"
        validButton['relief'] = 'groove'
        validButton['bd'] = '6'
        validButton['command'] = self.validar
        validButton.bind("<Return>", lambda _: self.validar())
        validButton.grid(row=2, column=0, sticky='ns', padx=(10, 0), pady=(5, 10), columnspan=2, )

        # =======================================================================
        # Entrada de Dados
        # =======================================================================

        # Destino        Entry        Label
        #   [0]=Verificar  [0]=Entry    [0]=Filial
        #   [1]=Validar    [1]=Entry    [1]=Filial
        #   [2]=Validar    [2]=Entry    [2]=CI

        self.labelList[0]['text'] = 'Filial'
        self.labelList[0].grid(row=0, column=0, padx=(5, 0), pady=(10, 0))
        self.entryList[0]['textvariable'] = self.varList[0]
        self.entryList[0].textvariable = self.varList[0]
        self.entryList[0].focus()
        self.entryList[0].bind("<Return>", self.proximo)
        self.entryList[0].grid(row=1, column=0, padx=(10, 10))
        self.varList[0].trace('w',
                              lambda a, b, c, i=0: self.traceVariaveis(i)
                              )

        self.labelList[1]['text'] = 'Filial'
        self.labelList[1].grid(row=0, column=0, pady=(10, 0))
        self.entryList[1]['textvariable'] = self.varList[1]
        self.entryList[1].textvariable = self.varList[1]
        self.entryList[1].bind("<Return>", self.proximo)
        self.entryList[1].grid(row=1, column=0, padx=(10, 10), pady=(0, 5))
        self.varList[1].trace('w',
                              lambda a, b, c, i=1: self.traceVariaveis(i)
                              )

        self.labelList[2]['text'] = 'Comunicação Interna'
        self.labelList[2].grid(row=0, column=1, pady=(10, 0))
        self.entryList[2]['textvariable'] = self.varList[2]
        self.entryList[2].textvariable = self.varList[2]
        self.entryList[2].bind("<Return>", self.proximo)
        self.entryList[2].grid(row=1, column=1, padx=(10, 10), pady=(0, 5))
        self.varList[2].trace('w',
                              lambda a, b, c, i=2: self.traceVariaveis(i)
                              )
        # Arruma a ordem de foco
        new_order = [self.entryList[0],
                     verifButton,
                     self.entryList[1],
                     self.entryList[2],
                     validButton]

        for widget in new_order:
            widget.lift()

    def traceVariaveis(self, index):
        # ------------------------Filial--------------------------------------
        if index == 0 or index == 1:
            filial = self.varList[index]

            if len(filial.get()) > 3:
                filial.set(filial.get()[:3])
                return

            saida = ''

            for char in filial.get():
                if char.isalpha():
                    saida += char.upper()
            filial.set(saida)
            del saida

        # ------------------------CI--------------------------------------
        elif index == 2:
            ci = self.varList[index]

            if len(ci.get()) > 10:
                ci.set(ci.get()[:10])
                return

            saida = ''

            for char in ci.get():
                if char.isdecimal():
                    saida += char
            ci.set(saida)
            del saida

        return

    def verificar(self):
        obrigatorio = True

        if self.varList[0].get() == '':
            self.labelList[0]['fg'] = 'red'
            obrigatorio = False
        if obrigatorio == True:
            path = os.path.abspath(os.path.join(get_secret("MAIN_PATH"), "Aberto", self.varList[0].get()))
            pasta = [path, os.listdir(path)]

            if len(pasta[1]) == 0:
                tk.messagebox.showinfo(title="Filial em Dia!",
                                       message="A filial %s está em dia.\n Envio de pedidos autorizado." % (
                                           self.varList[0].get()))
                self.clearEntry(False)

            else:
                tk.messagebox.showwarning(title="Filial Não Está em Dia!",
                                          message="A filial %s está devendo %d CIs.\n Clique em 'OK' para ver quais são."
                                                  % (self.varList[0].get(), len(pasta[1])))
                columns = ["CIs Em Aberto", "Solicitante", "Data de Envio"]
                popUP(self, instance='VC').montarTree(columns, pasta)

                self.clearEntry(False)
        else:
            tk.messagebox.showwarning(title="Campo Invalido!",
                                      message="O campo 'Filial' não esta preenchido.\nFavor preencher e tentar novamente.",
                                      parent=self)

    def validar(self):
        obrigatorio = True

        if self.varList[1].get() == '' or self.varList[2].get() == '':
            self.labelList[1]['fg'] = self.labelList[2]['fg'] = 'red'
            obrigatorio = False

        if obrigatorio == True:
            path = os.path.join(get_secret("MAIN_PATH"),
                                "Aberto", self.varList[1].get(),
                                f"{self.varList[2].get()}.docx")

            path = os.path.abspath(path)
            try:
                os.remove(path)
                self.clearEntry(True)
                tk.messagebox.showinfo(title="Sucesso!",
                                       message="CI validado com sucesso!",
                                       parent=self)

            except FileNotFoundError:
                tk.messagebox.showerror(title="Erro ao Remover!",
                                        message="Arquivo não encontrado no caminho:\n" + path,
                                        parent=self)
        else:
            tk.messagebox.showwarning(title="Campo Invalido!",
                                      message="Os campos em vermelho não estão preenchidos\ne são obrigatórios, favor verificar.",
                                      parent=self)
        return

    def clearEntry(self, campo):
        # campo -> False = Verificar
        # campo -> True = Validar
        if not isinstance(campo, bool):
            raise TypeError("campo must be a boolean!")

        if campo:
            index = [1, 2]
        else:
            index = [0]

        for idx in index:
            self.labelList[idx]['fg'] = '#000000'
            self.varList[idx].set("")

        self.entryList[index[0]].focus()

    def proximo(self, evt):
        evt.widget.tk_focusNext().focus()

    @property
    def frame(self):
        return self
