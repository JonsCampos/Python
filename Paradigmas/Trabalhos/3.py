continua = 's'
nome = []
profi = []
renda = []
totp_imposto = 0
while (continua.lower() == 's'):
    x = input('Digite o nome: ')
    nome.append(x)
    x = input('Digite a profissão: ')
    profi.append(x)
    x = float(input('Digite a renda: '))
    renda.append(x)
    if (x >= 2112):
        totp_imposto += 1
    continua = input("Deseja continuar a cadastrar pessoas? 's' para sim e 'n' para não: ")
    print('')
totp = len(nome)
print(f'{totp} pessoas foram cadastradas')
print(f'{totp_imposto} pessoas devem efetuar a declaração do imposto de renda')
