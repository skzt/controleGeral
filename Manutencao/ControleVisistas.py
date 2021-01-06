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


class ControleVisitas(tk.Frame):

    def __init__(self, parent, DB, *arg, **kwarg):
        tk.Frame.__init__(self, parent, *arg, **kwarg)

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=0, column=0, sticky=('e', 'w'))
        self.entryFrame = tk.Frame(self)
        self.entryFrame.grid(row=1, column=0, sticky=('e', 'w', 'n', 's'))

        self.variaveisVisitas = []
        self.entryVisitas = []
        self.labelVisitas = []
        self.dicLabels = {}

        self.new = tk.BooleanVar()
        self.new.set(True)
        self.err = False

        self.DB = DB

        # =======================================================================
        #                         Botões
        # =======================================================================

        saveButton = tk.Button(self.buttonFrame)
        saveButton['text'] = "Salvar Nova Visita"
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
        cleanButton.grid(row=0, column=1, sticky=('s'), padx=(0, 20), pady=(10, 10))

        buscarButton = tk.Button(self.buttonFrame)
        buscarButton['text'] = "Buscar"
        buscarButton['relief'] = 'groove'
        buscarButton['bd'] = '6'
        buscarButton['command'] = lambda master=self: Busca(master, self.DB, 'cv')
        buscarButton.grid(row=0, column=2, sticky=('s', 'e'), padx=(0, 10), pady=(10, 10))

        novoButton = tk.Checkbutton(self.buttonFrame)
        novoButton['text'] = "Marque Para Adicionar\n Nova Visita"
        novoButton['onvalue'] = True
        novoButton['offvalue'] = False
        novoButton['variable'] = self.new
        novoButton.grid(row=0, column=3, sticky=('s', 'e'), padx=(0, 10), pady=(10, 10))
        # =======================================================================
        #                    Entrada de Dados
        # =======================================================================

        # O vetor segue a sequencia de colunas da tabela do DB.
        # Variaveis         Entry      Label
        #    [0]=StringVar   [0]=Entry  [0]=num_chamado
        #    [1]=StringVar   [1]=Entry  [1]=num_serie
        #    [2]=StringVar   [2]=Entry  [2]=data_visita
        #    [3]=StringVar   [3]=Entry  [3]=hora_visita
        #    [4]= -          [4]=Text   [4]=observacao
        #    [5]= BooleanVar [5]= -     [5]= resolvido

        for i in range(3):
            self.variaveisVisitas.append(tk.StringVar())
            self.variaveisVisitas[i].trace('w',
                                           lambda a, b, c, i=i:
                                           self.traceVariaveis(i)
                                           )

            self.entryVisitas.append(tk.Entry
                                     (self.entryFrame,
                                      textvariable=self.variaveisVisitas[i]
                                      )
                                     )
            self.labelVisitas.append(tk.Label(self.entryFrame))

        self.labelVisitas.append(tk.Label(self.entryFrame))
        self.labelVisitas.append(tk.Label(self.entryFrame))

        self.entryVisitas.append(tk.Text(self.entryFrame,
                                         width=36,
                                         height=4)
                                 )

        self.variaveisVisitas.append(tk.BooleanVar())
        simButton = tk.Radiobutton(self.entryFrame,
                                   variable=self.variaveisVisitas[3],
                                   value=True,
                                   text="Sim"
                                   )

        naoButton = tk.Radiobutton(self.entryFrame,
                                   variable=self.variaveisVisitas[3],
                                   value=False,
                                   text="Não"
                                   )

        self.labelVisitas[0]['text'] = "Número do Chamado"
        self.labelVisitas[0].grid(row=0, column=0, sticky=('n', 'w'), padx=(10, 0))
        self.entryVisitas[0].bind("<Tab>", self.proximo)
        self.entryVisitas[0].bind("<Return>", self.proximo)
        self.dicLabels[self.entryVisitas[0]] = "num_chamado"
        self.entryVisitas[0].grid(row=1, column=0, sticky=('n', 'w'), pady=(0, 20), padx=(10, 0))

        self.labelVisitas[1]['text'] = "Data da Visita"
        self.labelVisitas[1].grid(row=0, column=1, sticky=('s', 'w'), padx=(0, 10))
        self.entryVisitas[1].bind("<F3>", self.today)
        self.entryVisitas[1].bind("<Tab>", self.proximo)
        self.entryVisitas[1].bind("<Return>", self.proximo)
        self.dicLabels[self.entryVisitas[1]] = "data_visita"
        self.entryVisitas[1].grid(row=1, column=1, sticky=('n', 'w'), pady=(0, 20), padx=(0, 20))

        self.labelVisitas[2]['text'] = "Hora da Visita"
        self.labelVisitas[2].grid(row=0, column=2, sticky=('n', 'w'), padx=(0, 10))
        self.entryVisitas[2].bind("<F3>", self.today)
        self.entryVisitas[2].bind("<Tab>", self.proximo)
        self.entryVisitas[2].bind("<Return>", self.proximo)
        self.dicLabels[self.entryVisitas[2]] = "hora_visita"
        self.entryVisitas[2].grid(row=1, column=2, sticky=('n', 'w'), padx=(0, 10))

        self.labelVisitas[4]['text'] = "O Problema foi Resolvido?"
        self.labelVisitas[4].grid(row=1, column=0, sticky=('s', 'w'), padx=(5, 0), columnspan=1)
        simButton.grid(row=2, column=0, sticky=('n', 'w'), pady=(0, 5), padx=(5, 0), columnspan=1)
        simButton.select()
        naoButton.grid(row=2, column=0, sticky=('n', 'e'), pady=(0, 5), padx=(0, 10))

        self.labelVisitas[3]['text'] = "Observação do Técnico"
        self.labelVisitas[3].grid(row=1, column=1, sticky=('s', 'w', 'e'), columnspan=3)
        self.entryVisitas[3].bind("<FocusOut>", lambda _: self.traceVariaveis(4))
        self.entryVisitas[3].bind("<Tab>", self.proximo)
        self.entryVisitas[3].bind("<Return>", self.proximo)
        self.dicLabels[self.entryVisitas[3]] = "observacao"
        self.entryVisitas[3].grid(row=2, column=1, sticky=('s', 'w'), columnspan=3, pady=(0, 10))

    def saveAction(self):

        if self.new.get():
            # Obrigadtorio == True indica que todos os campos obrigatorios estão
            # Preenchidos. E False indica que pelomenos 1 está vazio

            obrigatorio = True
            self.traceVariaveis(3)
            cursor = self.DB.cursor()

            for err in range(3):
                if err != 2:
                    if self.variaveisVisitas[err].get() == "" \
                            or self.variaveisVisitas[err].get() == " ":
                        obrigatorio = False
                        self.labelVisitas[err]['fg'] = 'red'

            text = self.entryVisitas[3].get(1.0, 'end')

            if text == '\n' or len(text) == text.count(' '):
                obrigatorio = False
                self.labelVisitas[3]['fg'] = 'red'

            if obrigatorio:
                try:
                    data = self.adaptaData("INSERT", self.variaveisVisitas[1].get())
                    insert = f"INSERT INTO `visitas` (`num_chamado`," \
                             f"`data_visita`," \
                             f"`hora_visita`," \
                             f"`observacao`," \
                             f"`resolvido`)" \
                             f"VALUES ('{self.variaveisVisitas[0].get()}'," \
                             f"'{data}'," \
                             f"'{self.variaveisVisitas[2].get()}'," \
                             f"'{text}'," \
                             f"'{int(self.variaveisVisitas[3].get())}')"

                    cursor.execute(insert)

                    self.DB.commit()
                    tk.messagebox.showinfo(title="Sucesso!",
                                           message="Nova Visita Adicionada Com Sucesso!",
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
        else:
            self.focus_get().tk_focusNext().focus()

    def traceVariaveis(self, index):
        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if index == 0:
            num_chamado = self.variaveisVisitas[index]
            num_chamado.set(num_chamado.get().upper())

            #             if len(num_chamado.get()) == 0:
            #                 self.new.set(False)

            if len(num_chamado.get()) > NUM_CHAMADO_SIZE:
                num_chamado.set(num_chamado.get()[:NUM_CHAMADO_SIZE])
                return

            saida = ''

            for char in num_chamado.get():
                if char.isalnum():
                    saida += char
            num_chamado.set(saida)
            del saida

        # ------------------------DATA---------------------------------------------------
        elif index == 1:
            data = self.variaveisVisitas[index]

            saida = ""

            if self.new.get() == False and len(data.get()) == 10 \
                    and data.get()[4] == '-':
                saida = self.adaptaData('select', data.get())

            else:

                for char in data.get():
                    if char.isdecimal():
                        # 01/34/6789
                        if len(saida) == 2 or len(saida) == 5:
                            saida += '/'
                        saida += char

            self.entryVisitas[index].delete(0, 'end')
            self.entryVisitas[index].insert('end', saida)

            if len(data.get()) > 10:
                data.set(data.get()[:10])
            del saida
            return

        # ------------------------HORARIO------------------------------------------------
        elif index == 2:
            horario = self.variaveisVisitas[index]

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

            self.entryVisitas[index].delete(0, 'end')
            self.entryVisitas[index].insert('end', saida)

            if len(horario.get()) > 8:
                horario.set(horario.get()[:8])
            del saida
        # ------------------------DESCRICAO----------------------------------------------
        elif index == 3:
            descricao = self.entryVisitas[index]

            saida = descricao.get(0.0, 'end')
            descricao.delete(0.0, 'end')

            if len(saida) > DESCRICAO_SIZE:
                descricao.insert(0.0, saida[:DESCRICAO_SIZE].upper())
            else:
                descricao.insert(0.0, saida.upper())

            del saida
            return
        return

    def proximo(self, evt=None):
        if isinstance(evt, tk.Event):
            w = evt.widget
        else:
            w = self.entryVisitas[evt]
        column = ["Número do Chamado", "Data",
                  "Horario", "Resolvido"]

        # ------------------------Descricao--------------------------------------
        if w is self.entryVisitas[3]:
            w.tk_focusNext().focus()
            return 'break'

        # ------------------------NUMERO DO CHAMADO--------------------------------------
        if w is self.entryVisitas[0] and self.variaveisVisitas[0].get() != "":
            cursor = self.DB.cursor()

            cursor.execute(f"SELECT num_chamado FROM chamadas WHERE num_chamado like '%{w.get()}%'")
            chamada = cursor.fetchall()
            cursor.close()
            if (len(chamada) <= 0 and self.new.get()) \
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
                    popUP(parent=self, instance='CV').montarTreeColunaUnica(select, "Número do Chamado", 0)

                    if self.err is True:
                        self.clearEntry()
                        self.err = False
                        return 'break'

                elif len(select) <= 0:
                    tk.messagebox.showerror(title="Chamado Não Encontrado.",
                                            message="Não foi possivel localizar este número de chamado.",
                                            parent=self
                                            )
                    self.clearEntry()
                    self.entryVisitas[0].focus()
                    return 'break'
                else:
                    w.delete(0, 'end')
                    w.insert(0, chamada)

                if self.new.get() == False:

                    chamada = w.get()

                    cursor = self.DB.cursor()

                    cursor.execute(
                        "SELECT num_chamado, data_visita, hora_visita, observacao,\
                    resolvido FROM visitas WHERE %s = '%s' "
                        % (self.dicLabels[w], chamada)
                    )

                    tmp = list(cursor.fetchall())
                    cursor.close()

                    if len(tmp) == 0:
                        tk.messagebox.showwarning(title="Visita Não Encontrada!",
                                                  message="Nenhuma visita registrada para este número de chamado.",
                                                  parent=self)
                        self.new.set(True)
                    else:
                        select = []
                        for s in tmp:
                            s = list(s)
                            s[1] = self.adaptaData('select', s[1])
                            s[4] = "Sim" if s[4] == 1 else "Não"
                            select.append(s)

                        del tmp
                        popUP(parent=self, instance='CV').montarTree(column, select)
                        if self.err is True:
                            self.clearEntry()
                            self.err = False
                            return 'break'



        # ------------------------Restante----------------------------------------
        elif w.get() != "":
            if self.new.get() == False:
                cursor = self.DB.cursor()
                if self.dicLabels[w] == 'data_visita':
                    if len(w.get()) < 10:
                        tk.messagebox.showwarning(title="Data Invalida",
                                                  message="Data Invalida",
                                                  parent=self)
                        return
                    select = self.adaptaData('insert', w.get())
                else:
                    select = "%" + w.get() + "%"

                cursor.execute(
                    "SELECT num_chamado, data_visita, hora_visita, observacao,\
resolvido FROM Visitas WHERE %s LIKE '%s'"
                    % (self.dicLabels[w], select)
                )

                tmp = list(cursor.fetchall())
                select = []

                for s in tmp:
                    s = list(s)
                    s[1] = self.adaptaData('select', s[1])
                    select.append(s)

                del tmp

                w.delete(0, 'end')

                popUP(parent=self, instance='CV').montarTree(column, select)
                if self.err is True:
                    self.clearEntry()
                    self.err = False
                    return 'break'

                cursor.close()
        w.tk_focusNext().focus()
        return

    def clearEntry(self, start=0):
        for label in self.labelVisitas:
            label['fg'] = '#000000'

        for var in range(start, len(self.variaveisVisitas)):
            if var == 3:
                continue
            elif var == 4:
                self.variaveisVisitas[var].set(True)
            else:
                self.variaveisVisitas[var].set("")

        for entry in range(start, 3):
            self.entryVisitas[entry].delete(0, 'end')

        self.entryVisitas[3].delete(0.0, 'end')
        self.entryVisitas[0].focus()
        self.new.set(True)
        self.err = False

    def today(self, evt):
        w = evt.widget
        if w == self.entryVisitas[1]:
            dia = strftime("%d")
            mes = strftime("%m")
            ano = strftime("%Y")
            self.variaveisVisitas[1].set("%s/%s/%s" % (dia, mes, ano))
        elif w == self.entryVisitas[2]:
            self.variaveisVisitas[2].set(strftime("%X"))

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
        return self.entryVisitas
