import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud
import acesso
import setor
import funcionario
import usuario
import local

def menu(janela):
    if (janela):
        janela.destroy()

    # Janela
    janelaMenu = tk.Tk()
    x, y = 800, 500
    posx, posy = int((janelaMenu.winfo_screenwidth()-x)/2), int((janelaMenu.winfo_screenheight()-y)/2)
    janelaMenu.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaMenu.minsize(x, y)
    janelaMenu.maxsize(x, y)
    janelaMenu.iconbitmap('icon.ico')
    janelaMenu.title('Sistema de Controle de acesso')

    # Título
    ttk.Label(janelaMenu, text='Menu', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Button - Acesso
    acessobtn = tk.Button(janelaMenu, text='Acesso', command=lambda: acesso.acesso(janelaMenu))
    acessobtn.place(relx=0.5, rely=0.1666, anchor=tk.CENTER)

    # Button - Setor
    setorbtn = tk.Button(janelaMenu, text='Setor', command=lambda: setor.setor(janelaMenu))
    setorbtn.place(relx=0.5, rely=0.3332, anchor=tk.CENTER)

    # Button - Funcionario
    funcionariobtn = tk.Button(janelaMenu, text='funcionário', command=lambda: funcionario.funcionario(janelaMenu))
    funcionariobtn.place(relx=0.5, rely=0.4998, anchor=tk.CENTER)

    # Button - Usuario
    usuariobtn = tk.Button(janelaMenu, text='usuário', command=lambda: usuario.usuario(janelaMenu))
    usuariobtn.place(relx=0.5, rely=0.6664, anchor=tk.CENTER)

    # Button - Local
    localbtn = tk.Button(janelaMenu, text='Local', command=lambda: local.local(janelaMenu))
    localbtn.place(relx=0.5, rely=0.833, anchor=tk.CENTER)

    janelaMenu.mainloop()