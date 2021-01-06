'''
Created on 25 de jun de 2018

@author: GYN-CPD-PEDRO
'''

import tkinter as tk
from time import strftime

from Manutencao.Constantes import *
from Manutencao.ControleChamadas import ControleChamadas
from Manutencao.PopUp import popUP
from Manutencao.SearchEngine import Busca


class ControlePecas(tk.Frame):

    def __init__(self, parent, DB, *arg, **kwarg):
        tk.Frame.__init__(self, parent, *arg, **kwarg)

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=0, column=0, sticky=('e', 'w'))
        self.entryFrame = tk.Frame(self)
        self.entryFrame.grid(row=1, column=0, sticky=('e', 'w', 'n', 's'))

        self.variaveisPecas = []
        self.entryPecas = []
        self.labelPecas = []
        self.dicLabels = {}

        self.new = tk.BooleanVar()
        self.new.set(True)

        self.preenchido = False
        self.err = False
        self.DB = DB

        # =======================================================================
        #                         Botões
        # =======================================================================

        saveButton = tk.Button(self.buttonFrame)
        saveButton['text'] = "Salvar Nova Entrada"
        saveButton['relief'] = 'groove'
        saveButton['bd'] = '6'
        saveButton['command'] = self.saveAction
        saveButton.bind("<Return>", lambda _: self.saveAction())
        saveButton.grid(row=0, column=0, sticky=('s', 'w'), padx=(50, 20), pady=(10, 10))

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
        buscarButton['command'] = lambda master=self: Busca(master, self.DB, 'cp')
        buscarButton.grid(row=0, column=2, sticky=('s', 'e'), padx=(0, 10), pady=(10, 10))

        # Se novoButton estiver desmarcado, signifca que o que sera digitado não é uma enrtada nova (new)
        # Ou seja, será atualizado uma NF ou é uma pesquisa. Logo self.new == False

        # Se atualiza estiver marcada, signifca que o que sera digitado é uma entrada nova (new)
        # Logo self.new == True

        novoButton = tk.Checkbutton(self.buttonFrame)
        novoButton['text'] = "Marque Para Adicionar\n O Novo Pedido de Fusor"
        novoButton['onvalue'] = True
        novoButton['offvalue'] = False
        novoButton['variable'] = self.new
        novoButton['command'] = self.changeNew
        novoButton.grid(row=0, column=3, sticky=('s', 'e'), padx=(0, 10), pady=(10, 10))

        # =======================================================================
        #                    Entrada de Dados
        # =======================================================================

        # O vetor segue a sequencia de colunas da tabela do DB.

        # Variaveis        Entry        Label
        #    [0]=StringVar  [0]=Entry    [0]=num_chamado
        #    [1]=StringVar  [1]=Entry    [1]=nf_entrada
        #    [2]=StringVar  [2]=Entry    [2]=data_envio
        #    [3]=StringVar  [3]=Entry    [3]=nf_saida
        #    [4]=StringVar  [4]=Entry    [4]=data_recebimento

        for i in range(5):
            self.variaveisPecas.append(tk.StringVar())
            self.variaveisPecas[i].trace('w',
                                         lambda a, b, c, i=i:
                                         self.traceVariaveis(i)
                                         )
            self.entryPecas.append(tk.Entry
                                   (self.entryFrame,
                                    textvariable=self.variaveisPecas[i]
                                    )
                                   )
            self.labelPecas.append(tk.Label(self.entryFrame))

        self.labelPecas[0]['text'] = "Número do Chamado"
        self.labelPecas[0].grid(row=0, column=0, sticky=('n', 'w'), padx=(80, 0))
        self.entryPecas[0].bind('<Return>', self.proximo)
        self.entryPecas[0].bind('<Tab>', self.proximo)
        self.dicLabels[self.entryPecas[0]] = "num_chamado"
        self.entryPecas[0].grid(row=1, column=0, sticky=('n', 'w'), pady=(0, 20), padx=(80, 0))

        self.labelPecas[1]['text'] = "Nota Fiscal de Entrada"
        self.labelPecas[1].grid(row=0, column=1, sticky=('n', 'w'), padx=(10, 0))
        self.entryPecas[1].bind('<Return>', self.proximo)
        self.entryPecas[1].bind('<Tab>', self.proximo)
        self.dicLabels[self.entryPecas[1]] = "nf_entrada"
        self.entryPecas[1].grid(row=1, column=1, sticky=('n', 'w'), pady=(0, 20), padx=(10, 0))

        self.labelPecas[2]['text'] = "Data de Envio"
        self.labelPecas[2].grid(row=0, column=2, sticky=('n', 'w'), padx=(10, 0))
        self.entryPecas[2].bind("<F3>", self.today)
        self.entryPecas[2].bind('<Return>', self.proximo)
        self.entryPecas[2].bind('<Tab>', self.proximo)
        self.dicLabels[self.entryPecas[2]] = "data_envio"
        self.entryPecas[2].grid(row=1, column=2, sticky=('n', 'w'), pady=(0, 20), padx=(10, 0))

        self.labelPecas[3]['text'] = "Nota Fiscal de Saida"
        self.labelPecas[3].grid(row=1, column=0, sticky=('s', 'w'), padx=(150, 0), columnspan=2)
        self.entryPecas[3].bind('<Return>', self.proximo)
        self.entryPecas[3].bind('<Tab>', self.proximo)
        self.dicLabels[self.entryPecas[3]] = "nf_saida"
        self.entryPecas[3].grid(row=2, column=0, sticky=('n', 'w'), pady=(0, 10), padx=(150, 0), columnspan=2)
        self.labelPecas[3].grid_remove()
        self.entryPecas[3].grid_remove()

        self.labelPecas[4]['text'] = "Data de Recebimento"
        self.labelPecas[4].grid(row=1, column=1, sticky=('s', 'w'), padx=(80, 0), columnspan=2)
        self.entryPecas[4].bind("<F3>", self.today)
        self.entryPecas[4].bind('<Return>', self.proximo)
        self.entryPecas[4].bind('<Tab>', self.proximo)
        self.dicLabels[self.entryPecas[4]] = "data_recebimento"
        self.entryPecas[4].grid(row=2, column=1, sticky=('n', 'w'), pady=(0, 10), padx=(80, 0), columnspan=2)
        self.labelPecas[4].grid_remove()
        self.entryPecas[4].grid_remove()

    def saveAction(self):

        # Obrigadtorio == True indica que todos os campos obrigatorios estão
        # Preenchidos. E False indica que pelomenos 1 está vazio

        obrigatorio = True
        cursor = self.DB.cursor()
        size = 0
        if self.new.get() is True:
            size = 3
        else:
            size = 5

        for err in range(size):
            if self.variaveisPecas[err].get() == "" \
                    or self.variaveisPecas[err].get() == " ":
                obrigatorio = False
                self.labelPecas[err]['fg'] = 'red'

        if obrigatorio:

            if self.new.get() is False:
                try:
                    data = self.adaptaData("INSERT", self.variaveisPecas[4].get())

                    update = "UPDATE `pecas` SET `nf_saida` = '%d',\
                                                 `data_recebimento` = '%s'\
                                                  WHERE \
                                                  `pecas`.`nf_entrada` = %d" \
                             % (int(self.variaveisPecas[3].get()),
                                data,
                                int(self.variaveisPecas[1].get()))
                    cursor.execute(update)
                    self.DB.commit()
                    tk.messagebox.showinfo(title="Sucesso!",
                                           message="Pedido Atualizada Com Sucesso!",
                                           parent=self)
                    self.clearEntry()
                except Exception as err:
                    tk.messagebox.showerror(title="ERROR!", message=("Erro ao atualizar pedido:\n" \
                                                                         , err), parent=self)
                    self.DB.rollback()

            else:
                try:
                    data = self.adaptaData("INSERT", self.variaveisPecas[2].get())
                    insert = f"INSERT INTO `pecas` (`num_chamado`,\
                                                        `nf_entrada`,\
                                                        `data_envio`,\
                                                        `nf_saida`,\
                                                        `data_recebimento`)\
                                                VALUES ('{self.variaveisPecas[0].get()}',\
                                                        '{int(self.variaveisPecas[1].get())}',\
                                                        '{data}',\
                                                        NULL,\
                                                        NULL)"

                    cursor.execute(insert)

                    self.DB.commit()
                    tk.messagebox.showinfo(title="Sucesso!",
                                           message="Pedido de Peça Adicionado Com Sucesso!",
                                           parent=self)
                    self.clearEntry()

                except Exception as err:
                    tk.messagebox.showerror(title="ERROR!", message=("Erro ao inserir nova chamada:\n" \
                                                                         , err), parent=self)
                    self.DB.rollback()

        else:
            tk.messagebox.showwarning(title="Campo Invalido!",
                                      message="Os campos em vermelho não estão preenchidos\ne são obrigatórios, favor verificar.",
                                      parent=self)
        cursor.close()

        return

    def traceVariaveis(self, index):
        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if index == 0:
            num_chamado = self.variaveisPecas[index]
            num_chamado.set(num_chamado.get().upper())

            if len(num_chamado.get()) > NUM_CHAMADO_SIZE:
                num_chamado.set(num_chamado.get()[:NUM_CHAMADO_SIZE])
                return

            saida = ''

            for char in num_chamado.get():
                if char.isalnum():
                    saida += char
            num_chamado.set(saida)
            return
        # ------------------------NF DE ENTRADA--------------------------------------
        elif index == 1:
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
        # ------------------------DATA---------------------------------------------------
        elif index == 2 or index == 4:
            data = self.variaveisPecas[index]

            saida = ""

            if self.new.get() is False and len(data.get()) == 10 \
                    and data.get()[4] == '-':
                saida = self.adaptaData('select', data.get())

            else:

                for char in data.get():
                    if char.isdecimal():
                        # 01/34/6789
                        if len(saida) == 2 or len(saida) == 5:
                            saida += '/'
                        saida += char

            self.entryPecas[index].delete(0, 'end')
            self.entryPecas[index].insert('end', saida)

            if len(data.get()) > 10:
                data.set(data.get()[:10])

            return

        # ------------------------NF DE SAIDA--------------------------------------
        elif index == 3:
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

        return

    def proximo(self, evt=None):
        if isinstance(evt, tk.Event):
            w = evt.widget
        else:
            w = self.entryPecas[evt]
        column = ["Número do Chamado", "NF de Entrada",
                  "Data de Envio", "NF de Saída", "Data de Recebimento"]

        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if self.preenchido is False:

            if w is self.entryPecas[0] and self.variaveisPecas[0].get() != "":
                cursor = self.DB.cursor()

                cursor.execute(f"SELECT num_chamado FROM chamadas WHERE num_chamado like '%{w.get()}%'")
                chamada = cursor.fetchall()
                cursor.close()
                if (len(chamada) <= 0) \
                        or \
                        (len(chamada) == 1 and chamada[0][0] != w.get()):
                    yesorno = tk.messagebox.askyesno(title="Chamado Não Encontrado.",
                                                     message="Não foi possivel localizar este número de chamado.\n\
    Caso deseje adicionar um novo chamado clique em 'Sim'.",
                                                     parent=self
                                                     )

                    if yesorno == True:
                        tmp = tk.Toplevel(self)
                        tmp.bind('<Escape>', lambda _: tmp.destroy())
                        tmp.transient(self.master)
                        tmp2 = ControleChamadas(tmp, self.DB, flag=True)
                        tmp2.pack()
                        tmp2.entradas[0].focus()
                        tk.Button(tmp,
                                  text="Sair",
                                  command=tmp.destroy
                                  ).pack()
                    else:
                        self.clearEntry()
                        return

                else:
                    tmp = list(chamada)
                    select = []

                    for s in tmp:
                        select.append(list(s))

                    del tmp

                    if len(select) > 1:
                        popUP(parent=self, instance='CP').montarTreeColunaUnica(select, "Número do Chamado", 0)
                        if self.err is True:
                            self.clearEntry()
                            self.err = False
                            return 'break'

                    elif len(select) == 1:
                        w.delete(0, 'end')
                        w.insert(0, chamada)

                    if self.new.get() is False:

                        chamada = w.get()

                        cursor = self.DB.cursor()

                        cursor.execute(
                            "SELECT * FROM pecas WHERE %s = '%s' "
                            % (self.dicLabels[w], chamada)
                        )

                        tmp = list(cursor.fetchall())
                        cursor.close()

                        if len(tmp) == 0:
                            tk.messagebox.showwarning(title="Nota Fiscal Não Encontrada!",
                                                      message="Nenhuma Nota Fiscal foi registrada para este número de chamado.",
                                                      parent=self)

                            self.new.set(True)
                            self.changeNew()

                        else:
                            select = []

                            for s in tmp:
                                s = list(s)
                                s[2] = self.adaptaData('select', s[2])
                                if s[3] == None:
                                    s[3] = ''
                                select.append(s)

                            del tmp
                            popUP(parent=self, instance='CP').montarTree(column, select)
                            if self.err is True:
                                self.clearEntry()
                                self.err = False
                                return 'break'

                            self.preenchido = True

            #                         if self.variaveisPecas[3].get() != '':
            #                             self.new.set(True)

            # ------------------------NF de Entrada--------------------------------------
            elif w is self.entryPecas[1] and self.variaveisPecas[1].get() != "":
                cursor = self.DB.cursor()

                cursor.execute(
                    "SELECT nf_entrada FROM pecas WHERE nf_entrada LIKE '%%%d%%'"
                    % int(w.get())
                )
                nf_entrada = list(cursor.fetchall())
                if len(nf_entrada) == 0:
                    self.new.set(True)
                    self.changeNew()
                    tk.messagebox.showwarning(title="Resultado não encontrado!",
                                              message="NF digitada não encontrada, adicione uma nova NF de Entrada\nou pesquise outro número.")

                else:

                    if len(nf_entrada) == 1:
                        # Caso new == True e a NF digitada esteje entre o retorno do select:
                        if self.new.get() is True and int(w.get()) == nf_entrada[0][0]:
                            tk.messagebox.showerror(title="NF Existente!",
                                                    message="A Nota Fiscal digitada já foi adicionada anteriormente.",
                                                    parent=self)
                            self.clearEntry()
                            return 'break'
                        else:
                            if self.new.get() is False:
                                w.delete(0, 'end')
                                w.insert(0, nf_entrada[0][0])

                    else:
                        if self.new.get() is True:
                            if True in [w.get() in nf for nf in nf_entrada]:
                                tk.messagebox.showerror(title="NF Existente!",
                                                        message="A Nota Fiscal digitada já foi adicionada anteriormente.",
                                                        parent=self)
                                self.clearEntry()
                                return 'break'
                        else:

                            tmp = []

                            for s in nf_entrada:
                                tmp.append(list(s))

                            nf_entrada = tmp
                            del tmp

                            popUP(parent=self, instance='CP').montarTreeColunaUnica(nf_entrada, "NF de Entrada", 1)
                            if self.err is True:
                                self.clearEntry()
                                self.err = False
                                return 'break'

                    if self.new.get() is False:
                        cursor = self.DB.cursor()

                        cursor.execute(
                            "SELECT * FROM pecas WHERE nf_entrada = '%d'"
                            % int(w.get())
                        )
                        nf_entrada = list(cursor.fetchall())

                        tmp = []

                        for s in nf_entrada:
                            s = list(s)
                            s[2] = self.adaptaData('select', s[2])
                            if s[3] == None:
                                s[3] = ''
                            tmp.append(s)

                        nf_entrada = tmp
                        del tmp

                        popUP(parent=self, instance='CP').montarTree(column, nf_entrada)
                        if self.err is True:
                            self.clearEntry()
                            self.err = False
                            return 'break'
                        else:
                            self.preenchido = True

            # ------------------------NF de Saida----------------------------------------

            elif w is self.entryPecas[3] and self.variaveisPecas[3].get() != "":
                cursor = self.DB.cursor()

                cursor.execute(
                    "SELECT nf_saida FROM pecas WHERE nf_saida LIKE '%%%d%%'"
                    % int(w.get())
                )
                nf_saida = list(cursor.fetchall())

                if len(nf_saida) == 1:
                    if int(w.get()) == nf_saida[0][0]:
                        w.delete(0, 'end')
                        w.insert(0, nf_saida[0][0])

                elif len(nf_saida) > 1:

                    tmp = []

                    for s in nf_saida:
                        tmp.append(list(s))

                    nf_saida = tmp
                    del tmp

                    popUP(parent=self, instance='CP').montarTreeColunaUnica(nf_saida, "NF de Saida", 3)
                    if self.err is True:
                        self.clearEntry()
                        self.err = False
                        return 'break'

                cursor = self.DB.cursor()

                cursor.execute(
                    "SELECT * FROM pecas WHERE nf_saida = '%d'"
                    % int(w.get())
                )
                nf_saida = list(cursor.fetchall())

                tmp = []

                for s in nf_saida:
                    s = list(s)
                    s[2] = self.adaptaData('select', s[2])
                    s[4] = self.adaptaData('select', s[4])
                    if s[3] == None:
                        s[3] = ''
                    tmp.append(list(s))

                nf_saida = tmp
                del tmp

                popUP(parent=self, instance='CP').montarTree(column, nf_saida)
                if self.err is True:
                    self.clearEntry()
                    self.err = False
                    return 'break'
                else:
                    self.preenchido = True

            # ------------------------Restante----------------------------------------
            elif w.get() != "":
                if self.preenchido == False:
                    cursor = self.DB.cursor()

                    if len(w.get()) < 10:
                        tk.messagebox.showwarning(title="Data Invalida",
                                                  message="Data Invalida",
                                                  parent=self)
                        return
                    select = self.adaptaData('insert', w.get())

                    cursor.execute(
                        "SELECT * FROM pecas WHERE %s LIKE '%s'"
                        % (self.dicLabels[w], select)
                    )

                    tmp = list(cursor.fetchall())
                    select = []

                    for s in tmp:
                        s = list(s)
                        s[2] = self.adaptaData('select', s[2])
                        s[4] = self.adaptaData('select', s[4])
                        if s[3] == None:
                            s[3] = ''
                        select.append(s)

                    del tmp
                    w.delete(0, 'end')

                    popUP(parent=self, instance='CP').montarTree(column, select)
                    if self.err is True:
                        self.clearEntry()
                        self.err = False
                        return 'break'

                    cursor.close()
        w.tk_focusNext().focus()
        return

    def clearEntry(self, start=0):
        for label in self.labelPecas:
            label['fg'] = '#000000'

        for var in range(start, len(self.variaveisPecas)):
            self.variaveisPecas[var].set("")

        for entry in range(start, 5):
            self.entryPecas[entry].delete(0, 'end')

        self.entryPecas[0].focus()
        self.new.set(True)
        self.changeNew()
        self.preenchido = False
        self.err = False

    def today(self, evt):
        w = evt.widget
        dia = strftime("%d")
        mes = strftime("%m")
        ano = strftime("%Y")
        w.insert('end', "%s/%s/%s" % (dia, mes, ano))

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

    def changeNew(self):
        if self.new.get() is True:
            self.labelPecas[3].grid_remove()
            self.entryPecas[3].grid_remove()
            # self.entryPecas[3]['state'] = 'readonly'

            self.labelPecas[4].grid_remove()
            self.entryPecas[4].grid_remove()
            # self.entryPecas[4]['state'] = 'readonly'

        else:
            self.labelPecas[3].grid()
            self.entryPecas[3].grid()
            # self.entryPecas[3]['state'] = 'normal'

            self.labelPecas[4].grid()
            self.entryPecas[4].grid()
            # self.entryPecas[4]['state'] = 'normal'

    @property
    def frame(self):
        return self

    @property
    def entradas(self):
        return self.entryPecas
