qnt = int(input('Digite a quantidade de alunos: '))
print('*'*45)
idade = [0]*qnt
soma_idade = 0
for i in range(qnt):
    idade[i] = int(input(f'Digite a idade do {i+1}° aluno: '))
    soma_idade += idade[i]
media_idade = soma_idade / qnt
print('*'*45)
print(f'As idades são: {idade}')
print(f'A média de idade da turma é de {media_idade:.1f} anos')
