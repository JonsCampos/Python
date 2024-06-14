def menu():
    print('*'*36)
    print('*',' '*10,'Candidatos',' '*10,'*')
    print('*',' '*32,'*')
    print('*\t19 - João das Couves\t   *')
    print('*\t33 - Amarildo\t\t   *')
    print('*\t46 - Geremaria Cruz\t   *')
    print('*'*36)
    print('')

def registro():
    for i in range(tot_entrev):
        nome = input(f'Digite o nome do {i+1}° entrevistado: ')
        intencao[i] = int(input(f'Digite o voto do {i+1}° entrevistado: '))
        print('')

def contar():
    for i in range(tot_entrev):
        if (intencao[i] == 19):
            total_votos[0] += 1
        elif (intencao[i] == 33):
            total_votos[1] += 1
        elif (intencao[i] == 46):
            total_votos[2] += 1
        else:
            total_votos[3] +=1

menu()
tot_entrev = int(input('Digite a quantidade de entrevistados: '))
print('')
intencao = [0]*tot_entrev
registro()
total_votos = [0]*4
contar()
print(f'João das Couves \t\t {total_votos[0]} votos')
print(f'Amarildo \t\t\t {total_votos[1]} votos')
print(f'Geremaria Cruz das Couves \t {total_votos[2]} votos')
print(f'Branco/Nulo \t\t\t {total_votos[3]} votos')
