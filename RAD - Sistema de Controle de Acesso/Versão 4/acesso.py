import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud

# Janela
janelaAcesso = tk.Tk()
posx, posy = int((janelaAcesso.winfo_screenwidth()-800)/2), int((janelaAcesso.winfo_screenheight()-500)/2)
janelaAcesso.geometry(f'800x500+{posx}+{posy}')
janelaAcesso.title('Sistema de Controle de acesso')

# Criação das tabelas (caso não exista)
classcrud.tabelas()

# Título
ttk.Label(janelaAcesso, text='Controle de Acesso', font=(12)).place(x=329, y=7, width=141)

# Entry - ID Funcionário
labelFunc = ttk.Label(text='ID do funcionário')
labelFunc.place(x=125, y=60)
idFunc = tk.Entry(janelaAcesso)
idFunc.place(x=125, y=80, width=120)

# Combobox - Local
labelLocal = ttk.Label(text='Local')
labelLocal.place(x=340, y=60)
local = ttk.Combobox(janelaAcesso, state='readonly')
registros = classcrud.fillComboboxLocal()
if registros == []:
    local['values'] = ['Sem registros']
else:
    local['values'] = [registro[0] for registro in registros]
local.current(0)
local.place(x=340, y=80, width=120)

# Radiobutton - Tipo
labelAcesso = ttk.Label(text='Tipo de acesso')
labelAcesso.place(x=570, y=60)
tipo = tk.StringVar(value='Entrada')
rb1 = tk.Radiobutton(janelaAcesso, text='Entrada', variable=tipo, value='Entrada')
rb1.place(x=570, y=80)
rb2 = tk.Radiobutton(janelaAcesso, text='Saída', variable=tipo, value='Saída')
rb2.place(x=570, y=100)

# TreeView
colunas = ('Nome', 'Setor', 'Tipo', 'Local', 'Data - Hora')            
treeAcessos = ttk.Treeview(janelaAcesso,columns=colunas, selectmode='browse')
treeAcessos['show'] = 'headings'
# Scrollbar
scroll = ttk.Scrollbar(janelaAcesso, orient='vertical', command=treeAcessos.yview)        
scroll.pack(side ='right', fill ='x')
treeAcessos.configure(yscrollcommand=scroll.set)
scroll.place(x=752, y=230, height=225)
# Cabeçalho
treeAcessos.heading('Nome', text='Nome')
treeAcessos.heading('Setor', text='Setor')
treeAcessos.heading('Tipo', text='Tipo')
treeAcessos.heading('Local', text='Local') 
treeAcessos.heading('Data - Hora', text='Data - Hora')  
# Colunas
treeAcessos.column('Nome',minwidth=0,width=140)
treeAcessos.column('Setor',minwidth=0,width=140)
treeAcessos.column('Tipo',minwidth=0,width=140)
treeAcessos.column('Local',minwidth=0,width=140)
treeAcessos.column('Data - Hora',minwidth=0,width=150)
treeAcessos.place(x=40, y=230)

# Button - Inserir
inserirbtn = tk.Button(janelaAcesso, text='Inserir', command=lambda: classcrud.insertAcesso(idFunc, local, tipo, treeAcessos))
inserirbtn.place(x=125, y=140)

# Button - Voltar
inserirbtn = tk.Button(janelaAcesso, text='Voltar', command=lambda: janelaAcesso.destroy())
inserirbtn.place(x=7, y=7)

# Atualização TreeView
classcrud.attTreeAcesso(treeAcessos)

janelaAcesso.mainloop()
