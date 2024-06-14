import sqlite3 as conector
import tkinter as tk
from tkinter import messagebox as mb
import menu

#--------------------------------------------------------------------------
# Classes
#--------------------------------------------------------------------------
class Acesso:
    def __init__(self, IDFunc, idLocal, tipo):
        self.__IDFunc = IDFunc
        self.__idLocal = idLocal
        self.__tipo = tipo
    
    def get(self):
         return self.__IDFunc, self.__idLocal, self.__tipo
    
class Setor:    
    def setIDSetor(self, IDSetor):
        self.__IDSetor = IDSetor

    def setNomeSetor(self, nomeSetor):
        self.__nomeSetor = nomeSetor

    def setDescSetor(self, descSetor):
        self.__descSetor = descSetor

    def getIDSetor(self):
        return self.__IDSetor

    def getNomeSetor(self):
        return self.__nomeSetor

    def getDescSetor(self):
        return self.__descSetor

class Funcionario:    
    def setIDFuncionario(self, IDFuncionario):
        self.__IDFuncionario = IDFuncionario

    def setNomeFuncionario(self, nomeFuncionario):
        self.__nomeFuncionario = nomeFuncionario

    def setIDSetorFuncionario (self, idSetorFuncionario):
        self.__IDSetorFuncionario = idSetorFuncionario

    def setEmailFuncionario (self, emailFuncionario):
        self.__emailFuncionario = emailFuncionario

    def getIDFuncionario(self):
        return self.__IDFuncionario

    def getNomeFuncionario(self):
        return self.__nomeFuncionario

    def getIDSetorFuncionario(self):
        return self.__IDSetorFuncionario
    
    def getEmailFuncionario(self):
        return self.__emailFuncionario

class Usuario:
    def setIDUsuario(self, IDUsuario):
        self.__IDUsuario = IDUsuario

    def setNomeUsuario(self, nomeUsuario):
        self.__nomeUsuario = nomeUsuario

    def setSenhaUsuario(self, SenhaUsuario):
        self.__SenhaUsuario = SenhaUsuario

    def setIDFuncionario(self, IDFuncionario):
        self.__IDFuncionario = IDFuncionario

    def getIDUsuario(self):
        return self.__IDUsuario

    def getNomeUsuario(self):
        return self.__nomeUsuario     

    def getSenhaUsuario(self):
        return self.__SenhaUsuario

    def getIDFuncionario(self):
        return self.__IDFuncionario    

class Local:    
    def setIDLocal(self, IDLocal):
        self.__IDLocal = IDLocal

    def setNomeLocal(self, nomeLocal):
        self.__nomeLocal = nomeLocal

    def getIDLocal(self):
        return self.__IDLocal

    def getNomeLocal(self):
        return self.__nomeLocal

class Login:
    def __init__(self, lgnUsuario, lgnSenha):
        self.__lgnUsuario = lgnUsuario
        self.__lgnSenha = lgnSenha
    
    def getUsuario(self):
         return self.__lgnUsuario

    def getSenha(self):
         return self.__lgnSenha


#--------------------------------------------------------------------------
# Abrir Conexão
#--------------------------------------------------------------------------
def abrirConexao():
    try:
        conexao = conector.connect('./db_controle_acesso.db') 
        cursor = conexao.cursor()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao conectar-se com o banco de dados: {erro}')
    finally:    
        return conexao, cursor

#--------------------------------------------------------------------------
# Fechar Conexão
#--------------------------------------------------------------------------
def fecharConexao(conexao, cursor):
    cursor.close()
    conexao.close()
    return conexao, cursor

#--------------------------------------------------------------------------
# Verificação Funcionário e Email existe
#--------------------------------------------------------------------------
def verificarFuncionario(IDFuncionario, cursor):  # Verifica se funcionário existe
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE funcionario_ID = ?', (IDFuncionario, ))
    selectFunc = cursor.fetchone()[0]
    return selectFunc

def verificarEmailFuncionario(emailFuncionario, cursor):  # Verifica se email existe
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE email = ?', (emailFuncionario, ))
    selectemailFuncionario = cursor.fetchone()[0]
    return selectemailFuncionario

#--------------------------------------------------------------------------
# CRUD Acesso
#--------------------------------------------------------------------------
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

