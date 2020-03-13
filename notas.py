"""""""""""
demo = [1, 2, 3, 2, 1]
# indice = [i for i, x in enumerate(concepto_por_vale) if x == 1]
list = []
for i, x in enumerate(demo):
    print("i: {}, x: {}".format(i,x))
    if x == 1:
        print(i)
        list.append(i)
print(list)
"""""""""""""""
""""      
try:
    #lista demo
    #demo = [1, 2, 3, 2, 1]

    #indice =[i for i, x in enumerate(concepto_por_vale) if x == 1]
    # indice = concepto_por_vale.index(1)
    print("\n el indice de 1: {}\n".format(indice))
except ValueError:
    print('ValueError: no hay vale unico en el frame')
# crear sublista
concepto_por_vale2 = [concepto_por_vale[i] for i in indice]
concepto_por_vale.pop(indice)
print("conceptos en vale ")

# iterar por la sublista y quitar los indices
subserie = valores.loc()
"""""