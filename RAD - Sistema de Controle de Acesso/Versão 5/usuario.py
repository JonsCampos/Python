import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud
import menu

def usuario(janelaMenu):
    if (janelaMenu):
        janelaMenu.destroy()

    # Janela
    janelaUsuario = tk.Tk()
    x, y = 800, 500
    posx, posy = int((janelaUsuario.winfo_screenwidth()-x)/2), int((janelaUsuario.winfo_screenheight()-y)/2)
    janelaUsuario.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaUsuario.minsize(x, y)
    janelaUsuario.maxsize(x, y)
    janelaUsuario.iconbitmap('icon.ico')
    janelaUsuario.title('Sistema de Controle de acesso')

    # Criação das tabelas (caso não exista)
    classcrud.tabelas()

    # Título
    ttk.Label(janelaUsuario, text='Usuários', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Entry - ID Usuário
    labelIDUsu = ttk.Label(text='ID do usuário')
    labelIDUsu.place(relx=0.2, rely=0.16, anchor=tk.CENTER)
    IDUsuario = tk.Entry(janelaUsuario)
    IDUsuario.place(relx=0.2, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome usuário
    labelNUsuario = ttk.Label(text='Nome de usuário')
    labelNUsuario.place(relx=0.4, rely=0.16, anchor=tk.CENTER)
    nomeUsuario = tk.Entry(janelaUsuario)
    nomeUsuario.place(relx=0.4, rely=0.21, anchor=tk.CENTER)

    # Entry - Senha
    labelSenha = ttk.Label(text='Senha')
    labelSenha.place(relx=0.6, rely=0.16, anchor=tk.CENTER)
    senhaUsuario = tk.Entry(janelaUsuario, show='*')
    senhaUsuario.place(relx=0.6, rely=0.21, anchor=tk.CENTER)

    # Entry - ID Funcionário
    labelSenha = ttk.Label(text='ID do funcionário')
    labelSenha.place(relx=0.8, rely=0.16, anchor=tk.CENTER)
    IDFuncionario = tk.Entry(janelaUsuario)
    IDFuncionario.place(relx=0.8, rely=0.21, anchor=tk.CENTER)

    # TreeView
    colunas = ('ID', 'Nome de usuário', 'Funcionário')            
    treeUsuario = ttk.Treeview(janelaUsuario,columns=colunas, selectmode='browse')
    treeUsuario['show'] = 'headings'
    # Scrollbar
    scroll = ttk.Scrollbar(janelaUsuario, orient='vertical', command=treeUsuario.yview)        
    scroll.pack(side ='right', fill ='x')
    treeUsuario.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.749, rely=0.7, anchor=tk.CENTER, height=224)
    # Cabeçalho
    treeUsuario.heading('ID', text='ID')
    treeUsuario.heading('Nome de usuário', text='Nome de usuário')
    treeUsuario.heading('Funcionário', text='Funcionário')
    # Colunas
    treeUsuario.column('ID',minwidth=0,width=100, anchor=tk.CENTER)
    treeUsuario.column('Nome de usuário',minwidth=0,width=140, anchor=tk.CENTER)
    treeUsuario.column('Funcionário',minwidth=0,width=140, anchor=tk.CENTER)
    treeUsuario.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Button - Inserir
    inserirbtn = tk.Button(janelaUsuario, text='Inserir', command=lambda: classcrud.insertUsuario(nomeUsuario, senhaUsuario, IDFuncionario , treeUsuario))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = tk.Button(janelaUsuario, text='Atualizar', command=lambda: classcrud.updateUsuario(IDUsuario, nomeUsuario, senhaUsuario, treeUsuario))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = tk.Button(janelaUsuario, text='Remover', command=lambda: classcrud.deleteUsuario(IDUsuario, treeUsuario))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    voltarbtn = tk.Button(janelaUsuario, text='Voltar', command=lambda: menu.menu(janelaUsuario))
    voltarbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeUsuario(treeUsuario)

    janelaUsuario.mainloop()
