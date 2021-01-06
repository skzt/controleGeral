'''
Created on 25 de jun de 2018

@author: GYN-CPD-PEDRO
'''

import tkinter as tk
from tkinter.ttk import Combobox

from Ferramentas.dataEntry import DataEntry
from Manutencao.Constantes import *
from Manutencao.PopUp import popUP


class Busca(tk.Toplevel):
    '''
    classdocs
    '''

    def __init__(self, parent, DB, instancia, *arg, **kwarg):
        tk.Toplevel.__init__(self, parent, *arg, **kwarg)

        self.grab_set()
        self.title("Busca por Chamado de Manutenção")
        self.transient(self.master)

        self.DB = DB

        self.numeroDeEntrys = 0

        buscaButton = tk.Button(self, text="Pesquisar")
        buscaButton['relief'] = 'groove'
        buscaButton['bd'] = 6

        if instancia == 'cc':
            self.numeroDeEntrys = 5
            buscaButton.bind('<Return>', lambda _: self.buscaChamadas())
            buscaButton['command'] = self.buscaChamadas
        elif instancia == 'cv':
            self.numeroDeEntrys = 3
            buscaButton.bind('<Return>', lambda _: self.buscaVisitas())
            buscaButton['command'] = self.buscaVisitas
        elif instancia == 'cp':
            self.numeroDeEntrys = 5
            buscaButton['command'] = self.buscaPecas

        self.entryList = []
        self.variableList = []
        self.labelList = []

        # =======================================================================
        # Gerando os labels, variables e entrys para as janelas de busca
        # =======================================================================
        for index in range(self.numeroDeEntrys):
            self.labelList.append(tk.Label(self))
            self.variableList.append(tk.StringVar())

            if instancia == 'cc':
                if index == 2:
                    self.entryList.append(DataEntry(self, self.variableList[index]))
                    self.entryList[index]['width'] = 10
                    continue

            elif instancia == 'cv':
                if index == 1:
                    self.entryList.append(DataEntry(self, self.variableList[index]))
                    self.entryList[index]['width'] = 10
                    continue
                if index == 2:
                    self.entryList.append(Combobox(self))
                    self.entryList[index]['textvariable'] = self.variableList[index]
                    self.entryList[index]['width'] = 6
                    self.entryList[index]['values'] = ['Sim', 'Não', 'Todos']
                    self.entryList[index]['state'] = 'readonly'
                    continue

            elif instancia == 'cp':
                if index == 2 or index == 4:
                    self.entryList.append(DataEntry(self, self.variableList[index]))
                    self.entryList[index]['width'] = 10
                    continue

            self.entryList.append(tk.Entry(self))
            self.variableList[index].trace('w',
                                           lambda a, b, c, i=index, inst=instancia:
                                           self.traceVariaveis(i, inst)
                                           )
            self.entryList[index]['textvariable'] = self.variableList[index]

        #                 cc                        cv                        cp
        #         0 -> Numero Chamado         0 -> Numero Chamado        0 -> Numero Chamado
        #         1 -> Numero de Serie        1 -> Data Visita           1 -> NF Entrada
        #         2 -> Data                   2 -> Resolvido             2 -> Data Envio
        #         3 -> Filial                                            3 -> NF Saida
        #         4 -> Responsavel                                       4 -> Data Recebimento

        # =======================================================================
        # Configurando e fixando na grid as labels
        # =======================================================================
        self.labelList[0]['text'] = "Número do Chamado"
        self.labelList[0].grid(row=0, column=0, pady=(10, 0))

        if instancia == 'cc':
            self.labelList[1]['text'] = "Número de Série"
            self.labelList[1].grid(row=0, column=1, pady=(10, 0))

            self.labelList[2]['text'] = "Data de Abertura"
            self.labelList[2].grid(row=0, column=2,
                                   pady=(10, 0), padx=(0, 10))

            self.labelList[3]['text'] = "Filial"
            self.labelList[3].grid(row=2, column=0, pady=(5, 0))

            self.labelList[4]['text'] = "Responsavel"
            self.labelList[4].grid(row=2, column=1, pady=(5, 0))

        elif instancia == 'cv':
            self.labelList[1]['text'] = "Data da Visita"
            self.labelList[1].grid(row=0, column=1, pady=(10, 0))

            self.labelList[2]['text'] = "Chamado Foi Resolvido?"
            self.labelList[2].grid(row=0, column=2,
                                   pady=(10, 0), padx=(0, 10))

        elif instancia == 'cp':
            self.labelList[1]['text'] = "Nota Fiscal de Entrada"
            self.labelList[1].grid(row=0, column=1, pady=(10, 0))

            self.labelList[2]['text'] = "Data de Envio"
            self.labelList[2].grid(row=0, column=2,
                                   pady=(10, 0), padx=(0, 10))

            self.labelList[3]['text'] = "Nota Fiscal de Saida"
            self.labelList[3].grid(row=2, column=0, pady=(5, 0))

            self.labelList[4]['text'] = "Data de Recebimento"
            self.labelList[4].grid(row=2, column=1, pady=(5, 0))

        # =======================================================================
        # Configurando e fixando na grid as entrys
        # =======================================================================
        self.entryList[0].focus()
        self.entryList[0].bind("<Return>",
                               lambda _:
                               self.entryList[0].tk_focusNext().focus())
        self.entryList[0].grid(row=1, column=0, padx=(10, 5))

        self.entryList[1].bind("<Return>",
                               lambda _:
                               self.entryList[1].tk_focusNext().focus())
        self.entryList[1].grid(row=1, column=1, padx=(0, 5))

        self.entryList[2].bind("<Return>",
                               lambda _:
                               self.entryList[2].tk_focusNext().focus())
        self.entryList[2].grid(row=1, column=2, padx=(0, 10))

        if self.numeroDeEntrys > 3:
            self.entryList[3].bind("<Return>",
                                   lambda _:
                                   self.entryList[3].tk_focusNext().focus())
            self.entryList[3].grid(row=3, column=0, padx=(10, 0))

            self.entryList[4].bind("<Return>",
                                   lambda _:
                                   self.entryList[4].tk_focusNext().focus())
            self.entryList[4].grid(row=3, column=1)

        buscaButton.grid(row=4, column=0, padx=(10, 0), pady=(10, 10))

        self.tudoVar = tk.IntVar()
        tudoBox = tk.Checkbutton(self)
        tudoBox['text'] = "Todos Resultados."
        tudoBox['variable'] = self.tudoVar
        tudoBox['command'] = lambda inst=instancia: self.searchAll(inst)
        tudoBox['indicatoron'] = False
        tudoBox['relief'] = 'groove'
        tudoBox['takefocus'] = False
        tudoBox.grid(row=3, column=2, pady=(10, 10), padx=(10, 10))

        clearButton = tk.Button(self)
        clearButton['text'] = "Limpar Filtros"
        clearButton['command'] = self.clearEntry
        clearButton['relief'] = 'groove'
        clearButton['bd'] = 6
        clearButton['takefocus'] = False
        clearButton.grid(row=4, column=1)

        cancelButton = tk.Button(self)
        cancelButton['text'] = "Cancelar"
        cancelButton['command'] = self.sair
        cancelButton['relief'] = 'groove'
        cancelButton['bd'] = 6
        cancelButton['takefocus'] = False
        cancelButton.grid(row=4, column=2, pady=(10, 10))

    def sair(self):
        self.destroy()

    def clearEntry(self):
        for var in self.variableList:
            var.set('')

    def searchAll(self, instancia):
        if self.tudoVar.get() == 0:
            # ===============================================================
            # CheckButton "Todos Resultados" foi desmarcado
            # ===============================================================
            for entry in self.entryList:
                entry['state'] = 'normal'
        else:
            # ===============================================================
            # CheckButton "Todos resultados" foi marcado
            # ===============================================================
            for entry in self.entryList:
                entry['state'] = 'disabled'

        if instancia == 'cc':
            self.buscaChamadas()
        elif instancia == 'cv':
            self.buscaVisitas()
        elif instancia == 'cp':
            self.buscaPecas()

    def buscaChamadas(self):
        column = ["Número do Chamado", "Número de Série", "Data",
                  "Horario", "Filial", "Responsavel"]
        busca = 'SELECT * FROM chamadas WHERE '

        buscaVazia = True

        if self.variableList[0].get() != '':
            busca += "num_chamado LIKE '%%%s%%'" % (self.variableList[0].get())
            buscaVazia = False

        if self.variableList[1].get() != '':
            if buscaVazia == False:
                busca += ' AND '
            busca += "num_serie LIKE '%%%s%%'" % (self.variableList[1].get())
            buscaVazia = False

        if self.variableList[2].get() != '  /  /    ':
            if buscaVazia == False:
                busca += ' AND '
            data = self.variableList[2].get()
            data = self.adaptaData('search', data)
            if isinstance(data, tuple):
                busca += "data LIKE '%%%s%%' AND data LIKE '%%%s%%'" % (data[0], data[1])
            else:
                busca += "data LIKE '%%%s%%'" % (data)
            buscaVazia = False

        if self.variableList[3].get() != '':
            if buscaVazia == False:
                busca += ' AND '
            busca += "filial LIKE '%%%s%%'" % (self.variableList[3].get())
            buscaVazia = False

        if self.variableList[4].get() != '':
            if buscaVazia == False:
                busca += ' AND '
            busca += "responsavel LIKE '%%%s%%'" % (self.variableList[4].get())
            buscaVazia = False

        if self.tudoVar.get() == 1:
            busca = busca[:22]

        else:
            if len(busca) <= 29:
                tk.messagebox.showerror(title="Campos em branco",
                                        message= \
                                            "Ao menos 1 campo deve ser preenchido para executar a busca.",
                                        parent=self)
                return

        cursor = self.DB.cursor()
        try:
            cursor.execute(busca)
        except Exception as exp:
            with open('log.txt', 'w', encoding=ENCODING) as file:
                file.write(exp)
                file.close()
        tmp = list(cursor.fetchall())

        select = []

        for resultado in tmp:
            resultado = list(resultado)
            resultado[2] = self.adaptaData('select', resultado[2])
            select.append(resultado)
        del tmp

        popUP(parent=self.master, instance='CC').montarTree(column, select)
        cursor.close()
        self.destroy()

    def buscaVisitas(self):
        column = ["Número do Chamado", "Data", "Horario", "Resolvido"]
        busca = 'SELECT num_chamado, data_visita, hora_visita, observacao,\
        resolvido FROM visitas WHERE '

        buscaVazia = True

        if self.variableList[0].get() != '':
            busca += "num_chamado LIKE '%%%s%%'" % (self.variableList[0].get())
            buscaVazia = False

        if self.variableList[1].get() != '  /  /    ':
            if buscaVazia == False:
                busca += ' AND '
            data = self.variableList[1].get()
            data = self.adaptaData('search', data)
            if isinstance(data, tuple):
                busca += "data LIKE '%%%s%%' AND data LIKE '%%%s%%'" % (data[0], data[1])
            else:
                busca += "data LIKE '%%%s%%'" % (data)
            buscaVazia = False

        if self.variableList[2].get() != '':
            if buscaVazia == False:
                busca += ' AND '

            resolvido = self.variableList[2].get()
            if resolvido == 'Sim':
                resolvido = 1
            elif resolvido == 'Não':
                resolvido = 0
            elif resolvido == 'Todos':
                resolvido = "1' OR resolvido = '0"
            busca += "resolvido = '%s'" % (resolvido)

            buscaVazia = False

        if self.tudoVar.get() == 1:
            busca = busca[:87]
        else:
            if len(busca) <= 94:
                tk.messagebox.showerror(title="Campos em branco",
                                        message= \
                                            "Ao menos 1 campo deve ser preenchido para executar a busca.",
                                        parent=self)
                return

        cursor = self.DB.cursor()
        try:
            cursor.execute(busca)
        except Exception as exp:
            tk.messagebox.showerror(title="Erro na busca", message=exp, parent=self)

        tmp = list(cursor.fetchall())

        select = []
        for resultado in tmp:
            resultado = list(resultado)
            resultado[1] = self.adaptaData('select', resultado[1])
            select.append(resultado)
        del tmp

        popUP(parent=self.master, instance='CV').montarTree(column, select)
        cursor.close()
        self.destroy()

    def buscaPecas(self):
        column = ["Número do Chamado", "NF de Entrada",
                  "Data de Envio", "NF de Saída", "Data de Recebimento"]
        busca = 'SELECT * FROM pecas WHERE '

        buscaVazia = True

        if self.variableList[0].get() != '':
            busca += "num_chamado LIKE '%%%s%%'" % (self.variableList[0].get())
            buscaVazia = False

        if self.variableList[1].get() != '':
            if buscaVazia == False:
                busca += ' AND '
            busca += "nf_entrada LIKE '%%%s%%'" % (self.variableList[1].get())
            buscaVazia = False

        if self.variableList[2].get() != '  /  /    ':
            if buscaVazia == False:
                busca += ' AND '
            data = self.variableList[2].get()
            data = self.adaptaData('search', data)
            if isinstance(data, tuple):
                busca += "data_envio LIKE '%%%s%%' AND data LIKE '%%%s%%'" % (data[0], data[1])
            else:
                busca += "data_envio LIKE '%%%s%%'" % (data)
            buscaVazia = False

        if self.variableList[3].get() != '':
            if buscaVazia == False:
                busca += ' AND '
            busca += "nf_saida LIKE '%%%s%%'" % (self.variableList[3].get())
            buscaVazia = False

        if self.variableList[4].get() != '  /  /    ':
            if buscaVazia == False:
                busca += ' AND '
            data = self.variableList[4].get()
            data = self.adaptaData('search', data)
            if isinstance(data, tuple):
                busca += "data_recebimento LIKE '%%%s%%' AND data LIKE '%%%s%%'" % (data[0], data[1])
            else:
                busca += "data_recebimento LIKE '%%%s%%'" % (data)
            buscaVazia = False

        if self.tudoVar.get() == 1:
            busca = busca[:22]

        else:
            if len(busca) <= 29:
                tk.messagebox.showerror(title="Campos em branco",
                                        message= \
                                            "Ao menos 1 campo deve ser preenchido para executar a busca.",
                                        parent=self)
                return

        cursor = self.DB.cursor()
        try:
            cursor.execute(busca)
        except Exception as exp:
            with open('log.txt', 'w', encoding=ENCODING) as file:
                file.write(exp)
                file.close()
        tmp = list(cursor.fetchall())

        select = []

        for resultado in tmp:
            resultado = list(resultado)
            resultado[2] = self.adaptaData('select', resultado[2])
            select.append(resultado)
        del tmp

        popUP(parent=self.master, instance='CP').montarTree(column, select)
        cursor.close()
        self.destroy()

    def traceVariaveis(self, index, instancia):
        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if index == 0:
            num_chamado = self.variableList[index]
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

        # -------------------------------------------------------------------------------
        elif index == 1:
            if instancia == 'cc':  # num_serie
                num_serie = self.variableList[index]
                if len(num_serie.get()) > NUM_SERIE_SIZE:
                    num_serie.set(num_serie.get()[:NUM_SERIE_SIZE].upper())
                else:
                    num_serie.set(num_serie.get().upper())
                return

            elif instancia == 'cp':  # nf_entrada
                nf_entrada = self.variableList[index]

                if len(nf_entrada.get()) > NOTAFISCAL_SIZE:
                    nf_entrada.set(nf_entrada.get()[:NOTAFISCAL_SIZE])
                    return

                saida = ''

                for char in nf_entrada.get():
                    if char.isdecimal():
                        saida += char
                nf_entrada.set(saida)
                return

        # -------------------------------------------------------------------------------
        elif index == 2:
            pass

        # -------------------------------------------------------------------------------
        elif index == 3:
            if instancia == 'cc':
                filial = self.variableList[index]  # FILIAL
                if len(filial.get()) > FILIAL_SIZE:
                    filial.set(filial.get()[:FILIAL_SIZE].upper())
                    return
                saida = ''

                for char in filial.get():
                    if char.isalpha():
                        saida += char
                filial.set(saida.upper())

                return

            elif instancia == 'cp':
                nf_entrada = self.variaveisPecas[index]

                if len(nf_entrada.get()) > NOTAFISCAL_SIZE:
                    nf_entrada.set(nf_entrada.get()[:NOTAFISCAL_SIZE])
                    return

                saida = ''

                for char in nf_entrada.get():
                    if char.isdecimal():
                        saida += char
                nf_entrada.set(saida)
                return

        # -------------------------------------------------------------------------------
        elif index == 4:
            if instancia == 'cc':
                responsavel = self.variableList[index]
                if len(responsavel.get()) > RESPONSAVEL_SIZE:
                    responsavel.set(responsavel.get()[:RESPONSAVEL_SIZE])
                    return

                saida = ''

                for char in responsavel.get():
                    if char.isalpha() or char == ' ':
                        saida += char
                responsavel.set(saida.upper())
                return

    def adaptaData(self, mode, data):
        ''' Para mode = "INSERT" -> adaptar data para o formato 2017-10-31
            Para mode = "SELECT" -> adaptar data para o formato 31/10/2017
            Para mode = "SEARCH" -> adaptar data para o formato 2017-10-31
        '''
        if mode.upper() == "INSERT":
            data = data[6:10] + '-' + data[3:5] + '-' + data[:2]
            return data
        elif mode.upper() == "SELECT":
            data = str(data)
            data = data[8:10] + '/' + data[5:7] + '/' + data[:4]
            return data
        elif mode.upper() == "SEARCH":
            formatoData = []

            if data[:2] == '  ':
                formatoData.append(True)
            else:
                formatoData.append(False)

            if data[3:5] == '  ':
                formatoData.append(True)
            else:
                formatoData.append(False)

            if data[6:10] == '    ':
                formatoData.append(True)
            else:
                formatoData.append(False)

            def removeEspaços(string):
                return string.replace(' ', '')

            if formatoData == [False, False, True]:
                data = removeEspaços(data[3:5]) + '-' + removeEspaços(data[:2])
                return data

            if formatoData == [False, True, False]:
                return (removeEspaços(data[6:10]), removeEspaços(data[:2]))

            if formatoData == [False, True, True]:
                return removeEspaços(data[:2])

            if formatoData == [True, False, False]:
                data = removeEspaços(data[6:10]) + '-' + removeEspaços(data[3:5])
                return data

            if formatoData == [True, False, True]:
                return removeEspaços(data[3:5])

            if formatoData == [True, True, False]:
                return removeEspaços(data[6:10])

            if formatoData == [False, False, False]:
                data = data[6:10] + '-' + data[3:5] + '-' + data[:2]
                return data
