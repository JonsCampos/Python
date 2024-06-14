import tkinter as tk
from tkinter import ttk, messagebox as mb
import classcrud

# Janela
janelaMain = tk.Tk()
x, y = 800, 500
posx, posy = int((janelaMain.winfo_screenwidth()-x)/2), int((janelaMain.winfo_screenheight()-y)/2)
janelaMain.geometry(f'{x}x{y}+{posx}+{posy}')
janelaMain.minsize(x, y)
janelaMain.maxsize(x, y)
janelaMain.iconbitmap('icon.ico')
janelaMain.title('Sistema de Controle de acesso')

# Criação das tabelas (caso não exista)
classcrud.tabelas()

# Título
ttk.Label(janelaMain, text='Login', font=(12)).place(relx=0.5, rely=0.05, anchor=tk.CENTER)

# Imagem
icon = tk.PhotoImage(file='loginIcon.png')
label = ttk.Label(image=icon)
label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

# Entry - Usuário
labelLgnUsuario = ttk.Label(text='Usuário')
labelLgnUsuario.place(relx=0.41, rely=0.53, anchor=tk.CENTER)
lgnUsuario = tk.Entry(janelaMain)
lgnUsuario.place(relx=0.52, rely=0.53, anchor=tk.CENTER)

# Entry - Senha
labelLgnSenha = ttk.Label(text='Senha')
labelLgnSenha.place(relx=0.41, rely=0.61, anchor=tk.CENTER)
lgnSenha = tk.Entry(janelaMain, show='*')
lgnSenha.place(relx=0.52, rely=0.61, anchor=tk.CENTER)

# Button - Entrar
entrarbtn = tk.Button(janelaMain, text='Entrar', command=lambda: classcrud.entrar(lgnUsuario, lgnSenha, janelaMain))
entrarbtn.place(relx=0.5, rely=0.73, anchor=tk.CENTER)

janelaMain.mainloop()
