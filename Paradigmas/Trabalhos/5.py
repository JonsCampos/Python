def media_turma(nota_av, x):
    soma = 0
    for i in range(x):
        soma = soma + nota_av[i]
    media = soma / x
    return media

def cria_dados(x):
    nome_alu = [0]*x
    nota_av = [0]*x
    for i in range(x):
        nome_alu[i] = input(f'Digite o nome do {i+1}º aluno: ')
        nota_av[i] = float(input(f'Digite a nota da AV do {i+1}º aluno: '))
        print('')
    media = media_turma(nota_av, x)
    print(f'Notas: {nota_av}')
    print(f'A média da turma é {media:.2f}')


x = int(input('Digite a quantidade de alunos: '))
print('')
cria_dados(x)
