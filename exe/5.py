nome = [0]*5
nota = [0]*5
acima = 0
abaixo = 0
for i in range(5):
    nome[i] = input(f'Digite o nome do {i+1}° aluno: ')
    nota[i] = eval(input(f'Digite a nota da AV do {i+1}° aluno: '))
    print('*'*40)
    if nota[i] >= 6:
        acima += 1
    else:
        abaixo += 1
print(f'{acima} alunos estão acima da média\n{abaixo} alunos estão abaixo da média')
