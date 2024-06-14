import tkinter as tk
from tkinter import ttk, messagebox as mb
import classCrud

# Janela
janela = tk.Tk()
posx, posy = int((janela.winfo_screenwidth()-800)/2), int((janela.winfo_screenheight()-500)/2)
janela.geometry(f'800x500+{posx}+{posy}')
janela.title('Controle de acesso')

# Criação das tabelas (caso não exista)
classCrud.tabelas()

# Título
ttk.Label(janela, text='Sistema de Controle de Acesso', font=(12)).place(x=287, y=7, width=225)

# Entry - ID Funcionário
labelFunc = ttk.Label(text='ID do funcionário')
labelFunc.place(x=125, y=60)
idFunc = tk.Entry(janela)
idFunc.place(x=125, y=80, width=120)

# Combobox - Portaria
labelPortaria = ttk.Label(text='Portaria')
labelPortaria.place(x=340, y=60)
portaria = ttk.Combobox(janela, state='readonly')
registros = classCrud.fillCombobox()
if registros == []:
    portaria['values'] = ['Sem registros']
else:
    portaria['values'] = [registro[0] for registro in registros]
portaria.current(0)
portaria.place(x=340, y=80, width=120)

# Radiobutton - Tipo
labelAcesso = ttk.Label(text='Tipo de acesso')
labelAcesso.place(x=570, y=60)
tipo = tk.StringVar(value='Entrada')
rb1 = tk.Radiobutton(janela, text='Entrada', variable=tipo, value='Entrada')
rb1.place(x=570, y=80)
rb2 = tk.Radiobutton(janela, text='Saída', variable=tipo, value='Saída')
rb2.place(x=570, y=100)

# TreeView
colunas = ('Nome', 'Setor', 'Tipo', 'Portaria', 'Data - Hora')            
treeAcessos = ttk.Treeview(janela,columns=colunas, selectmode='browse')
treeAcessos['show'] = 'headings'
# Scrollbar
scroll = ttk.Scrollbar(janela, orient='vertical', command=treeAcessos.yview)        
scroll.pack(side ='right', fill ='x')
treeAcessos.configure(yscrollcommand=scroll.set)
scroll.place(x=752, y=230, height=225)
# Cabeçalho
treeAcessos.heading('Nome', text='Nome')
treeAcessos.heading('Setor', text='Setor')
treeAcessos.heading('Tipo', text='Tipo')
treeAcessos.heading('Portaria', text='Portaria') 
treeAcessos.heading('Data - Hora', text='Data - Hora')  
# Colunas
treeAcessos.column('Nome',minwidth=0,width=140)
treeAcessos.column('Setor',minwidth=0,width=140)
treeAcessos.column('Tipo',minwidth=0,width=140)
treeAcessos.column('Portaria',minwidth=0,width=140)
treeAcessos.column('Data - Hora',minwidth=0,width=150)
treeAcessos.place(x=40, y=230)

# Button - Inserir
inserirbtn = tk.Button(janela, text='Inserir', command=lambda: classCrud.insert(idFunc, portaria, tipo, treeAcessos))
inserirbtn.place(x=125, y=140)

# Atualização TreeView
classCrud.attTree(treeAcessos)

janela.mainloop()
