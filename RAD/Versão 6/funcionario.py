import tkinter as tk
from tkinter import ttk
import classcrud

def voltar(janelaFuncionario, janelaMenu):
    janelaMenu.deiconify()
    janelaFuncionario.destroy()

def funcionario(nvl, janelaMenu):
    # Janela
    janelaFuncionario = tk.Toplevel()
    x, y = 800, 500
    posx, posy = int((janelaFuncionario.winfo_screenwidth()-x)/2), int((janelaFuncionario.winfo_screenheight()-y)/2)
    janelaFuncionario.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaFuncionario.resizable(False, False)
    janelaFuncionario.iconbitmap('icon.ico')
    janelaFuncionario.title('Sistema de Controle de acesso')
    janelaMenu.withdraw()
    janelaFuncionario.protocol("WM_DELETE_WINDOW", lambda: voltar(janelaFuncionario, janelaMenu))

    # Título
    ttk.Label(janelaFuncionario, text='Funcionários', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ttk.Label(janelaFuncionario, text=nvl[0], font=(12)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do funcionário
    labelIDF = ttk.Label(janelaFuncionario, text='ID do Funcionário')
    labelIDF.place(relx=0.2, rely=0.16, anchor=tk.CENTER)
    IDFuncionario = tk.Entry(janelaFuncionario)
    IDFuncionario.place(relx=0.2, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do funcionário
    labelNFuncionario = ttk.Label(janelaFuncionario, text='Nome do Funcionário')
    labelNFuncionario.place(relx=0.4, rely=0.16, anchor=tk.CENTER)
    nomeFuncionario = tk.Entry(janelaFuncionario)
    nomeFuncionario.place(relx=0.4, rely=0.21, anchor=tk.CENTER)

    # Entry - E-mail do funcionário
    labelEmailFuncionario = ttk.Label(janelaFuncionario, text='E-Mail do Funcionário')
    labelEmailFuncionario.place(relx=0.6, rely=0.16, anchor=tk.CENTER)
    emailFuncionario = tk.Entry(janelaFuncionario)
    emailFuncionario.place(relx=0.6, rely=0.21, anchor=tk.CENTER)

    # Entry - ComboBox do setor do funcionário
    labelSFuncionario = ttk.Label(janelaFuncionario, text='Setor do Funcionário')
    labelSFuncionario.place(relx=0.8, rely=0.16, anchor=tk.CENTER)
    setorFuncionario = ttk.Combobox(janelaFuncionario, state='readonly')
    setorFuncionario.place(relx=0.8, rely=0.21, anchor=tk.CENTER)

    # Preenchimento do ComboBox de Setor
    registros = classcrud.fillComboboxSetor(janelaFuncionario)
    if registros == []:
        setorFuncionario['values'] = ['Sem registros']
    else:
        setorFuncionario['values'] = [registro[0] for registro in registros]
    setorFuncionario.current(0)

    # TreeView
    colunas = ('ID', 'Nome', 'Email', 'Setor')            
    treeFuncionario = ttk.Treeview(janelaFuncionario, columns=colunas, selectmode='browse')
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
    # Selecionar
    def selecionarRegistros(event):
        IDFuncionario.delete(0, tk.END)
        nomeFuncionario.delete(0, tk.END)
        emailFuncionario.delete(0, tk.END)
        setorFuncionario.current(0)

        for selecao in treeFuncionario.selection():  
            item = treeFuncionario.item(selecao)  
            idfunc, nomefunc, emailfunc, setorfunc = item["values"][0:4]  
            IDFuncionario.insert(0, idfunc)  
            nomeFuncionario.insert(0, nomefunc)
            emailFuncionario.insert(0, emailfunc)
            setorFuncionario.set(setorfunc)

    treeFuncionario.bind("<<TreeviewSelect>>", selecionarRegistros)

    # Button - Inserir
    inserirbtn = tk.Button(janelaFuncionario, text='Inserir', command=lambda: classcrud.insertFuncionario(nomeFuncionario, emailFuncionario, setorFuncionario, treeFuncionario, janelaFuncionario))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = tk.Button(janelaFuncionario, text='Atualizar', command=lambda: classcrud.updateFuncionario(IDFuncionario, nomeFuncionario, emailFuncionario, setorFuncionario, treeFuncionario, janelaFuncionario))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = tk.Button(janelaFuncionario, text='Remover', command=lambda: classcrud.deleteFuncionario(IDFuncionario, treeFuncionario, janelaFuncionario))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    inserirbtn = tk.Button(janelaFuncionario, text='Voltar', command=lambda: voltar(janelaFuncionario, janelaMenu))
    inserirbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeFuncionario(treeFuncionario, janelaFuncionario)

    janelaFuncionario.mainloop()
