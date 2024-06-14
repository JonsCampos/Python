import crud

opc = int(input('1 - Inserir Acesso | 2 - Listar Acessos\n'))
if opc == 1:
    crud.ins_acesso()
elif opc == 2:
    crud.list_acesso()
