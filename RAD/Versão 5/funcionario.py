import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud
import menu

def funcionario(janelaMenu):
    if (janelaMenu):
        janelaMenu.destroy()

    # Janela
    janelaFuncionario = tk.Tk()
    x, y = 800, 500
    posx, posy = int((janelaFuncionario.winfo_screenwidth()-x)/2), int((janelaFuncionario.winfo_screenheight()-y)/2)
    janelaFuncionario.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaFuncionario.minsize(x, y)
    janelaFuncionario.maxsize(x, y)
    janelaFuncionario.iconbitmap('icon.ico')
    janelaFuncionario.title('Sistema de Controle de acesso')

    # Criação das tabelas (caso não exista)
    classcrud.tabelas()

    # Título
    ttk.Label(janelaFuncionario, text='Funcionários', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do funcionário
    labelIDF = ttk.Label(text='ID do Funcionário')
    labelIDF.place(relx=0.2, rely=0.16, anchor=tk.CENTER)
    IDFuncionario = tk.Entry(janelaFuncionario)
    IDFuncionario.place(relx=0.2, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do funcionário
    labelNFuncionario = ttk.Label(text='Nome do Funcionário')
    labelNFuncionario.place(relx=0.4, rely=0.16, anchor=tk.CENTER)
    nomeFuncionario = tk.Entry(janelaFuncionario)
    nomeFuncionario.place(relx=0.4, rely=0.21, anchor=tk.CENTER)

    # Entry - E-mail do funcionário
    labelEmailFuncionario = ttk.Label(text='E-Mail do Funcionário')
    labelEmailFuncionario.place(relx=0.6, rely=0.16, anchor=tk.CENTER)
    emailFuncionario = tk.Entry(janelaFuncionario)
    emailFuncionario.place(relx=0.6, rely=0.21, anchor=tk.CENTER)

    # Entry - ComboBox do setor do funcionário
    labelSFuncionario = ttk.Label(text='Setor do Funcionário')
    labelSFuncionario.place(relx=0.8, rely=0.16, anchor=tk.CENTER)
    setorFuncionario = ttk.Combobox(janelaFuncionario, state='readonly')
    setorFuncionario.place(relx=0.8, rely=0.21, anchor=tk.CENTER)

    # Preenchimento do ComboBox de Setor
    registros = classcrud.fillComboboxSetor()
    if registros == []:
        setorFuncionario['values'] = ['Sem registros']
    else:
        setorFuncionario['values'] = [registro[0] for registro in registros]
    setorFuncionario.current(0)

    # TreeView
    colunas = ('ID', 'Nome', 'Email', 'Setor')            
    treeFuncionario = ttk.Treeview(janelaFuncionario,columns=colunas, selectmode='browse')
    treeFuncionario['show'] = 'headings'
    # Scrollbar
    scroll = ttk.Scrollbar(janelaFuncionario, orient='vertical', command=treeFuncionario.yview)        
    scroll.pack(side ='right', fill ='x')
    treeFuncionario.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.861, rely=0.7, anchor=tk.CENTER, height=224)
    # Cabeçalho
    treeFuncionario.heading('ID', text='ID')
    treeFuncionario.heading('Nome', text='Nome')
    treeFuncionario.heading ('Email', text='E-mail')
    treeFuncionario.heading ('Setor', text='Setor')
    # Colunas
    treeFuncionario.column('ID',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.column('Nome',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.column('Email',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.column('Setor',minwidth=0,width=140, anchor=tk.CENTER)
    treeFuncionario.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Button - Inserir
    inserirbtn = tk.Button(janelaFuncionario, text='Inserir', command=lambda: classcrud.insertFuncionario(nomeFuncionario, emailFuncionario, setorFuncionario, treeFuncionario))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = tk.Button(janelaFuncionario, text='Atualizar', command=lambda: classcrud.updateFuncionario(IDFuncionario, nomeFuncionario, emailFuncionario, setorFuncionario, treeFuncionario))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = tk.Button(janelaFuncionario, text='Remover', command=lambda: classcrud.deleteFuncionario(IDFuncionario, treeFuncionario))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    voltarbtn = tk.Button(janelaFuncionario, text='Voltar', command=lambda: menu.menu(janelaFuncionario))
    voltarbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeFuncionario(treeFuncionario)

    janelaFuncionario.mainloop()
