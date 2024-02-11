x = int(input('Digite a quantidade de números: '))
print('*'*50)
base = [0]*x
expo = [0]*x
potencia = [0]*x
for i in range(x):
    base[i] = int(input(f'Digite a {i+1}ª base: '))
print('*'*50)
for i in range(x):
    expo[i] = int(input(f'Digite o {i+1}° expoente: '))
print('*'*50)
for i in range(x):
    potencia[i] = base[i] ** expo[i]
print(f'As potências entre as listas são: {potencia}')