def pegarIDLocal(local, cursor):    # Pega o ID do local selecionado
    cursor.execute('SELECT local_ID FROM Local WHERE nome_local = ?', (local['values'][local.current()], ))
    selectLocal_ID = cursor.fetchone()[0]
    return selectLocal_ID

def insertAcesso(IDFunc, local, tipo, treeAcessos):   # Insert tabela Acesso
    try:
        conexao, cursor = abrirConexao()
        # Verificação Funcionário
        selectFunc = verificarFuncionario(IDFunc.get(), cursor)
        if selectFunc == 0:
            mb.showerror('Erro', 'Funcionário não encontrado')
            return
        # ID do local
        if local['values'][0] == 'Sem registros':
            mb.showerror('Erro', 'Local não encontrado')
            return
        else:
            selectLocal_ID = pegarIDLocal(local, cursor)
        # Instância da classe Acesso
        acesso = Acesso(IDFunc.get(), selectLocal_ID, tipo.get())
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
        IDFunc.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeAcesso(treeAcessos)

#--------------------------------------------------------------------------
# CRUD Setor
#--------------------------------------------------------------------------
def attTreeSetor(treeSetor):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeSetor.get_children():
        treeSetor.delete(registro)
    try:
        # Select - Locais
        conexao, cursor = abrirConexao()
        comando = '''SELECT * FROM setor;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNome = registro[1]
            treeDesc = registro[2]
            treeSetor.insert('', 'end', values=(treeID, treeNome, treeDesc))           
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao exibir os setores: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarUpdateNomeSetor(IDSetor, cursor):
    cursor.execute('SELECT nome_setor FROM setor WHERE setor_ID = ?', (IDSetor, ))
    selectNomeSetorID = cursor.fetchone()[0]
    return selectNomeSetorID

def verificarSetor(IDSetor, cursor):    # Verifica se setor existe
    cursor.execute('SELECT COUNT(*) FROM setor WHERE setor_ID = ?', (IDSetor, ))
    selectID = cursor.fetchone()[0]
    return selectID

def verificarNomeSetor(nomeSetor, cursor):   # Verificar nome do setor repetido
    cursor.execute('SELECT COUNT(*) FROM setor WHERE nome_setor= ?', (nomeSetor, ))
    selectNomeSetor = cursor.fetchone()[0]
    return selectNomeSetor

def insertSetor(nomeSetor, descSetor, treeSetor):   # Insert tabela Setor
    try:
        conexao, cursor = abrirConexao()
        # Verificação nome do setor vazio
        if nomeSetor.get() == '':
            mb.showerror('Erro', 'Nome inválido')
            return
        # Verificação nome do setor
        selectNomeSetor = verificarNomeSetor(nomeSetor.get(), cursor)
        if selectNomeSetor != 0:
            mb.showerror('Erro', 'Setor já registrado\nTente outro nome')
            return
        # Instância da classe Setor
        setor = Setor()
        setor.setNomeSetor(nomeSetor.get())
        setor.setDescSetor(descSetor.get())
        # Insert - Setor
        comando = '''INSERT INTO setor (nome_setor, desc_setor) 
                        VALUES (?, ?);'''
        cursor.execute(comando, (setor.getNomeSetor(), setor.getDescSetor()))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar inserção?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao inserir os dados: {erro}')
    finally:
        nomeSetor.delete(0, tk.END)
        descSetor.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeSetor(treeSetor)

def updateSetor(IDSetor, nomeSetor, descSetor, treeSetor):  # Update tabela Setor
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarSetor(IDSetor.get(), cursor)
        if selectID == 0:
            mb.showerror('Erro', 'ID inválido')
            return
        # Verificação nome do setor vazio
        if nomeSetor.get() == '':
            mb.showerror('Erro', 'Nome inválido')
            return



        # Verificação nome do setor
        selectNomeSetor = verificarNomeSetor(nomeSetor.get(), cursor)
        if selectNomeSetor != 0:
            selectNomeSetorID = verificarUpdateNomeSetor(IDSetor.get(), cursor)
            if selectNomeSetorID != nomeSetor.get():
                mb.showerror('Erro', 'Setor já registrado\nTente outro nome')
                return




        # Instância da classe Setor
        setor = Setor()
        setor.setIDSetor(IDSetor.get())
        setor.setNomeSetor(nomeSetor.get())
        setor.setDescSetor(descSetor.get())
        # Update - Setor
        comando = '''UPDATE Setor
                        SET nome_setor = (?), desc_setor = (?)
                        WHERE setor_ID = (?);'''
        cursor.execute(comando, (setor.getNomeSetor(), setor.getDescSetor(), setor.getIDSetor()))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Atualização?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao atualizar os dados: {erro}')
    finally:
        nomeSetor.delete(0, tk.END)
        descSetor.delete(0, tk.END)
        IDSetor.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeSetor(treeSetor)

def deleteSetor(IDSetor, treeSetor): # Delete tabela setor
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarSetor(IDSetor.get(), cursor)
        if selectID == 0:
            mb.showerror('Erro', 'ID inválido')
            return
        # Instância da classe Setor
        setor = Setor()
        setor.setIDSetor(IDSetor.get())
        # Delete - Setor
        comando = '''DELETE FROM setor WHERE setor_ID = (?);'''
        cursor.execute(comando, (setor.getIDSetor(), ))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Remoção?'):
            conexao.commit()
        else:
            conexao.rollback()   
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao remover os dados: {erro}')
    finally:
        IDSetor.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeSetor(treeSetor)

#--------------------------------------------------------------------------
# CRUD Funcionario
#--------------------------------------------------------------------------
def fillComboboxSetor():    # Preenchimento dos locais
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT nome_setor FROM Setor;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao listar os setores: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
    return registros

def fillComboboxIDSetor():    # Preenchimento dos IDs de SETOR
    try:
        conexao, cursor = abrirConexao()
        comando = '''SELECT setor_ID FROM Setor;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
    except conector.Error as erro:
        mb.showerror('Erro', f'Erro ao listar os setores: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
    return registros

def attTreeFuncionario(treeFuncionario):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeFuncionario.get_children():
        treeFuncionario.delete(registro)
    try:
        # Select - Funcionarios
        conexao, cursor = abrirConexao()
        comando = '''SELECT funcionario_ID, nome, email, nome_setor
                    FROM Funcionario
                    LEFT JOIN Setor ON Setor.setor_ID = Funcionario.setor_ID'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNome = registro[1]
            treeEmail = registro[2]
            treeSetor = registro[3]
            treeFuncionario.insert('', 'end', values=(treeID, treeNome, treeEmail, treeSetor))            
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao exibir os funcionários: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarNomeFuncionario(nomeFuncionario, cursor):   # Verificar nome do funcionario repetido
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE nome = ?', (nomeFuncionario, ))
    selectNomeFuncionario = cursor.fetchone()[0]
    return selectNomeFuncionario
        
def pegarIDSetor(setor, cursor):    # Pega o ID do setor selecionado
    cursor.execute('SELECT setor_ID FROM Setor WHERE nome_setor = ?', (setor['values'][setor.current()], ))
    selectSetor_ID = cursor.fetchone()[0]
    return selectSetor_ID       

def insertFuncionario(nomeFuncionario, emailFuncionario, setorFuncionario, treeFuncionario):   # Insert tabela Funcionario
    try:
        conexao, cursor = abrirConexao()
        # Verificação de dados do funcionario vazio
        if nomeFuncionario.get() == '' or emailFuncionario.get() == '':
            mb.showerror('Erro', 'Email e/ou Nome vazio(s)!')
            return
        
        if setorFuncionario['values'][0] == 'Sem registros':
            mb.showerror('Erro', 'Local não encontrado')
            return
        else:
            selectSetor_ID = pegarIDSetor(setorFuncionario, cursor)

        # Instância da classe Funcionario
        funcionario = Funcionario()
        funcionario.setNomeFuncionario(nomeFuncionario.get())
        funcionario.setIDSetorFuncionario(setorFuncionario.get())
        funcionario.setEmailFuncionario(emailFuncionario.get())
        # Insert - Funcionario
        comando = '''INSERT INTO funcionario (nome, setor_ID, email) 
                        VALUES (?, ?, ?);'''
        cursor.execute(comando, (funcionario.getNomeFuncionario(), selectSetor_ID, funcionario.getEmailFuncionario()))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar inserção?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao inserir os dados: {erro}')
    finally:
        nomeFuncionario.delete(0, tk.END)
        emailFuncionario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeFuncionario(treeFuncionario)

def updateFuncionario(IDFuncionario, nomeFuncionario, emailFuncionario, setorFuncionario, treeFuncionario):  # Update tabela Funcionario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectFunc = verificarFuncionario(IDFuncionario.get(), cursor)
        if selectFunc == 0:
            mb.showerror('Erro', 'ID inválido')
            return
        # Verificação nome e E-mail do funcionario vazio
        if nomeFuncionario.get() == '' or emailFuncionario.get()==  '':
            mb.showerror('Erro', 'Nome e/ou E-Mail inválido(s)')
            return
        
        if setorFuncionario['values'][0] == 'Sem registros':
            mb.showerror('Erro', 'Local não encontrado')
            return
        else:
            selectSetor_ID = pegarIDSetor(setorFuncionario, cursor)
        
        # Instância da classe funcionario
        funcionario = Funcionario()
        funcionario.setIDFuncionario(IDFuncionario.get())
        funcionario.setEmailFuncionario(emailFuncionario.get())
        funcionario.setNomeFuncionario(nomeFuncionario.get())
        funcionario.setIDSetorFuncionario(setorFuncionario.get())

        # Update - Funcionario
        func = (funcionario.getNomeFuncionario(), funcionario.getEmailFuncionario(), selectSetor_ID, funcionario.getIDFuncionario())
        comando = '''UPDATE Funcionario
                        SET nome = (?),
                        email = (?),
                        setor_ID = (?)
                        WHERE funcionario_ID = (?);'''
        cursor.execute(comando, func)
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Atualização?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao atualizar os dados: {erro}')
    finally:
        nomeFuncionario.delete(0, tk.END)
        IDFuncionario.delete(0, tk.END)
        emailFuncionario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeFuncionario(treeFuncionario)

def deleteFuncionario(IDFuncionario, treeFuncionario): # Delete tabela Funcionario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectFunc = verificarFuncionario(IDFuncionario.get(), cursor)
        if selectFunc == 0:
            mb.showerror('Erro', 'ID inválido')
            return
        # Instância da classe Funcionario
        funcionario = Funcionario()
        funcionario.setIDFuncionario(IDFuncionario.get())
        # Delete - Funcionario
        comando = '''DELETE FROM funcionario WHERE funcionario_ID = (?);'''
        cursor.execute(comando, (funcionario.getIDFuncionario(), ))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Remoção?'):
            conexao.commit()
        else:
            conexao.rollback()   
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao remover os dados: {erro}')
    finally:
        IDFuncionario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeFuncionario(treeFuncionario)

#--------------------------------------------------------------------------
# CRUD Usuario
#--------------------------------------------------------------------------
def attTreeUsuario(treeUsuario):       # Atualização TreeView
    # Apaga registros antigos
    for registro in treeUsuario.get_children():
        treeUsuario.delete(registro)
    try:
        # Select - Locais
        conexao, cursor = abrirConexao()
        comando = '''SELECT u.usuario_ID, u.nome_usuario, f.nome
                        FROM Usuario u
                        JOIN Funcionario f ON u.funcionario_ID = f.funcionario_ID;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        # Coloca novos registros
        for registro in registros:
            treeID = registro[0]
            treeNomeUsuario = registro[1]
            treeFuncionario = registro[2]
            treeUsuario.insert('', 'end', values=(treeID, treeNomeUsuario, treeFuncionario))           
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao exibir os usuários: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

def verificarUpdateNomeUsuario(IDUsuario, cursor):
    cursor.execute('SELECT nome_usuario FROM usuario WHERE usuario_ID = ?', (IDUsuario, ))
    selectNomeUsuID = cursor.fetchone()[0]
    return selectNomeUsuID

def verificarUsuario(IDUsuario, cursor):    # Verifica se usuario existe
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE usuario_ID = ?', (IDUsuario, ))
    selectID = cursor.fetchone()[0]
    return selectID

def verificarNomeUsuario(nomeUsuario, cursor):   # Verificar nome de usuário repetido
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE nome_usuario = ?;', (nomeUsuario, ))
    selectNomeUsuario = cursor.fetchone()[0]
    return selectNomeUsuario

def verificarFuncionarioUsuario(IDFuncionario, cursor): # Verificar se funcionário já tem usuário
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE funcionario_ID = ?;', (IDFuncionario, ))
    selectFuncUsuario = cursor.fetchone()[0]
    return selectFuncUsuario

def insertUsuario(nomeUsuario, senhaUsuario, IDFuncionario, treeUsuario): # Insert tabela Usuario
    try:
        conexao, cursor = abrirConexao()
        # Verificação nome de usuário vazio
        if nomeUsuario.get() == '':
            mb.showerror('Erro', 'Nome de usuário inválido')
            return
        # Verificação nome do usuário
        selectNomeUsuario = verificarNomeUsuario(nomeUsuario.get(), cursor)
        if selectNomeUsuario != 0:
            mb.showerror('Erro', 'Usuário já registrado\nTente outro nome')
            return
        # Verificação senha vazia
        if senhaUsuario.get() == '':
            mb.showerror('Erro', 'Senha inválida')
            return
        # Verificação ID do funcionário vazio
        if IDFuncionario.get() == '':
            mb.showerror('Erro', 'ID do funcionário inválido')
            return
        # Verificação Funcionário
        selectFunc = verificarFuncionario(IDFuncionario.get(), cursor)
        if selectFunc == 0:
            mb.showerror('Erro', 'Funcionário não encontrado')
            return
        else:
            selectFuncUsuario = verificarFuncionarioUsuario(IDFuncionario.get(), cursor)
            if selectFuncUsuario != 0:
                mb.showerror('Erro', 'Funcionário já tem um usuário')
                return
        # Instância da classe Usuário
        usuario = Usuario()
        usuario.setNomeUsuario(nomeUsuario.get())
        usuario.setSenhaUsuario(senhaUsuario.get())
        usuario.setIDFuncionario(IDFuncionario.get())
        # Insert - Usuario
        comando = '''INSERT INTO usuario (nome_usuario, senha, funcionario_ID) 
                        VALUES (?, ?, ?);'''
        cursor.execute(comando, (usuario.getNomeUsuario(), usuario.getSenhaUsuario(), usuario.getIDFuncionario()))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar inserção?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao inserir os dados: {erro}')
    finally:
        nomeUsuario.delete(0, tk.END)
        senhaUsuario.delete(0, tk.END)
        IDFuncionario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeUsuario(treeUsuario)

def updateUsuario(IDUsuario, nomeUsuario, senhaUsuario, treeUsuario):  # Update tabela Usuario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarUsuario(IDUsuario.get(), cursor)
        if selectID == 0:
            mb.showerror('Erro', 'ID do usuário inválido')
            return
        # Verificação nome de usuário vazio
        if nomeUsuario.get() == '':
            mb.showerror('Erro', 'Nome de usuário inválido')
            return



        # Verificação nome do usuário
        selectNomeUsuario = verificarNomeUsuario(nomeUsuario.get(), cursor)
        if selectNomeUsuario != 0:
            selectNomeUsuID = verificarUpdateNomeUsuario(IDUsuario.get(), cursor)
            if selectNomeUsuID != nomeUsuario.get():
                mb.showerror('Erro', 'Usuário já registrado\nTente outro nome')
                return






        # Verificação senha vazia
        if senhaUsuario.get() == '':
            mb.showerror('Erro', 'Senha inválida')
            return
        # Instância da classe Usuário
        usuario = Usuario()
        usuario.setIDUsuario(IDUsuario.get())
        usuario.setNomeUsuario(nomeUsuario.get())
        usuario.setSenhaUsuario(senhaUsuario.get())
        # Update - Usuário
        comando = '''UPDATE Usuario
                        SET nome_usuario = (?), senha = (?)
                        WHERE usuario_ID = (?);'''
        cursor.execute(comando, (usuario.getNomeUsuario(), usuario.getSenhaUsuario(), usuario.getIDUsuario()))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Atualização?'):
            conexao.commit()
        else:
            conexao.rollback()
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao atualizar os dados: {erro}')
    finally:
        IDUsuario.delete(0, tk.END)
        nomeUsuario.delete(0, tk.END)
        senhaUsuario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeUsuario(treeUsuario)

def deleteUsuario(IDUsuario, treeUsuario): # Delete tabela Usuario
    try:
        conexao, cursor = abrirConexao()
        # Verificação ID
        selectID = verificarUsuario(IDUsuario.get(), cursor)
        if selectID == 0:
            mb.showerror('Erro', 'ID do usuário inválido')
            return
        # Instância da classe Usuario
        usuario = Usuario()
        usuario.setIDUsuario(IDUsuario.get())
        # Delete - Usuario
        comando = '''DELETE FROM Usuario WHERE usuario_ID = (?);'''
        cursor.execute(comando, (usuario.getIDUsuario(), ))
        # Messagebox - Confirmação
        if mb.askyesno('Confirmação', 'Confirmar Remoção?'):
            conexao.commit()
        else:
            conexao.rollback()   
    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao remover os dados: {erro}')
    finally:
        IDUsuario.delete(0, tk.END)
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)
        # Atualização TreeView
        attTreeUsuario(treeUsuario)        

