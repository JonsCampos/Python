qnt = int(input('Digite a quantidade de números a ser digitado: '))
print('*'*50)
lista = [0]*qnt
prod = 1
for i in range(qnt):
    lista[i] = eval(input(f'Digite o {i+1}° número: '))
    prod *= lista[i]
print('*'*50)
print(f'Os números digitados foram: {lista}')
print(f'O produtório dos números digitados é: {prod}')
