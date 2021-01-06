'''
Created on 25 de jun de 2018

@author: GYN-CPD-PEDRO
'''

import tkinter as tk
from time import strftime

from Manutencao.Constantes import *
from Manutencao.PopUp import popUP
from Manutencao.SearchEngine import Busca


class ControleChamadas(tk.Frame):

    def __init__(self, parent, DB, flag=None, *arg, **kwarg):
        tk.Frame.__init__(self, parent, *arg, **kwarg)
        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=0, column=0, sticky=('e', 'w'))
        self.entryFrame = tk.Frame(self)
        self.entryFrame.grid(row=1, column=0, sticky=('e', 'w', 'n', 's'))

        self.variaveisChamadas = []
        self.entryChamadas = []
        self.labelChamadas = []
        self.dicLabels = {}

        self.new = False
        self.err = False
        self.DB = DB

        # =======================================================================
        #                         Botões
        # =======================================================================

        saveButton = tk.Button(self.buttonFrame)
        saveButton['text'] = "Salvar Nova Chamada"
        saveButton['relief'] = 'groove'
        saveButton['bd'] = '6'
        saveButton['command'] = lambda flag=flag: self.saveAction(flag)
        saveButton.bind("<Return>", lambda _, flag=flag: self.saveAction(flag))
        saveButton.grid(row=0, column=0, sticky=('s', 'w'), padx=(110, 20), pady=(10, 10))

        cleanButton = tk.Button(self.buttonFrame)
        cleanButton['text'] = "Limpar Campos"
        cleanButton['relief'] = 'groove'
        cleanButton['bd'] = '6'
        cleanButton['command'] = self.clearEntry
        cleanButton.bind("<Return>", lambda _: self.clearEntry())
        cleanButton.grid(row=0, column=1, sticky=('s'), padx=(0, 20), pady=(10, 10))

        buscarButton = tk.Button(self.buttonFrame)
        buscarButton['text'] = "Buscar"
        buscarButton['relief'] = 'groove'
        buscarButton['bd'] = '6'
        buscarButton['command'] = lambda master=self: Busca(master, self.DB, 'cc')
        buscarButton.grid(row=0, column=2, sticky=('se'), padx=(0, 10), pady=(10, 10))

        #         imprimirButton = tk.Button(self.buttonFrame)
        #         imprimirButton['text'] = "Imprimir"
        #         imprimirButton['relief'] = 'groove'
        #         imprimirButton['bd'] = '6'
        #         imprimirButton.grid(row = 0, column = 2, sticky = ('s', 'e'), padx = (0, 10), pady = (10, 10))

        # =======================================================================
        #                    Entrada de Dados
        # =======================================================================

        # O vetor segue a sequencia de colunas da tabela do DB.

        # Variaveis        Entry        Label
        #    [0]=StringVar  [0]=Entry    [0]=num_chamado
        #    [1]=StringVar  [1]=Entry    [1]=num_serie
        #    [2]=StringVar  [2]=Entry    [2]=data
        #    [3]=StringVar  [3]=Entry    [3]=hora
        #    [4]=StringVar  [4]=Entry    [4]=filial
        #    [5]=StringVar  [5]=Entry    [5]=responsavel
        #                   [6]=Text     [6]=descricao

        for i in range(6):
            self.variaveisChamadas.append(tk.StringVar())
            self.variaveisChamadas[i].trace('w',
                                            lambda a, b, c, i=i:
                                            self.traceVariaveis(i)
                                            )

            self.entryChamadas.append(tk.Entry
                                      (self.entryFrame,
                                       textvariable=self.variaveisChamadas[i]
                                       )
                                      )
            self.labelChamadas.append(tk.Label(self.entryFrame))

        self.labelChamadas.append(tk.Label(self.entryFrame))
        self.entryChamadas.append(tk.Text(self.entryFrame,
                                          width=36,
                                          height=4
                                          ))

        self.labelChamadas[0]['text'] = "Número do Chamado"
        self.labelChamadas[0].grid(row=0, column=0, sticky=('n', 'w'), padx=(5, 0))
        self.entryChamadas[0].bind("<Tab>", self.proximo)
        self.entryChamadas[0].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[0]] = "num_chamado"
        self.entryChamadas[0].grid(row=1, column=0, sticky=('n', 'w'), pady=(0, 20), padx=(5, 0))

        self.labelChamadas[1]['text'] = "Número de Série"
        self.labelChamadas[1].grid(row=0, column=1, sticky=('n', 'w'), padx=(5, 0))
        self.entryChamadas[1].bind("<Tab>", self.proximo)
        self.entryChamadas[1].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[1]] = "num_serie"
        self.entryChamadas[1].grid(row=1, column=1, sticky=('n', 'w'), pady=(0, 20), padx=(5, 0))

        self.labelChamadas[2]['text'] = "Data de Abertura"
        self.labelChamadas[2].grid(row=0, column=2, sticky=('n', 'w'), padx=(5, 0))
        self.entryChamadas[2].bind("<F3>", self.today)
        self.entryChamadas[2].bind("<Tab>", self.proximo)
        self.entryChamadas[2].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[2]] = "data"
        self.entryChamadas[2].grid(row=1, column=2, sticky=('n', 'w'), pady=(0, 20), padx=(5, 0))

        self.labelChamadas[3]['text'] = "Horário"
        self.labelChamadas[3].grid(row=0, column=3, sticky=('n', 'w'), padx=(0, 5))
        self.entryChamadas[3].bind("<F3>", self.today)
        self.entryChamadas[3].bind("<Tab>", self.proximo)
        self.entryChamadas[3].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[3]] = "hora"
        self.entryChamadas[3].grid(row=1, column=3, sticky=('n', 'w'), padx=(0, 5))

        self.labelChamadas[4]['text'] = "Filial"
        self.labelChamadas[4].grid(row=1, column=0, sticky=('s', 'w'), padx=(5, 0))
        self.entryChamadas[4].bind("<Tab>", self.proximo)
        self.entryChamadas[4].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[4]] = "filial"
        self.entryChamadas[4].grid(row=2, column=0, sticky=('n', 'w'), pady=(0, 5), padx=(5, 0))

        self.labelChamadas[5]['text'] = "Responsavel"
        self.labelChamadas[5].grid(row=1, column=1, sticky=('s', 'w'), padx=(5, 0))
        self.entryChamadas[5].bind("<Tab>", self.proximo)
        self.entryChamadas[5].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[5]] = "responsavel"
        self.entryChamadas[5].grid(row=2, column=1, sticky=('n', 'w'), pady=(0, 5), padx=(5, 0))

        self.labelChamadas[6]['text'] = "Descrição do Problema"
        self.labelChamadas[6].grid(row=1, column=2, sticky=('s', 'e', 'w'), padx=(5, 0), columnspan=5)
        self.entryChamadas[6].bind("<FocusOut>", lambda _: self.traceVariaveis(6))
        self.entryChamadas[6].bind("<Tab>", self.proximo)
        self.entryChamadas[6].bind("<Return>", self.proximo)
        self.dicLabels[self.entryChamadas[6]] = "descricao"
        self.entryChamadas[6].grid(row=2, column=2, sticky=('s', 'w'), pady=(0, 5), padx=(5, 0), columnspan=5)

    def saveAction(self, flag):

        if self.new:
            # Obrigadtorio == True indica que todos os campos obrigatorios estão
            # Preenchidos. E False indica que pelomenos 1 está vazio

            obrigatorio = True
            self.traceVariaveis(6)
            cursor = self.DB.cursor()
            for err in range(6):
                if err != 3:
                    if self.variaveisChamadas[err].get() == "" \
                            or self.variaveisChamadas[err].get() == " ":
                        obrigatorio = False
                        self.labelChamadas[err]['fg'] = 'red'

            text = self.entryChamadas[6].get(1.0, 'end')

            if text == '\n' or len(text) == text.count(' '):
                obrigatorio = False
                self.labelChamadas[6]['fg'] = 'red'

            if obrigatorio:
                try:
                    data = self.adaptaData("INSERT", self.variaveisChamadas[2].get())

                    insert = f"INSERT INTO `chamadas` (`num_chamado`," \
                             f"`num_serie`," \
                             f"`data`," \
                             f"`hora`," \
                             f"`filial`," \
                             f"`responsavel`," \
                             f"`descricao`)" \
                             f"VALUES ( '{self.variaveisChamadas[0].get()}'," \
                             f"'{self.variaveisChamadas[1].get()}'," \
                             f"'{data}'," \
                             f"'{self.variaveisChamadas[3].get()}'," \
                             f"'{self.variaveisChamadas[4].get()}'," \
                             f"'{self.variaveisChamadas[5].get()}'," \
                             f"'{text}')"
                    cursor.execute(insert)
                    self.DB.commit()
                    tk.messagebox.showinfo(title="Sucesso!",
                                           message="Novo Chamado Adicionado Com Sucesso!",
                                           parent=self)
                    self.clearEntry()

                except Exception as err:
                    tk.messagebox.showerror(title="ERROR!", message=f"Erro ao inserir nova chamada:\n{err}",
                                            parent=self)
                    self.DB.rollback()

            else:
                tk.messagebox.showwarning(title="Campo Invalido!",
                                          message="Os campos em vermelho não estão preenchidos\ne são obrigatórios, favor verificar.",
                                          parent=self)
            cursor.close()
            if flag:
                self.destroy()
            return
        else:
            self.proximo(0)

    def traceVariaveis(self, index):
        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if index == 0:
            num_chamado = self.variaveisChamadas[index]
            num_chamado.set(num_chamado.get().upper())
            if len(num_chamado.get()) == 0:
                self.new = False

            if len(num_chamado.get()) > NUM_CHAMADO_SIZE:
                num_chamado.set(num_chamado.get()[:NUM_CHAMADO_SIZE])
                return

            saida = ''

            for char in num_chamado.get():
                if char.isalnum():
                    saida += char
            num_chamado.set(saida)

        # ------------------------NUMERO DE SERIE----------------------------------------
        elif index == 1:
            num_serie = self.variaveisChamadas[index]
            if len(num_serie.get()) > NUM_SERIE_SIZE:
                num_serie.set(num_serie.get()[:NUM_SERIE_SIZE].upper())
            else:
                num_serie.set(num_serie.get().upper())
            return

        # ------------------------DATA---------------------------------------------------
        elif index == 2:
            data = self.variaveisChamadas[index]

            saida = ""

            if self.new == False and len(data.get()) == 10 \
                    and data.get()[4] == '-':
                saida = self.adaptaData('select', data.get())

            else:
                for char in data.get():
                    if char.isdecimal():
                        # 01/34/6789
                        if len(saida) == 2 or len(saida) == 5:
                            saida += '/'
                        saida += char

            self.entryChamadas[index].delete(0, 'end')
            self.entryChamadas[index].insert('end', saida)

            if len(data.get()) > 10:
                data.set(data.get()[:10])

            return

        # ------------------------HORARIO------------------------------------------------
        elif index == 3:
            horario = self.variaveisChamadas[index]
            if len(horario.get()) == 0:
                return
            if horario.get()[1] == ':':
                horario.set("0" + horario.get())
            saida = ""

            for char in horario.get():
                if char.isdecimal():
                    # 01:34:67
                    if len(saida) == 2:  # Horas
                        if int(saida[:2]) > 24:
                            saida = '24'
                        saida += ':'

                    elif len(saida) == 5:  # Minutos
                        if int(saida[3:5]) > 60:
                            saida = saida[:3] + '59'
                        saida += ':'
                    saida += char

                    if len(saida) == 8:
                        if int(saida[6:8]) > 60:
                            saida = saida[:6] + '59'

            self.entryChamadas[index].delete(0, 'end')
            self.entryChamadas[index].insert('end', saida)

            if len(horario.get()) > 8:
                horario.set(horario.get()[:8])

        # ------------------------FILIAL-------------------------------------------------
        elif index == 4:
            filial = self.variaveisChamadas[index]
            if len(filial.get()) > FILIAL_SIZE:
                filial.set(filial.get()[:FILIAL_SIZE].upper())
                return
            saida = ''

            for char in filial.get():
                if char.isalpha():
                    saida += char
            filial.set(saida.upper())

            return

        # ------------------------RESPONSAVEL--------------------------------------------
        elif index == 5:
            responsavel = self.variaveisChamadas[index]
            if len(responsavel.get()) > RESPONSAVEL_SIZE:
                responsavel.set(responsavel.get()[:RESPONSAVEL_SIZE])
                return

            saida = ''

            for char in responsavel.get():
                if char.isalpha() or char == ' ':
                    saida += char
            responsavel.set(saida.upper())

        # ------------------------DESCRICAO----------------------------------------------
        elif index == 6:
            descricao = self.entryChamadas[index]

            saida = descricao.get(0.0, 'end')
            descricao.delete(0.0, 'end')

            if len(saida) > DESCRICAO_SIZE:
                descricao.insert(0.0, saida[:NUM_SERIE_SIZE].upper())
            else:
                descricao.insert(0.0, saida.upper())

            return
        return

    def proximo(self, evt=None):
        if isinstance(evt, tk.Event):
            w = evt.widget
        else:
            w = self.entryChamadas[evt]
        column = ["Número do Chamado", "Número de Série", "Data",
                  "Horario", "Filial", "Responsavel"]

        # ------------------------Descricao--------------------------------------
        if w is self.entryChamadas[6]:
            w.tk_focusNext().focus()
            return 'break'

        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if w is self.entryChamadas[0] and self.variaveisChamadas[0].get() != "":
            if not self.new:
                cursor = self.DB.cursor()

                cursor.execute(f"SELECT * FROM chamadas WHERE num_chamado = '{w.get()}'")
                chamada = cursor.fetchone()
                cursor.close()
                if chamada == None:
                    self.new = True
                    tk.messagebox.showinfo(title="Chamado Não Encontrado.",
                                           message="Não foi possivel localizar este número de chamado.\n\
Caso deseje, preencha os campos e adicione o novo chamado.",
                                           parent=self
                                           )
                    self.clearEntry(1)

                else:
                    for index in range(1, len(chamada) - 1):
                        if index == 2:
                            data = self.adaptaData("select", chamada[index])
                            self.variaveisChamadas[index].set(data)

                        else:
                            self.variaveisChamadas[index].set(chamada[index])

                    self.entryChamadas[6].delete(0.0, 'end')
                    self.entryChamadas[6].insert('end', chamada[6])

        # ------------------------Restante----------------------------------------
        elif w.get() != "":
            if self.new == False:
                cursor = self.DB.cursor()

                if self.dicLabels[w] == 'data':
                    if len(w.get()) < 10:
                        tk.messagebox.showwarning(title="Data Invalida",
                                                  message="Data Invalida",
                                                  parent=self)
                        return
                    select = self.adaptaData('insert', w.get())

                else:
                    select = "%" + w.get() + "%"

                cursor.execute(
                    "SELECT * FROM chamadas WHERE %s LIKE '%s'"
                    % (self.dicLabels[w], select)
                )
                tmp = list(cursor.fetchall())

                select = []

                for s in tmp:
                    s = list(s)
                    s[2] = self.adaptaData('select', s[2])
                    select.append(list(s))

                del tmp

                w.delete(0, 'end')

                popUP(parent=self, instance='CC').montarTree(column, select)
                if self.err is True:
                    self.clearEntry()
                    self.err = False
                    return 'break'

                cursor.close()
        w.tk_focusNext().focus()
        return

    def clearEntry(self, start=0):
        for label in self.labelChamadas:
            label['fg'] = '#000000'

        for var in range(start, len(self.variaveisChamadas)):
            self.variaveisChamadas[var].set("")

        for entry in range(start, 6):
            self.entryChamadas[entry].delete(0, 'end')

        self.entryChamadas[6].delete(0.0, 'end')
        self.entryChamadas[0].focus()
        self.err = False

        if start:
            self.new = True
        else:
            self.new = False

    def today(self, evt):
        w = evt.widget
        if w == self.entryChamadas[2]:
            dia = strftime("%d")
            mes = strftime("%m")
            ano = strftime("%Y")
            self.variaveisChamadas[2].set("%s/%s/%s" % (dia, mes, ano))
        elif w == self.entryChamadas[3]:
            self.variaveisChamadas[3].set(strftime("%X"))

    def adaptaData(self, mode, data):
        ''' Para mode = "INSERT" -> adaptar data para o formato 2017/10/31
            Para mode = "SELECT" -> adaptar data para o formato 31/10/2017
        '''
        if mode.upper() == "INSERT":
            data = data[6:10] + '-' + data[3:5] + '-' + data[:2]
            return data
        elif mode.upper() == "SELECT":
            data = str(data)
            data = data[8:10] + '/' + data[5:7] + '/' + data[:4]
            return data

    @property
    def frame(self):
        return self

    @property
    def entradas(self):
        return self.entryChamadas
