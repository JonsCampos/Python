import sqlite3 as conector
from tkinter import messagebox as mb

# Criação da classe Acesso
class Acesso:
    def __init__(self, idFunc, idLocal, tipo):
        self.__idFunc = idFunc
        self.__idLocal = idLocal
        self.__tipo = tipo
    
    def get(self):
         return self.__idFunc, self.__idLocal, self.__tipo

# Abertura de conexão com o banco de dados
def abrirConexao():
    try:
        conexao = conector.connect('./db_controle_acesso.db') 
        cursor = conexao.cursor()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao conectar-se com o banco de dados: {erro}')
    finally:    
        return conexao, cursor

# Preenchimento das portarias
def fillCombobox():
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT nome_local FROM Local;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao listar as portarias: {erro}')
    finally:
        if (conexao):
            cursor.close()
            conexao.close()
    return registros

# Atualização TreeView
def attTree(treeAcessos):
    # Apagar registros antigos
    for registro in treeAcessos.get_children():
        treeAcessos.delete(registro)

    try:
        # Select - Acessos
        conexao, cursor = abrirConexao()
        comando = '''SELECT f.nome, s.nome_setor, a.tipo, l.nome_local,  strftime("%d/%m/%Y - %H:%M", a.data_hora)
                    FROM Acesso a
                    JOIN Funcionario f ON a.funcionario_ID = f.funcionario_ID
                    JOIN Setor s ON f.setor_ID = s.setor_ID
                    JOIN Local l ON a.local_ID = l.local_ID
                    ORDER BY a.data_hora DESC;'''
        cursor.execute(comando)
        registros = cursor.fetchall()

        # Colocar novos registros
        for registro in registros:
            treeNome = registro[0]
            treeSetor = registro[1]
            treeTipo = registro[2]
            treePortaria = registro[3]
            treeDt_hr = registro[4]
            treeAcessos.insert('', 'end', values=(treeNome, treeSetor, treeTipo, treePortaria, treeDt_hr))
            
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao exibir os acessos: {erro}')
    finally:
        if (conexao):
            cursor.close()
            conexao.close()

# Verificação de funcionários
def verificarFunc(idFunc, cursor):
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE funcionario_ID = ?', (idFunc, ))
    selectFunc = cursor.fetchone()[0]
    return selectFunc

# Pega o ID da portaria
def pegarIDLocal(portaria, cursor):
    cursor.execute('SELECT local_ID FROM Local WHERE nome_local = ?', (portaria['values'][portaria.current()], ))
    selectLocal_ID = cursor.fetchone()[0]
    return selectLocal_ID

# Inserção de dados 
def insert(idFunc, portaria, tipo, treeAcessos):
    try:
        conexao, cursor = abrirConexao()

        # Verificação Funcionário
        selectFunc = verificarFunc(idFunc.get(), cursor)
        if selectFunc == 0:
            mb.showerror('Erro', 'Funcionário não encontrado')
            return

        # ID da portaria
        if portaria['values'][0] == 'Sem registros':
            mb.showerror('Erro', 'Portaria não encontrada')
            return
        else:
            selectLocal_ID = pegarIDLocal(portaria, cursor)

        # Instância da classe Acesso
        acesso = Acesso(idFunc.get(), selectLocal_ID, tipo.get())

        # Insert - Acesso
        comando = '''INSERT INTO acesso (funcionario_ID, local_ID, tipo) 
        VALUES (?, ?, ?);'''
        cursor.execute(comando, (acesso.get()))

        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar acesso?'):
            conexao.commit()
        else:
            conexao.rollback()
            
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao inserir os dados: {erro}')
    finally:
        if (conexao):
            cursor.close()
            conexao.close()

        # Atualização TreeView
        attTree(treeAcessos)

# Criação das tabelas (caso não exista)
def tabelas():
    try:
        conexao, cursor = abrirConexao()
        comando = '''CREATE TABLE IF NOT EXISTS "Setor" (
                        "setor_ID" INTEGER NOT NULL,
                        "nome_setor" VARCHAR(50) NOT NULL,
                        "desc_setor" VARCHAR(255),
                        PRIMARY KEY("setor_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()
        comando = '''CREATE TABLE IF NOT EXISTS "Funcionario" (
                        "funcionario_ID" INTEGER NOT NULL,
                        "nome"	VARCHAR(50) NOT NULL,
                        "dt_nasc" DATE NOT NULL,
                        "CPF" VARCHAR(14) NOT NULL,
                        "telefone" VARCHAR(20),
                        "email"	VARCHAR(100),
                        "setor_ID" INTEGER NOT NULL,
                        PRIMARY KEY("funcionario_ID" AUTOINCREMENT),
                        FOREIGN KEY("setor_ID") REFERENCES "Setor"("setor_ID")
                    );'''
        cursor.execute(comando, )
        conexao.commit()
        comando = '''CREATE TABLE IF NOT EXISTS "Local" (
                        "local_ID" INTEGER NOT NULL,
                        "nome_local" VARCHAR(50) NOT NULL UNIQUE,
                        PRIMARY KEY("local_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()
        comando = '''CREATE TABLE IF NOT EXISTS "Acesso" (
                        "data_hora" DATETIME DEFAULT (datetime('now', 'localtime')),
                        "tipo"	VARCHAR(7) NOT NULL,
                        "funcionario_ID" INTEGER NOT NULL,
                        "local_ID" INTEGER NOT NULL,
                        FOREIGN KEY("local_ID") REFERENCES "Local"("local_ID"),
                        FOREIGN KEY("funcionario_ID") REFERENCES "Funcionario"("funcionario_ID"),
                        PRIMARY KEY("data_hora","funcionario_ID","local_ID")
                    );'''
        cursor.execute(comando, )
        conexao.commit()

    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao criar as tabelas: {erro}')
    finally:
        if (conexao):
            cursor.close()
            conexao.close()
