x = int(input('Digite a quantidade de números: '))
print('*'*55)
lista = [0]*x
par = 0
impar = 0
for i in range(x):
    lista[i] = int(input(f'Digite o {i+1}° número : '))
    if (lista[i] % 2 == 0):
        par += 1
    else:
        impar += 1
print('*'*55)
print(f'Os valores digitados foram: {lista}')
print(f'A quantidade de números pares é {par} e de ímpares é {impar}')
