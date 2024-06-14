import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud
import menu

def acesso(janelaMenu):
    if (janelaMenu):
        janelaMenu.destroy()

    # Janela
    janelaAcesso = tk.Tk()
    x, y = 800, 500
    posx, posy = int((janelaAcesso.winfo_screenwidth()-x)/2), int((janelaAcesso.winfo_screenheight()-y)/2)
    janelaAcesso.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaAcesso.minsize(x, y)
    janelaAcesso.maxsize(x, y)
    janelaAcesso.iconbitmap('icon.ico')
    janelaAcesso.title('Sistema de Controle de acesso')

    # Criação das tabelas (caso não exista)
    classcrud.tabelas()

    # Título
    ttk.Label(janelaAcesso, text='Controle de Acesso', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Entry - ID Funcionário
    labelFunc = ttk.Label(text='ID do funcionário')
    labelFunc.place(relx=0.25, rely=0.16, anchor=tk.CENTER)
    IDFunc = tk.Entry(janelaAcesso)
    IDFunc.place(relx=0.25, rely=0.21, anchor=tk.CENTER)

    # Combobox - Local
    labelLocal = ttk.Label(text='Local')
    labelLocal.place(relx=0.5, rely=0.16, anchor=tk.CENTER)
    local = ttk.Combobox(janelaAcesso, state='readonly')
    registros = classcrud.fillComboboxLocal()
    if registros == []:
        local['values'] = ['Sem registros']
    else:
        local['values'] = [registro[0] for registro in registros]
    local.current(0)
    local.place(relx=0.5, rely=0.21, anchor=tk.CENTER)

    # Radiobutton - Tipo
    labelAcesso = ttk.Label(text='Tipo de acesso')
    labelAcesso.place(relx=0.75, rely=0.16, anchor=tk.CENTER)
    tipo = tk.StringVar(value='Entrada')
    rb1 = tk.Radiobutton(janelaAcesso, text='Entrada', variable=tipo, value='Entrada')
    rb1.place(relx=0.75, rely=0.21, anchor=tk.CENTER)
    rb2 = tk.Radiobutton(janelaAcesso, text='Saída', variable=tipo, value='Saída')
    rb2.place(relx=0.75, rely=0.26, anchor=tk.CENTER)

    # TreeView
    colunas = ('Nome', 'Setor', 'Tipo', 'Local', 'Data - Hora')            
    treeAcessos = ttk.Treeview(janelaAcesso,columns=colunas, selectmode='browse')
    treeAcessos['show'] = 'headings'
    # Scrollbar
    scroll = ttk.Scrollbar(janelaAcesso, orient='vertical', command=treeAcessos.yview)        
    scroll.pack(side ='right', fill ='x')
    treeAcessos.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.955, rely=0.7, anchor=tk.CENTER, height=224)
    # Cabeçalho
    treeAcessos.heading('Nome', text='Nome')
    treeAcessos.heading('Setor', text='Setor')
    treeAcessos.heading('Tipo', text='Tipo')
    treeAcessos.heading('Local', text='Local') 
    treeAcessos.heading('Data - Hora', text='Data - Hora')  
    # Colunas
    treeAcessos.column('Nome',minwidth=0,width=140, anchor=tk.CENTER)
    treeAcessos.column('Setor',minwidth=0,width=140, anchor=tk.CENTER)
    treeAcessos.column('Tipo',minwidth=0,width=140, anchor=tk.CENTER)
    treeAcessos.column('Local',minwidth=0,width=140, anchor=tk.CENTER)
    treeAcessos.column('Data - Hora',minwidth=0,width=150, anchor=tk.CENTER)
    treeAcessos.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Button - Inserir
    inserirbtn = tk.Button(janelaAcesso, text='Inserir', command=lambda: classcrud.insertAcesso(IDFunc, local, tipo, treeAcessos))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    voltarbtn = tk.Button(janelaAcesso, text='Voltar', command=lambda: menu.menu(janelaAcesso))
    voltarbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeAcesso(treeAcessos)

    janelaAcesso.mainloop()
