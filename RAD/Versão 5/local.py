import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud
import menu

def local(janelaMenu):
    if (janelaMenu):
        janelaMenu.destroy()

    # Janela
    janelaLocal = tk.Tk()
    x, y = 800, 500
    posx, posy = int((janelaLocal.winfo_screenwidth()-x)/2), int((janelaLocal.winfo_screenheight()-y)/2)
    janelaLocal.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaLocal.minsize(x, y)
    janelaLocal.maxsize(x, y)
    janelaLocal.iconbitmap('icon.ico')
    janelaLocal.title('Sistema de Controle de acesso')

    # Criação das tabelas (caso não exista)
    classcrud.tabelas()

    # Título
    ttk.Label(janelaLocal, text='Locais', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do local
    labelIDL = ttk.Label(text='ID do local')
    labelIDL.place(relx=0.33, rely=0.16, anchor=tk.CENTER)
    IDLocal = tk.Entry(janelaLocal)
    IDLocal.place(relx=0.33, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do local
    labelNLocal = ttk.Label(text='Nome')
    labelNLocal.place(relx=0.66, rely=0.16, anchor=tk.CENTER)
    nomeLocal = tk.Entry(janelaLocal)
    nomeLocal.place(relx=0.66, rely=0.21, anchor=tk.CENTER)

    # TreeView
    colunas = ('ID', 'Nome')            
    treeLocal = ttk.Treeview(janelaLocal,columns=colunas, selectmode='browse')
    treeLocal['show'] = 'headings'
    # Scrollbar
    scroll = ttk.Scrollbar(janelaLocal, orient='vertical', command=treeLocal.yview)        
    scroll.pack(side ='right', fill ='x')
    treeLocal.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.686, rely=0.7, anchor=tk.CENTER, height=224)
    # Cabeçalho
    treeLocal.heading('ID', text='ID')
    treeLocal.heading('Nome', text='Nome')
    # Colunas
    treeLocal.column('ID',minwidth=0,width=140, anchor=tk.CENTER)
    treeLocal.column('Nome',minwidth=0,width=140, anchor=tk.CENTER)
    treeLocal.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Button - Inserir
    inserirbtn = tk.Button(janelaLocal, text='Inserir', command=lambda: classcrud.insertLocal(nomeLocal, treeLocal))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = tk.Button(janelaLocal, text='Atualizar', command=lambda: classcrud.updateLocal(IDLocal, nomeLocal, treeLocal))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = tk.Button(janelaLocal, text='Remover', command=lambda: classcrud.deleteLocal(IDLocal, treeLocal))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    voltarbtn = tk.Button(janelaLocal, text='Voltar', command=lambda: menu.menu(janelaLocal))
    voltarbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeLocal(treeLocal)

    janelaLocal.mainloop()
