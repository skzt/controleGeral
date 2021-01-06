"""
Created on 30 de maio de 2016

@author: Pedro Vaz
"""
import os
from time import strftime
from tkinter import Text, END, DISABLED, NORMAL, Checkbutton, IntVar, LabelFrame
from tkinter import Toplevel, Entry, Label, StringVar, Button, font
from tkinter import messagebox, RIGHT, Scrollbar, BOTH

from Manutencao.Constantes import ENCODING
from .Config import get_secret
from .Functions import functions
from .toolTip import ToolTip


class filtrar:

    def __init__(self, parent):
        self.parent = parent
        self.pathLocation = get_secret("MAIN_PATH")
        self.func = functions(self)
        self.contador = None
        self.mesDe = StringVar()
        self.anoDe = StringVar()
        self.anoAte = StringVar()
        self.mesAte = StringVar()

    def Filtrar(self):

        self.top = Toplevel(self.parent)
        self.top.wm_title("Filtrar Pedidos")
        self.top.geometry("391x370+100+50")

        self.contador = 0
        self.anoDe.set(strftime("%Y"))
        self.mesDe.set(self.func.getMes(strftime("%B")))
        self.anoAte.set("")
        self.mesAte.set("")

        check = IntVar()
        check.set(0)

        # Apartir desta data
        # =========================A PARTIR DE==========================================

        labelDe = Label(self.top)
        labelDe['text'] = "A partir de:"
        labelDe.place(y=5, x=5)

        labelAno = Label(self.top)
        labelAno['text'] = "Ano"
        labelAno.place(y=20, x=50)

        self.entryAnoDe = Entry(self.top)
        self.entryAnoDe["textvariable"] = self.anoDe
        self.entryAnoDe.textvariable = self.anoDe
        self.entryAnoDe["width"] = 4
        self.entryAnoDe.focus()
        self.entryAnoDe.bind("<Return>", self.setNext)
        self.entryAnoDe.place(y=40, x=50)

        labelMes = Label(self.top)
        labelMes["text"] = "Mes"
        labelMes.place(y=60, x=50)

        self.entryMesDe = Entry(self.top)
        self.entryMesDe["textvariable"] = self.mesDe
        self.entryMesDe.textvariable = self.mesDe
        self.entryMesDe["width"] = 10
        self.entryMesDe.bind("<Return>", self.setNext)
        self.entryMesDe.place(y=80, x=50)
        # =========================ATE==================================================
        self.frame = LabelFrame(self.top)
        self.frame['width'] = 100
        self.frame['height'] = 117
        self.frame['borderwidth'] = 3
        self.frame.place(y=2, x=125)

        self.checkBox = Checkbutton(self.frame)
        self.checkBox['text'] = "Até"
        self.checkBox['variable'] = check
        self.checkBox['command'] = lambda: self.ativaAte(check.get())
        self.checkBox['onvalue'] = 1
        self.checkBox['offvalue'] = 0
        self.checkBox.variable = check
        self.checkBox.place(y=1, x=2)

        labelAno = Label(self.frame)
        labelAno['text'] = "Ano"
        labelAno.place(y=20, x=5)

        self.entryAnoAte = Entry(self.frame)
        self.entryAnoAte["state"] = DISABLED
        self.entryAnoAte["width"] = 4
        self.entryAnoAte['textvariable'] = self.anoAte
        self.entryAnoAte.bind("<Return>", self.setNext)
        self.entryAnoAte.place(y=40, x=5)

        labelMes = Label(self.frame)
        labelMes["text"] = "Mes"
        labelMes.place(y=60, x=5)

        self.entryMesAte = Entry(self.frame)
        self.entryMesAte["state"] = DISABLED
        self.entryMesAte["width"] = 10
        self.entryMesAte['textvariable'] = self.mesAte
        self.entryMesAte.bind("<Return>", self.setNext)
        self.entryMesAte.place(y=80, x=5)
        # =========================FILTRO===============================================

        labelEntry = Label(self.top)
        labelEntry['text'] = "Filtro"
        labelEntry.place(y=20, x=265)

        self.entryFiltro = Entry(self.top)
        self.entryFiltro['width'] = 15
        self.entryFiltro.bind("<Return>", lambda _: self.getFiltrado())
        self.entryFiltro.place(y=40, x=240)

        # =======================================================================
        # LABEL PARA COMPLETAR ESPAÇOS
        # =======================================================================

        Label(self.top).pack()
        Label(self.top).pack()
        Label(self.top).pack()
        Label(self.top).pack()
        Label(self.top).pack()
        Label(self.top).pack()
        Label(self.top).pack()
        # -----------------------------------------------------------------------
        self.scrollbar = Scrollbar(self.top)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)

        self.customFont = font.Font(family="Arial", size=10)
        self.textFrame = Text(self.top)
        self.textFrame['font'] = self.customFont
        self.textFrame['height'] = 11
        self.textFrame['width'] = 51
        self.textFrame['borderwidth'] = 3
        self.textFrame['takefocus'] = False
        self.textFrame['yscrollcommand'] = self.scrollbar.set
        self.textFrame.yscrollcommand = self.scrollbar.set
        self.textFrame.place(y=160, x=5)

        self.scrollbar['command'] = self.textFrame.yview
        self.scrollbar.command = self.textFrame.yview

        self.labelTotal = Label(self.top)
        self.labelTotal['text'] = "Total de pedidos: 0"
        self.labelTotal.place(y=345, x=3)

        buttonFiltrar = Button(self.top)
        buttonFiltrar['text'] = "Filtrar"
        buttonFiltrar['command'] = self.getFiltrado
        buttonFiltrar.bind("<Return>", lambda _: self.getFiltrado())
        buttonFiltrar.place(y=130, x=80)

        button_limpar = Button(self.top)
        button_limpar['text'] = "Limpar Resultados"
        button_limpar['command'] = self.limpar_resultados
        button_limpar.bind("<Return>", lambda _: self.limpar_resultados())
        button_limpar.place(y=130, x=130)

        buttonCancel = Button(self.top)
        buttonCancel['text'] = "Voltar"
        buttonCancel['command'] = self.top.destroy
        buttonCancel.bind("<Return>", lambda _: self.top.destroy())
        buttonCancel.place(y=130, x=250)

        # toolTips
        ToolTip(self.entryAnoDe, "Exemplos:\n2016\n2015\n2014")
        ToolTip(self.entryMesDe, "Exemplos:\nAbril\nDezembro\nJaneiro")
        ToolTip(self.entryFiltro, "Exemplos:\nURA\n15/04/16\nJoão")
        msg = "Marque caso queira obter resultados\napartir de uma faixa de data."
        ToolTip(self.checkBox, msg)

    def limpar_resultados(self):
        self.textFrame['state'] = NORMAL
        self.textFrame.delete(1.0, END)
        self.contador = 0
        self.labelTotal.config(text=f"Total de pedidos: {self.contador}")
        self.textFrame['state'] = DISABLED
        self.entryAnoDe.focus()

    def getListas(self):
        ano = []
        listasMeses = []

        meses = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
                 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO',
                 'DEZEMBRO'
                 ]

        # ===============================================================================
        #                             EXCEPTIONS
        # ===============================================================================
        def mudarCor(key, cor):
            entry = {
                0: self.entryAnoAte,
                1: self.entryAnoDe,
                2: self.entryMesAte,
                3: self.entryMesDe,
            }
            if key == 4:
                for i in range(4):
                    entry[i].config(fg=cor)

            elif key >= 4:
                for i in range(4):
                    if i != (key - 5):
                        entry[i].config(fg=cor)
            else:
                entry[key].config(fg=cor)
        try:
            anoDe = int(self.anoDe.get())
            mesDe = self.mesDe.get().upper()

            if anoDe <= 2015:
                self.entryAnoDe.focus()
                mudarCor(1, 'red')  # AnoDe RED
                mudarCor(6, 'black')  # Restante BLACK
                messagebox.showwarning("ERRO", "Ano Invalido",
                                       parent=self.top
                                       )
                return ("ERRO", "ERRO")

            elif mesDe not in meses:
                self.entryMesDe.focus()
                mudarCor(3, 'red')  # MesDeDe RED
                mudarCor(8, 'black')  # Restante BLACK
                messagebox.showwarning("ERRO", "Mes Invalido",
                                       parent=self.top
                                       )
                return ("ERRO", "ERRO")

        except ValueError:
            if self.anoDe.get() != "":
                self.entryAnoDe.focus()
                mudarCor(1, 'red')  # AnoDe RED
                mudarCor(6, 'black')  # Restante BLACK
                messagebox.showwarning("ERRO", "Ano Invalido",
                                       parent=self.top
                                       )
                return ("ERRO", "ERRO")

        if self.anoAte.get() == "" and self.mesAte.get().upper() == "":
            anoAte = int(self.anoDe.get())
            mesAte = self.mesDe.get().upper()

        else:
            try:
                anoAte = int(self.anoAte.get())
                mesAte = self.mesAte.get().upper()
                if self.anoDe.get() == "":
                    anoDe = anoAte
                    mesDe = mesAte

                if anoAte <= 2015:
                    self.entryAnoAte.focus()
                    mudarCor(0, 'red')  # AnoAte RED
                    mudarCor(5, 'black')  # Restante BLACK
                    messagebox.showwarning("ERRO", "Ano Invalido",
                                           parent=self.top
                                           )
                    return ("ERRO", "ERRO")

                elif anoAte < anoDe:
                    self.entryAnoDe.focus()
                    mudarCor(0, 'red')  # AnoAte e AnoDe RED
                    mudarCor(5, 'black')  # Restante BLACK
                    mudarCor(1, 'red')
                    msg = """Ano "De" tem de ser maior que Ano "Ate" """
                    messagebox.showwarning("ERRO", msg,
                                           parent=self.top
                                           )
                    return ("ERRO", "ERRO")


                elif mesAte not in meses:
                    self.entryMesAte.focus()
                    mudarCor(2, 'red')  # MesAte RED
                    mudarCor(7, 'black')  # Restante BLACK
                    messagebox.showwarning("ERRO", "Mes Invalido",
                                           parent=self.top
                                           )
                    return ("ERRO", "ERRO")

                elif anoAte == anoDe:
                    if meses.index(mesDe) > meses.index(mesAte):
                        self.entryMesDe.focus()

                        mudarCor(2, 'red')  # MesAte e MesDe RED
                        mudarCor(7, 'black')  # Restante BLACK
                        mudarCor(3, 'red')
                        msg = """Mes "De" tem de ser anterior ao Mes "Ate"
                        Exemplo:
    Mes De: Junho
    Mes Até: Julho """
                        messagebox.showwarning("ERRO", msg,
                                               parent=self.top
                                               )
                        return ("ERRO", "ERRO")

            except ValueError:
                self.entryAnoAte.focus()
                self.entryAnoAte['fg'] = 'red'
                mudarCor(0, 'red')  # AnoAte RED
                mudarCor(5, 'black')  # Restante BLACK
                messagebox.showwarning("ERRO", "Ano Invalido",
                                       parent=self.top
                                       )
                return ("ERRO", "ERRO")

        mudarCor(4, 'black')  # TODOS BALCK

        # ===============================================================================
        #                             Função
        # ===============================================================================

        for x in range(anoDe, anoAte + 1):
            ano.append(x)
            aux = []

            if anoDe == anoAte:

                if mesDe == mesAte:
                    listasMeses.append([mesDe])

                else:
                    for i in range(meses.index(mesDe), meses.index(mesAte) + 1):
                        aux.append(meses[i])

                    listasMeses.append(aux)

            elif x != anoDe and x != anoAte:
                listasMeses.append(meses)

            elif x == anoDe:
                index = meses.index(mesDe)
                for i in range(index, 12):
                    aux.append(meses[i])

                listasMeses.append(aux)

            else:
                index = meses.index(mesAte)
                for i in range(0, index + 1):
                    aux.append(meses[i])

                listasMeses.append(aux)
        return (ano, listasMeses)

    def getFiltrado(self):

        anos, meses = self.getListas()
        if anos == "ERRO" or meses == "ERRO":
            return

        if self.textFrame.get(1.0) != '\n':
            self.textFrame['state'] = NORMAL
            self.textFrame.delete(1.0, END)
            self.contador = 0

        self.textFrame['state'] = NORMAL

        for cont in range(len(anos)):
            mes = meses[cont]
            y = anos[cont]
            for m in mes:
                try:
                    _path = os.path.abspath(os.path.join(self.pathLocation, str(y), f"{m}.cfg"))
                    with open(_path, 'r', encoding=ENCODING) as file:

                        lines = file.readlines()[1:]
                        for line in lines:
                            if self.entryFiltro.get().upper() in line.rstrip().upper():
                                self.textFrame.insert(END, line.rstrip() + "\n")
                                self.contador += 1

                            else:
                                self.contador += 0

                        self.labelTotal.config(text=f"Total de pedidos: {self.contador}")

                except IOError:
                    message = """Arquivo %s/%s.cfg não localizado!""" % (y, m)
                    messagebox.showwarning("Erro!", message,
                                           parent=self.top)

        self.textFrame['state'] = DISABLED

    def ativaAte(self, flag):
        toolTipAno = ToolTip(self.entryAnoAte, "Exemplos:\n2016\n2015\n2014")

        toolTipMes = ToolTip(self.entryMesAte, "Exemplos:\nAbril\nDezembro\nJaneiro")

        if flag == 1:
            self.entryAnoAte.config(state=NORMAL)
            self.entryAnoDe.focus()
            self.entryMesAte.config(state=NORMAL)
            self.frame['borderwidth'] = 0

            toolTipAno.startShowing()
            toolTipMes.startShowing()

            self.anoAte.set(self.anoDe.get())
            self.mesAte.set(self.mesDe.get().upper())
            self.anoDe.set("")
            self.mesDe.set("")


        else:
            self.anoDe.set(self.anoAte.get())
            self.mesDe.set(self.mesAte.get().upper())
            self.anoAte.set("")
            self.mesAte.set("")

            self.entryAnoAte.config(state=DISABLED)
            self.entryMesAte.config(state=DISABLED)
            self.entryFiltro.focus()
            self.frame['borderwidth'] = 3

            toolTipAno.stopShowing()
            toolTipMes.stopShowing()

    def setNext(self, event):
        event.widget.tk_focusNext().focus()
        return ("break")
