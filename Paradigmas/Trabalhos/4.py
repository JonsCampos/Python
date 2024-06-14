tot_entrev = int(input('Quantas pessoas serão entrevistadas? '))
print('')
idade = [0]*tot_entrev
t_jovem = 0
t_adulto = 0
t_idoso = 0
for i in range(tot_entrev):
    idade[i] = int(input(f'Digite a idade do {i+1}º entrevistado: '))
    if (idade[i] >= 18) and (idade[i] < 35):
        t_jovem += 1
    elif (idade[i] >= 35) and (idade[i] < 65):
        t_adulto += 1
    elif (idade[i] >= 65):
        t_idoso += 1
print('')
print(f'{t_jovem} Jovens')
print(f'{t_adulto} Adultos')
print(f'{t_idoso} Idosos')

