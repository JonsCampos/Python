import sqlite3 as conector

def verificar_func(id_func, cursor):
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE funcionario_ID = ?', (id_func, ))
    select_func = cursor.fetchone()[0]
    return select_func

def verificar_local(id_local, cursor):
    cursor.execute('SELECT COUNT(*) FROM local WHERE local_ID = ?', (id_local, ))
    select_local = cursor.fetchone()[0]
    return select_local

def ins_ent():
    while True:
        try:
            conexao = conector.connect('./banco_rad.db') 
            cursor = conexao.cursor()
            id_func = int(input('Digite o id do funcionário: ').strip())
            select_func = verificar_func(id_func, cursor)
            if select_func == 0:
                print('Funcionário não encontrado\n')
                continue
            id_local = int(input('Digite o id do local: ').strip())
            select_local = verificar_local(id_local, cursor)
            if select_local == 0:
                print('Local não encontrado\n')
                continue
            comando = '''INSERT INTO entrada (funcionario_ID, local_ID) 
            VALUES (?, ?);'''
            cursor.execute(comando, (id_func, id_local))
            confirm = input('Confirmar entrada? [S/N] ')
            if confirm.lower() == 's':
                conexao.commit()
                print('Entrada confirmada!')
            else:
                conexao.rollback()
                print('Entrada cancelada!')
            break
        except ValueError:
            print('Digite um número válido\n')
        except conector.Error as erro:
            print('Erro ao conectar-se ao banco de dados:', erro)
        finally:
            cursor.close()
            conexao.close()

def list_ent():
    try:
        conexao = conector.connect('./banco_rad.db') 
        cursor = conexao.cursor()
        comando = '''SELECT f.nome, s.nome_setor, l.nome_local,  strftime('%d/%m/%Y %H:%M', e.data_hora_ent)
                        FROM Entrada e
                        JOIN Funcionario f ON e.funcionario_ID = f.funcionario_ID
                        JOIN Setor s ON f.setor_ID = s.setor_ID
                        JOIN Local l ON e.local_ID = l.local_ID
                        ORDER BY e.data_hora_ent DESC;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        print('\nLista de Entradas')
        if len(registros) == 0:
            print('Nenhuma entrada registrada')
        else:
            for registro in registros:
                print(registro)
    except conector.Error as erro:
        print('Erro ao conectar-se ao banco de dados:', erro)
    finally:
        cursor.close()
        conexao.close()

def ins_sai():
    while True:
        try:
            conexao = conector.connect('./banco_rad.db') 
            cursor = conexao.cursor()
            id_func = int(input('Digite o id do funcionário: ').strip())
            select_func = verificar_func(id_func, cursor)
            if select_func == 0:
                print('Funcionário não encontrado\n')
                continue
            id_local = int(input('Digite o id do local: ').strip())
            select_local = verificar_local(id_local, cursor)
            if select_local == 0:
                print('Local não encontrado\n')
                continue
            comando = '''INSERT INTO saida (funcionario_ID, local_ID) 
            VALUES (?, ?);'''
            cursor.execute(comando, (id_func, id_local))
            confirm = input('Confirmar saída? [S/N] ')
            if confirm.lower() == 's':
                conexao.commit()
                print('Saída confirmada!')
            else:
                conexao.rollback()
                print('Saída cancelada!')
            break
        except ValueError:
            print('Digite um número válido\n')
        except conector.Error as erro:
            print('Erro ao conectar-se ao banco de dados:', erro)
        finally:
            cursor.close()
            conexao.close()

def list_sai():
    try:
        conexao = conector.connect('./banco_rad.db') 
        cursor = conexao.cursor()
        comando = '''SELECT f.nome, st.nome_setor, l.nome_local, strftime('%d/%m/%Y %H:%M', sd.data_hora_sai) 
                        FROM Saida sd
                        JOIN Funcionario f ON sd.funcionario_ID = f.funcionario_ID
                        JOIN Setor st ON f.setor_ID = st.setor_ID
                        JOIN Local l ON sd.local_ID = l.local_ID
                        ORDER BY sd.data_hora_sai DESC;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        print('\nLista de Saídas')
        if len(registros) == 0:
            print('Nenhuma saída registrada')
        else:
            for registro in registros:
                print(registro)
    except conector.Error as erro:
        print('Erro ao conectar-se ao banco de dados:', erro)
    finally:
        cursor.close()
        conexao.close()


opc = int(input('1 - Inserir Entrada | 2 - Listar Entradas | 3 - Inserir Saída | 4 - Listar Saídas\n'))
if opc == 1:
    ins_ent()
elif opc == 2:
    list_ent()
elif opc == 3:
    ins_sai()
elif opc == 4:
    list_sai()
