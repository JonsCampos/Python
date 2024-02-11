x=int(input("Quantos elementos tem os vetores? "))
vet1=[0]*x
vet2=[0]*x
vet3=[0]*x
for i in range(x):
    vet1[i]=int(input(f"Digite o valor do {i+1}º elemento"))
for i in range(x):
    vet2[i]=int(input(f"Digite o valor do {i+1}º elemento"))
for i in range(x):
    vet3[i]=vet1[i]+vet2[i]
print(f"{vet3}")


'''
Linha 1  = imput    ->    input
Linha 2  = [ ]*x    ->    [0]*x
Linha 3  = [ ]*x    ->    [0]*x
Linha 4  = [ ]*x    ->    [0]*x
Linha 5  = (x+1)    ->    (x)
Linha 10 = vet3    ->    vet3[i]
Linha 11 = (f"(vet3)")    ->    (f"{vet3}")
'''