#--------------------------------------------------------------------------
# CRUD Local
#--------------------------------------------------------------------------
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
            mb.showerror('Erro', 'Nome inválido')
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
            mb.showerror('Erro', 'Nome inválido')
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

#--------------------------------------------------------------------------
# Main - Login
#--------------------------------------------------------------------------
def verificarLgnUsuario(lgnUsuario, cursor):    # Verifica Login Usuario
    cursor.execute('SELECT COUNT(*) FROM usuario WHERE nome_usuario = ?', (lgnUsuario, ))
    selectLgnUsuario = cursor.fetchone()[0]
    return selectLgnUsuario

def verificarLgnSenha(lgnUsuario, cursor):    # Verifica Login Senha
    cursor.execute('SELECT senha FROM usuario WHERE nome_usuario = ?', (lgnUsuario, ))
    selectLgnSenha = cursor.fetchone()[0]
    return selectLgnSenha

def entrar(lgnUsuario, lgnSenha, janelaMain):
    try:
        conexao, cursor = abrirConexao()
        # Instância da classe Login
        login = Login(lgnUsuario.get(), lgnSenha.get())
        # Verificação Login
        selectLgnUsuario = verificarLgnUsuario(login.getUsuario(), cursor)
        if selectLgnUsuario == 0:
            mb.showerror('Erro', 'Usuário e/ou senha inválidos')
            return
        else:
            selectLgnSenha = verificarLgnSenha(login.getUsuario(), cursor)
            if selectLgnSenha != login.getSenha():
                mb.showerror('Erro', 'Usuário e/ou senha inválidos')
                return

        menu.menu(janelaMain)

    except conector.Error as erro:
            mb.showerror('Erro', f'Erro ao se conectar com o banco de dados: {erro}')
    finally:
        if (conexao):
            conexao, cursor = fecharConexao(conexao, cursor)

