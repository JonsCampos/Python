import tkinter as tk
from tkinter import ttk
import classcrud
import acesso

def voltar(janelaMenu, janelaMain):
    janelaMain.deiconify()
    janelaMenu.destroy()

def menu(nvl, janelaMain):
    # Janela
    janelaMenu = tk.Toplevel()
    x, y = 800, 500
    posx, posy = int((janelaMenu.winfo_screenwidth()-x)/2), int((janelaMenu.winfo_screenheight()-y)/2)
    janelaMenu.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaMenu.resizable(False, False)
    janelaMenu.iconbitmap('icon.ico')
    janelaMenu.title('Sistema de Controle de acesso')
    janelaMain.withdraw()
    janelaMenu.protocol("WM_DELETE_WINDOW", lambda: voltar(janelaMenu, janelaMain))

    # Título
    ttk.Label(janelaMenu, text='Menu', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ttk.Label(janelaMenu, text=nvl[0], font=(12)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Button - Acesso
    acessobtn = tk.Button(janelaMenu, text='Acesso', command=lambda: acesso.acesso(nvl, janelaMenu))
    acessobtn.place(relx=0.5, rely=0.1666, anchor=tk.CENTER)

    # Button - Sair
    sairbtn = tk.Button(janelaMenu, text='Sair', command=lambda: voltar(janelaMenu, janelaMain))
    sairbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    janelaMenu.mainloop()