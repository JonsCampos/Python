import tkinter as tk
from tkinter import ttk
import classcrud

def voltar(janelaSetor, janelaMenu):
    janelaMenu.deiconify()
    janelaSetor.destroy()

def setor(nvl, janelaMenu):
    # Janela
    janelaSetor = tk.Toplevel()
    x, y = 800, 500
    posx, posy = int((janelaSetor.winfo_screenwidth()-x)/2), int((janelaSetor.winfo_screenheight()-y)/2)
    janelaSetor.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaSetor.resizable(False, False)
    janelaSetor.iconbitmap('icon.ico')
    janelaSetor.title('Sistema de Controle de acesso')
    janelaMenu.withdraw()
    janelaSetor.protocol("WM_DELETE_WINDOW", lambda: voltar(janelaSetor, janelaMenu))

    # Título
    ttk.Label(janelaSetor, text='Setores', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ttk.Label(janelaSetor, text=nvl[0], font=(12)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do local
    labelIDSetor = ttk.Label(janelaSetor, text='ID do setor')
    labelIDSetor.place(relx=0.2, rely=0.16, anchor=tk.CENTER)
    IDSetor = tk.Entry(janelaSetor)
    IDSetor.place(relx=0.2, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do local
    labelNSetor = ttk.Label(janelaSetor, text='Nome')
    labelNSetor.place(relx=0.4, rely=0.16, anchor=tk.CENTER)
    nomeSetor = tk.Entry(janelaSetor)
    nomeSetor.place(relx=0.4, rely=0.21, anchor=tk.CENTER)

    # Entry - Descrição do local
    labelDscSetor = ttk.Label(janelaSetor, text='Descrição')
    labelDscSetor.place(relx=0.7, rely=0.16, anchor=tk.CENTER)
    descSetor = tk.Entry(janelaSetor)
    descSetor.place(relx=0.7, rely=0.21, width=282, anchor=tk.CENTER)

    # TreeView
    colunas = ('ID', 'Nome', 'Descrição')
    treeSetor = ttk.Treeview(janelaSetor, columns=colunas, selectmode='browse')
    treeSetor['show'] = 'headings'
    # Scrollbar
    scroll = ttk.Scrollbar(janelaSetor, orient='vertical', command=treeSetor.yview)        
    scroll.pack(side ='right', fill ='x')
    treeSetor.configure(yscrollcommand=scroll.set)
    scroll.place(relx=0.861, rely=0.7, anchor=tk.CENTER, height=224)
    # Cabeçalho
    treeSetor.heading('ID', text='ID')
    treeSetor.heading('Nome', text='Nome')
    treeSetor.heading('Descrição', text='Descrição')
    # Colunas
    treeSetor.column('ID',minwidth=0,width=140, anchor=tk.CENTER)
    treeSetor.column('Nome',minwidth=0,width=140, anchor=tk.CENTER)
    treeSetor.column('Descrição',minwidth=0,width=280, anchor=tk.CENTER)
    treeSetor.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    # Selecionar
    def selecionarRegistros(event):
        IDSetor.delete(0, tk.END)
        nomeSetor.delete(0, tk.END)
        descSetor.delete(0, tk.END)

        for selecao in treeSetor.selection():  
            item = treeSetor.item(selecao)  
            idsetor, nomesetor, descsetor = item["values"][0:3]  
            IDSetor.insert(0, idsetor)  
            nomeSetor.insert(0, nomesetor)
            descSetor.insert(0, descsetor)

    treeSetor.bind("<<TreeviewSelect>>", selecionarRegistros)

    # Button - Inserir
    inserirbtn = tk.Button(janelaSetor, text='Inserir', command=lambda: classcrud.insertSetor(nomeSetor, descSetor, treeSetor, janelaSetor))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = tk.Button(janelaSetor, text='Atualizar', command=lambda: classcrud.updateSetor(IDSetor, nomeSetor, descSetor, treeSetor, janelaSetor))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = tk.Button(janelaSetor, text='Remover', command=lambda: classcrud.deleteSetor(IDSetor, treeSetor, janelaSetor))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    inserirbtn = tk.Button(janelaSetor, text='Voltar', command=lambda: voltar(janelaSetor, janelaMenu))
    inserirbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeSetor(treeSetor, janelaSetor)

    janelaSetor.mainloop()
