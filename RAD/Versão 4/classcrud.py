import sqlite3 as conector
import tkinter as tk
from tkinter import messagebox as mb

#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------
class Acesso:
    def __init__(self, idFunc, idLocal, tipo):
        self.__idFunc = idFunc
        self.__idLocal = idLocal
        self.__tipo = tipo
    
    def get(self):
         return self.__idFunc, self.__idLocal, self.__tipo

class Local:    
    def setIDLocal(self, IDLocal):
        self.__IDLocal = IDLocal

    def setNomeLocal(self, nomeLocal):
        self.__nomeLocal = nomeLocal

    def getIDLocal(self):
        return self.__IDLocal

    def getNomeLocal(self):
        return self.__nomeLocal

#-----------------------------------------------------------------------------
# Abrir Conexão
#-----------------------------------------------------------------------------
def abrirConexao():
    try:
        conexao = conector.connect('./db_controle_acesso.db') 
        cursor = conexao.cursor()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao conectar-se com o banco de dados: {erro}')
    finally:    
        return conexao, cursor

#-----------------------------------------------------------------------------
# Fechar Conexão
#-----------------------------------------------------------------------------
def fecharConexao(conexao, cursor):
    cursor.close()
    conexao.close()
    return conexao, cursor

#-----------------------------------------------------------------------------
# CRUD Acesso
#-----------------------------------------------------------------------------
def fillComboboxLocal():    # Preenchimento dos locais
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT nome_local FROM Local;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao listar os locais: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
    return registros

def attTreeAcesso(treeAcessos):   # Atualização TreeView
    # Apaga registros antigos
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
        # Coloca novos registros
        for registro in registros:
            treeNome = registro[0]
            treeSetor = registro[1]
            treeTipo = registro[2]
            treeLocal = registro[3]
            treeDt_hr = registro[4]
            treeAcessos.insert('', 'end', values=(treeNome, treeSetor, treeTipo, treeLocal, treeDt_hr))           
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao exibir os acessos: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarFunc(idFunc, cursor):  # Verifica se funcionário existe
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE funcionario_ID = ?', (idFunc, ))
    selectFunc = cursor.fetchone()[0]
    return selectFunc

def pegarIDLocal(local, cursor):    # Pega o ID do local selecionado
    cursor.execute('SELECT local_ID FROM Local WHERE nome_local = ?', (local['values'][local.current()], ))
    selectLocal_ID = cursor.fetchone()[0]
    return selectLocal_ID

def insertAcesso(idFunc, local, tipo, treeAcessos):   # Insert tabela Acesso
    try:
        conexao, cursor = abrirConexao()
        # Verificação Funcionário
        selectFunc = verificarFunc(idFunc.get(), cursor)
        if selectFunc == 0:
            mb.showerror('Erro', 'Funcionário não encontrado')
            return
        # ID do local
        if local['values'][0] == 'Sem registros':
            mb.showerror('Erro', 'Local não encontrada')
            return
        else:
            selectLocal_ID = pegarIDLocal(local, cursor)
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
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeAcesso(treeAcessos)

#-----------------------------------------------------------------------------
# CRUD Local
#-----------------------------------------------------------------------------
def attTreeLocal(treeLocal):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeLocal.get_children():
        treeLocal.delete(registro)

    try:
        # Select - Locais
        conexao, cursor = abrirConexao()
        comando = '''SELECT * FROM local;'''
        cursor.execute(comando)
        registros = cursor.fetchall()

        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNome = registro[1]
            treeLocal.insert('', 'end', values=(treeID, treeNome))
            
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao exibir os locais: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarLocal(IDlocal, cursor):    # Verifica se local existe
    cursor.execute('SELECT COUNT(*) FROM local WHERE local_ID = ?', (IDlocal, ))
    selectID = cursor.fetchone()[0]
    return selectID

def verificarNomeLocal(nomeLocal, cursor):   # Verificar nome do local repetido
    cursor.execute('SELECT COUNT(*) FROM local WHERE nome_local= ?', (nomeLocal, ))
    selectNomeLocal = cursor.fetchone()[0]
    return selectNomeLocal

def insertLocal(nomeLocal, treeLocal):   # Insert tabela Local
    try:
        conexao, cursor = abrirConexao()
        # Verificação nome do local vazio
        if nomeLocal.get() == '':
            mb.showerror('Erro', 'Nome do local vazio')
            return
        # Verificação nome do local
        selectNomeLocal = verificarNomeLocal(nomeLocal.get(), cursor)
        if selectNomeLocal != 0:
            mb.showerror('Erro', 'Local já registrado\nTente outro nome')
            return
        # Instância da classe Local
        local = Local()
        local.setNomeLocal(nomeLocal.get())
        # Insert - Local
        comando = '''INSERT INTO local (nome_local) 
                        VALUES (?);'''
        cursor.execute(comando, (local.getNomeLocal(), ))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar inserção?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao inserir os dados: {erro}')
    finally:
        nomeLocal.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeLocal(treeLocal)

def updateLocal(IDLocal, nomeLocal, treeLocal):  # Update tabela Local
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarLocal(IDLocal.get(), cursor)
        if selectID == 0:
            mb.showerror('Erro', 'ID inválido')
            return
        # Verificação nome do local vazio
        if nomeLocal.get() == '':
            mb.showerror('Erro', 'Nome do local vazio')
            return
        # Verificação nome do local
        selectNomeLocal = verificarNomeLocal(nomeLocal.get(), cursor)
        if selectNomeLocal != 0:
            mb.showerror('Erro', 'Local já registrado\nTente outro nome')
            return
        # Instância da classe Local
        local = Local()
        local.setIDLocal(IDLocal.get())
        local.setNomeLocal(nomeLocal.get())
        # Update - Local
        comando = '''UPDATE Local
                        SET nome_local = (?)
                        WHERE local_ID = (?);'''
        cursor.execute(comando, (local.getNomeLocal(), local.getIDLocal()))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Atualização?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao atualizar os dados: {erro}')
    finally:
        nomeLocal.delete(0, tk.END)
        IDLocal.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeLocal(treeLocal)

def deleteLocal(IDLocal, treeLocal): # Delete tabela Local
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarLocal(IDLocal.get(), cursor)
        if selectID == 0:
            mb.showerror('Erro', 'ID inválido')
            return
        # Instância da classe Local
        local = Local()
        local.setIDLocal(IDLocal.get())
        # Delete - Local
        comando = '''DELETE FROM Local WHERE local_ID = (?);'''
        cursor.execute(comando, (local.getIDLocal(), ))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Remoção?'):
            conexao.commit()
        else:
            conexao.rollback()   
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao remover os dados: {erro}')
    finally:
        IDLocal.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeLocal(treeLocal)

#-----------------------------------------------------------------------------
# CRUD Setor
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# CRUD Funcionario
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# Tabelas
#-----------------------------------------------------------------------------
def tabelas():  # Criação das tabelas (caso não exista)
    try:
        conexao, cursor = abrirConexao()
        # Setor
        comando = '''CREATE TABLE IF NOT EXISTS "Setor" (
                        "setor_ID" INTEGER NOT NULL,
                        "nome_setor" VARCHAR(50) NOT NULL,
                        "desc_setor" VARCHAR(255),
                        PRIMARY KEY("setor_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()
        # Funcionário
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
        # Local
        comando = '''CREATE TABLE IF NOT EXISTS "Local" (
                        "local_ID" INTEGER NOT NULL,
                        "nome_local" VARCHAR(50) NOT NULL UNIQUE,
                        PRIMARY KEY("local_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()
        # Acesso
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
            conexao, cursor = fecharConexao(conexao, cursor)