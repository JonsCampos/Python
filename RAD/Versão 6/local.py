import tkinter as tk
from tkinter import ttk
import classcrud

def voltar(janelaLocal, janelaMenu):
    janelaMenu.deiconify()
    janelaLocal.destroy()

def local(nvl, janelaMenu):
    # Janela
    janelaLocal = tk.Toplevel()
    x, y = 800, 500
    posx, posy = int((janelaLocal.winfo_screenwidth()-x)/2), int((janelaLocal.winfo_screenheight()-y)/2)
    janelaLocal.geometry(f'{x}x{y}+{posx}+{posy}')
    janelaLocal.resizable(False, False)
    janelaLocal.iconbitmap('icon.ico')
    janelaLocal.title('Sistema de Controle de acesso')
    janelaMenu.withdraw()
    janelaLocal.protocol("WM_DELETE_WINDOW", lambda: voltar(janelaLocal, janelaMenu))

    # Título
    ttk.Label(janelaLocal, text='Locais', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    # Usuário
    ttk.Label(janelaLocal, text=nvl[0], font=(12)).place(relx=0.92, rely=0.05, anchor=tk.CENTER)

    # Entry - ID do local
    labelIDL = ttk.Label(janelaLocal, text='ID do local')
    labelIDL.place(relx=0.33, rely=0.16, anchor=tk.CENTER)
    IDLocal = tk.Entry(janelaLocal)
    IDLocal.place(relx=0.33, rely=0.21, anchor=tk.CENTER)

    # Entry - Nome do local
    labelNLocal = ttk.Label(janelaLocal, text='Nome')
    labelNLocal.place(relx=0.66, rely=0.16, anchor=tk.CENTER)
    nomeLocal = tk.Entry(janelaLocal)
    nomeLocal.place(relx=0.66, rely=0.21, anchor=tk.CENTER)

    # TreeView
    colunas = ('ID', 'Nome')            
    treeLocal = ttk.Treeview(janelaLocal, columns=colunas, selectmode='browse')
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
    # Selecionar
    def selecionarRegistros(event):
        IDLocal.delete(0, tk.END)
        nomeLocal.delete(0, tk.END)

        for selecao in treeLocal.selection():  
            item = treeLocal.item(selecao)  
            idlocal, nomelocal = item["values"][0:2]  
            IDLocal.insert(0, idlocal)  
            nomeLocal.insert(0, nomelocal)

    treeLocal.bind("<<TreeviewSelect>>", selecionarRegistros)

    # Button - Inserir
    inserirbtn = tk.Button(janelaLocal, text='Inserir', command=lambda: classcrud.insertLocal(nomeLocal, treeLocal, janelaLocal))
    inserirbtn.place(relx=0.25, rely=0.33, anchor=tk.CENTER)

    # Button - Atualizar
    atualizarbtn = tk.Button(janelaLocal, text='Atualizar', command=lambda: classcrud.updateLocal(IDLocal, nomeLocal, treeLocal, janelaLocal))
    atualizarbtn.place(relx=0.50, rely=0.33, anchor=tk.CENTER)

    # Button - Remover
    removerbtn = tk.Button(janelaLocal, text='Remover', command=lambda: classcrud.deleteLocal(IDLocal, treeLocal, janelaLocal))
    removerbtn.place(relx=0.75, rely=0.33, anchor=tk.CENTER)

    # Button - Voltar
    inserirbtn = tk.Button(janelaLocal, text='Voltar', command=lambda: voltar(janelaLocal, janelaMenu))
    inserirbtn.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

    # Atualização TreeView
    classcrud.attTreeLocal(treeLocal, janelaLocal)

    janelaLocal.mainloop()