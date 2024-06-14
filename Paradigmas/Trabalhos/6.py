def aliquota():
    print('-'*50)
    print('BASE DE CÁLCULO\t\t\t\tALÍQUOTA')
    print('-'*50)
    print('De R$ 0,00 até R$ 2.2122,00\t\tIsento')
    print('-'*50)
    print('De R$ 2.2122,01 até R$ 2.826,65\t\t7,50%')
    print('-'*50)
    print('De R$ 2.826,66 até R$ 3.751,05\t\t15,00%')
    print('-'*50)
    print('De R$ 3.751,06 até R$ 4.664,68\t\t22,50%')
    print('-'*50)
    print('A partir de R$ 4.664,68\t\t\t27,50%')
    print('-'*50)
    print('')

def desconto(x, renda):
    desc = [0]*x
    for i in range(x):
        if (renda[i] <= 2112.00):
            desc[i] = 0
        elif (renda[i] <= 2826.65):
            desc[i] = renda[i] * 0.075
        elif (renda[i] <= 3751.05):
            desc[i] = renda[i] * 0.15
        elif (renda[i] <= 4664.68):
            desc[i] = renda[i] * 0.225
        else:
            desc[i] = renda[i] * 0.275
    print(f'Lista de descontos: {desc}')   


aliquota()
x = int(input('Digite a quantidade de pessoas: '))
print('')
cpf = [0]*x
nome = [0]*x
renda = [0]*x
for i in range(x):
    print(f'{i+1}ª PESSOA')
    cpf[i] = input(f'Digite o CPF: ')
    nome[i] = input(f'Digite o nome: ')
    renda[i] = float(input(f'Digite a renda: '))
    print('')
desconto(x, renda)
