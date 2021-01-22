"""
Created on 19 de set de 2017

@author: Pedro Vaz
"""

import tkinter as tk
import tkinter.ttk as ttk

import pymysql as sql

from Ferramentas.Config import get_secret
from Manutencao.ControleChamadas import ControleChamadas
from Manutencao.ControlePecas import ControlePecas
from Manutencao.ControleVisistas import ControleVisitas
from Manutencao.ValidaCI import ValidaCI

TESTE_CONST = 10


class MainWindow(tk.Toplevel):
    """
    classdocs
    """

    def __init__(self, *arg, **kwarg):
        """
        Constructor
        """
        tk.Toplevel.__init__(self, *arg, **kwarg)
        self.grab_set()
        self.title("Menu de Chamadas de Manutenção")
        # self.transient(self.master)
        self.__DB = None
        self.__cc = None
        self.__cv = None
        self.__cp = None
        self.__vci = None
        self.gui()

    def gui(self):

        self.bind_all("<F2>", self.clearEntry)
        self.bind_all("<F4>", self.changeCheck)
        self.bind("<Escape>", lambda _: self.sair())
        mainWindow = ttk.Notebook(self)

        mainWindow['padding'] = 10
        mainWindow['takefocus'] = False
        print(get_secret("DB_HOST"))
        self.__DB = sql.connect(host=get_secret("DB_HOST"),
                                user=get_secret("DB_USER"),
                                password=get_secret("DB_PW"),
                                database=get_secret("DB_SCHEMA"))

        self.__cc = ControleChamadas(self, self.DB)
        self.__cv = ControleVisitas(self, self.DB)
        self.__cp = ControlePecas(self, self.DB)
        self.__vci = ValidaCI(self)

        mainWindow.add(self.__cc.frame, text="Controle de Chamadas")
        mainWindow.add(self.__cv.frame, text="Controle de Visitas")
        mainWindow.add(self.__cp.frame, text="Controle de Peças")
        mainWindow.add(self.__vci.frame, text="Validar CI")

        self.bind("<Control-Key-1>", lambda _: mainWindow.select(self.__cc.frame))
        self.bind("<Control-Key-2>", lambda _: mainWindow.select(self.__cv.frame))
        self.bind("<Control-Key-3>", lambda _: mainWindow.select(self.__cp.frame))
        self.bind("<Control-Key-4>", lambda _: mainWindow.select(self.__vci.frame))
        mainWindow.pack()
        self.__cc.entradas[0].focus()

        exitButton = tk.Button(self)
        exitButton['text'] = "Sair"
        exitButton['command'] = self.sair
        exitButton['relief'] = 'groove'
        exitButton['bd'] = 6
        exitButton['takefocus'] = False
        exitButton.pack()
        self.wait_window(self)

    def sair(self):
        self.DB.close()
        self.destroy()

    def clearEntry(self, evt):
        w = evt.widget

        # começa com quem tem o foco(chamou o evento) ->
        # pega o pai dele ->
        # pega o pai do pai, que é uma das 3 classes (CC, CV ou CP)
        # chama clearEntry() nessa classe
        if w.master.master is self.__cc:
            self.__cc.clearEntry()

        elif w.master.master is self.__cv:
            self.__cv.clearEntry()

        elif w.master.master is self.__cp:
            self.__cp.clearEntry()

        elif w.master.master is self.__vci:
            index = True if w.master['text'] == "Validar" else False
            self.__vci.clearEntry(index)
        return

    def changeCheck(self, evt):
        w = evt.widget
        if w.master.master is self.__cv:
            self.__cv.new.set(not self.__cv.new.get())

        elif w.master.master is self.__cp:
            self.__cp.new.set(not self.__cp.new.get())
            self.__cp.changeNew()

    @property
    def DB(self):
        return self.__DB