#--------------------------------------------------------------------------
# Tabelas
#--------------------------------------------------------------------------
def tabelas():  # Criação das tabelas (caso não exista)
    try:
        conexao, cursor = abrirConexao()
        # Setor
        comando = '''CREATE TABLE IF NOT EXISTS "Setor" (
                        "setor_ID" INTEGER NOT NULL,
                        "nome_setor" VARCHAR(50) NOT NULL UNIQUE,
                        "desc_setor" VARCHAR(255),
                        PRIMARY KEY("setor_ID" AUTOINCREMENT)
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Funcionário
        comando = '''CREATE TABLE IF NOT EXISTS "Funcionario" (
	                    "funcionario_ID" INTEGER NOT NULL,
	                    "nome"	VARCHAR(50) NOT NULL,
	                    "email"	VARCHAR(100),
	                    "setor_ID" INTEGER NOT NULL,
	                    PRIMARY KEY("funcionario_ID" AUTOINCREMENT),
	                    FOREIGN KEY("setor_ID") REFERENCES "Setor"("setor_ID")
                    );'''
        cursor.execute(comando, )
        conexao.commit()

        # Usuario
        comando = '''CREATE TABLE IF NOT EXISTS "Usuario" (
	                    "usuario_ID" INTEGER NOT NULL,
	                    "nome_usuario" VARCHAR(50) NOT NULL UNIQUE,
	                    "senha" VARCHAR(50) NOT NULL,
	                    "funcionario_ID" INTEGER NOT NULL,
	                    PRIMARY KEY("usuario_ID" AUTOINCREMENT)
	                    FOREIGN KEY("funcionario_ID") REFERENCES "Funcionario"("funcionario_ID") ON DELETE CASCADE
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
