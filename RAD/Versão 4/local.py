import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud

# Janela
janelaLocal = tk.Tk()
posx, posy = int((janelaLocal.winfo_screenwidth()-800)/2), int((janelaLocal.winfo_screenheight()-500)/2)
janelaLocal.geometry(f'800x500+{posx}+{posy}')
janelaLocal.title('Sistema de Controle de acesso')

# Criação das tabelas (caso não exista)
classcrud.tabelas()

# Título
ttk.Label(janelaLocal, text='Local', font=(12)).place(x=379, y=7, width=41)

# Entry - ID do local
labelIDL = ttk.Label(text='ID do local')
labelIDL.place(x=200, y=60)
IDLocal = tk.Entry(janelaLocal)
IDLocal.place(x=200, y=80, width=120)

# Entry - Nome do local
labelNLocal = ttk.Label(text='Nome do local')
labelNLocal.place(x=480, y=60)
nomeLocal = tk.Entry(janelaLocal)
nomeLocal.place(x=480, y=80, width=120)

# TreeView
colunas = ('ID', 'Nome')            
treeLocal = ttk.Treeview(janelaLocal,columns=colunas, selectmode='browse')
treeLocal['show'] = 'headings'
# Scrollbar
scroll = ttk.Scrollbar(janelaLocal, orient='vertical', command=treeLocal.yview)        
scroll.pack(side ='right', fill ='x')
treeLocal.configure(yscrollcommand=scroll.set)
scroll.place(x=542, y=230, height=225)
# Cabeçalho
treeLocal.heading('ID', text='ID')
treeLocal.heading('Nome', text='Nome')
# Colunas
treeLocal.column('ID',minwidth=0,width=140)
treeLocal.column('Nome',minwidth=0,width=140)
treeLocal.place(x=260, y=230)

# Button - Inserir
inserirbtn = tk.Button(janelaLocal, text='Inserir', command=lambda: classcrud.insertLocal(nomeLocal, treeLocal))
inserirbtn.place(x=200, y=140)

# Button - Atualizar
atualizarbtn = tk.Button(janelaLocal, text='Atualizar', command=lambda: classcrud.updateLocal(IDLocal, nomeLocal, treeLocal))
atualizarbtn.place(x=371.5, y=140)

# Button - Remover
removerbtn = tk.Button(janelaLocal, text='Remover', command=lambda: classcrud.deleteLocal(IDLocal, treeLocal))
removerbtn.place(x=543, y=140)

# Button - Voltar
inserirbtn = tk.Button(janelaLocal, text='Voltar', command=lambda: janelaLocal.destroy())
inserirbtn.place(x=7, y=7)

# Atualização TreeView
classcrud.attTreeLocal(treeLocal)

janelaLocal.mainloop()