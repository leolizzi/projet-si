from random import*
fichier = open('code_generes.txt','w')
for j in range(10):
    string = ''
    for i in range(16):
        string += str(randint(0,9))
    fichier.write(string+'\n')
    print(string)
fichier.close()
