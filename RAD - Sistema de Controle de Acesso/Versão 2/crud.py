import sqlite3 as conector
import classes

def verificar_func(id_func, cursor):
    cursor.execute('SELECT COUNT(*) FROM funcionario WHERE funcionario_ID = ?', (id_func, ))
    select_func = cursor.fetchone()[0]
    return select_func

def verificar_local(id_local, cursor):
    cursor.execute('SELECT COUNT(*) FROM local WHERE local_ID = ?', (id_local, ))
    select_local = cursor.fetchone()[0]
    return select_local

def ins_acesso():
    while True:
        try:
            conexao = conector.connect('./Banco/db_controle_acesso.db') 
            cursor = conexao.cursor()
            id_func = int(input('Digite o id do funcionário: ').strip())    # Entry
            select_func = verificar_func(id_func, cursor)
            if select_func == 0:
                print('Funcionário não encontrado\n')
                continue
            id_local = int(input('Digite o id do local: ').strip())     # Combobox
            select_local = verificar_local(id_local, cursor)
            if select_local == 0:
                print('Local não encontrado\n')
                continue
            tipo = input('Digite o tipo de acesso [Entrada/Saída]: ').strip().lower()   # RadioButton
            if tipo != 'entrada' and tipo != 'saída' and tipo != 'saida':
                print('Tipo de acesso incorreto, por favor digite somente "Entrada" ou "Saída"\n')
                continue
            if tipo.lower() == 'saida':
                tipo = 'saída'
            acesso = classes.Acesso(id_func, id_local, tipo)
            comando = '''INSERT INTO acesso (funcionario_ID, local_ID, tipo) 
            VALUES (?, ?, ?);'''
            cursor.execute(comando, (acesso.id_func, acesso.id_local, acesso.tipo))
            confirm = input('Confirmar acesso? [S/N] ')         # MessageBox
            if confirm.lower() == 's':
                conexao.commit()
                print('Acesso confirmado!')
            else:
                conexao.rollback()
                print('Acesso cancelado!')
            break
        except ValueError:
            print('Digite um número válido\n')
        except conector.Error as erro:
            print('Erro ao conectar-se ao banco de dados:', erro)
        finally:
            if (conexao):
                cursor.close()
                conexao.close()

def list_acesso():      # Treeview
    try:
        conexao = conector.connect('./Banco/db_controle_acesso.db') 
        cursor = conexao.cursor()
        comando = '''SELECT f.nome, s.nome_setor, l.nome_local,  strftime('%d/%m/%Y %H:%M', a.data_hora), a.tipo
                    FROM Acesso a
                    JOIN Funcionario f ON a.funcionario_ID = f.funcionario_ID
                    JOIN Setor s ON f.setor_ID = s.setor_ID
                    JOIN Local l ON a.local_ID = l.local_ID
                    ORDER BY a.data_hora DESC;'''
        cursor.execute(comando)
        registros = cursor.fetchall()
        print('\nLista de Acessos')
        if len(registros) == 0:
            print('Nenhum acesso registrado')
        else:
            for registro in registros:
                print(registro)
    except conector.Error as erro:
        print('Erro ao conectar-se ao banco de dados:', erro)
    finally:
        if (conexao):
            cursor.close()
            conexao.close()
