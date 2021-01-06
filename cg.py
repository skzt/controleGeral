"""
Created on 17 de maio de 2016

    Main File da aplicação. Responsavel pela tela inicial.

@author: Pedro Vaz
@version: 2.0
"""
import os
from tkinter import Frame, Label, Button, PhotoImage, Tk
from tkinter import messagebox

from Ferramentas import Pedidos, Filtrar, Config
from Manutencao.GerenciadorManutencao import MainWindow


class MainApp(Frame):
    def __init__(self, parent, *arg, **kwarg):
        Frame.__init__(self, *arg, **kwarg)

        # app -> Frame Inicial
        self.app = parent
        self.app.focus()
        self.app.bind("<Escape>", self.sureQuit)

        # framePedido -> Frame de prencher pedidos.
        self.framePedido = Pedidos.pedidos(self.app)
        self.frameFiltrar = Filtrar.filtrar(self.app)
        self.pathLocation = Config.get_secret("MAIN_PATH")

    def Inicial(self):

        # Insere o Logo da empresa na tela inicial.
        imageObject = PhotoImage(file=os.path.abspath(os.path.join(self.pathLocation, 'poli.gif')))

        labelImagem = Label(self.app)
        labelImagem['image'] = imageObject
        labelImagem.image = imageObject
        labelImagem.pack(side="top", pady=(20, 0))

        # Botão para adicionar novos pedidos.
        addButton = Button(self.app)
        addButton['text'] = "Adicionar Pedido"
        addButton['width'] = 20
        addButton['command'] = lambda: self.framePedido.addPedido(imageObject)
        addButton.bind("<Return>", lambda _: self.framePedido.addPedido(imageObject))
        self.app.bind("<Control-n>", lambda _: self.framePedido.addPedido(imageObject))
        addButton.place(y=176, x=52)

        #         #Botão para fazer busca nos pedidos.
        #         buscarButton = Button(self.app)
        #         buscarButton['text'] = "Buscar Pedido"
        #         buscarButton['width'] =20
        #         buscarButton['command'] = emObras
        #         buscarButton.bind("<Return>", lambda _ : emObras())
        #         buscarButton.place(y = 176, x = 299)

        # Botão para filtrar pedidos.
        filtraButton = Button(self.app)
        filtraButton['text'] = "Filtrar Pedidos"
        filtraButton['width'] = 20
        filtraButton['command'] = self.frameFiltrar.Filtrar
        filtraButton.bind("<Return>", lambda _: self.frameFiltrar.Filtrar())
        self.app.bind("<Control-f>", lambda _: self.frameFiltrar.Filtrar())
        filtraButton.place(y=176, x=299)
        #         filtraButton.place(y = 243, x = 52)

        # Botão para Acessar o Modulo de Chamadas de Manutenção
        manutencaoButton = Button(self.app)
        manutencaoButton['text'] = "Chamadas de Manutenção"
        manutencaoButton['command'] = lambda: MainWindow(self.app)
        manutencaoButton.place(y=243, x=52)

        # Botão para sair da aplicação.
        exitButton = Button(self.app)
        exitButton['text'] = "Sair"
        exitButton['width'] = 20
        # exitButton['command'] = self.sureQuit
        exitButton['command'] = self.sureQuit
        exitButton.bind("<Return>", lambda event: self.sureQuit(event))
        #         exitButton.place(y = 243, x = 299)
        exitButton.place(y=243, x=299)

    def sureQuit(self, event=None):
        """
            Verifica se o usuário realmente deseja fechar o programa.
        """
        message = "Tem certeza que deseja fechar completamente o programa?"

        widget = "Tk" if event is None else event.widget

        if messagebox.askyesno("Fechar Programa", message):
            # YES
            if type(widget) != "Tk":
                self.app.destroy()
            else:
                widget.destroy()
        else:
            # NO
            if type(widget) != "Tk":
                self.app.tk_focusNext().focus()
            else:
                widget.focus()



if __name__ == '__main__':
    # Cria a tela inicial da aplicação.
    root = Tk()
    root.title("Controle Geral de Impressões")
    root.geometry("600x400")
    MainApp(root).Inicial()
    root.mainloop()
