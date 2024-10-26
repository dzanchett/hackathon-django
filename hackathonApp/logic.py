import re
import pdf
import math

custo_encomenda = 10
custo_posse = 0.70
prazo_entrega = 7

procura_anual = 50000

tecido_s = 1000
algodao_s = 1000
fio_s = 1000
poliester_s = 1000

tecido = 2200
algodao = 2200
fio = 2200
poliester = 2200

quantidade_eco_encomenda = math.sqrt((2*procura_anual*custo_encomenda)/custo_posse)
procura_diaria = procura_anual/365

ponto_encomenda = procura_diaria*prazo_entrega + 1000

tecido_por_tipo = {
    'Tshirt' : 1.00,
    'Calcoes' : 0.80,
    'Camisola' : 0.50,
    'Calcas' : 1.20
}
algodao_por_tipo = {
    'Tshirt' : 0.80,
    'Calcoes' : 0.70,
    'Camisola' : 0.35,
    'Calcas' : 0.95
}
fio_por_tipo = {
    'Tshirt' : 0.40,
    'Calcoes' : 0.40,
    'Camisola' : 0.50,
    'Calcas' : 0.35
}
poliester_por_tipo = {
    'Tshirt' : 1.30,
    'Calcoes' : 1.40,
    'Camisola' : 1.15,
    'Calcas' : 1.50
}

razao_tamanho = {
    'XS' : 0.50,
    'S' : 0.75,
    'M' : 1.00,
    'L' : 1.50,
    'XL' : 2.00
}


with open('encomenda1.txt', 'r') as file:
    lines = file.readlines()

dia = 0
items = []
for line in lines:
    parts = line.split()
    if len(parts) == 3:
        num = parts[0]
        item = parts[1]
        tamanho = parts[2]
        items.append((num, item, tamanho))
    elif len(parts) == 1:
        padrao = r'(\d+)(Camisola|Tshirt|Calcoes|Calcas)([LXS]{1,2})'
        conjuntos = re.findall(padrao, line.strip())
        for c in conjuntos:
            num = c[0]
            item = c[1]
            tamanho = c[2]
            items.append((num, item, tamanho))
    else:
        padrao= r'(\d+)\s+(Camisola|Tshirt|Calcoes|Calcas)\s+do\s+tamanho\s+([LXS]{1,2})'
        conjuntos = re.findall(padrao, line)
        for c in conjuntos:
            num = c[0]
            item = c[1]
            tamanho = c[2]
            items.append((num, item, tamanho))



dias = 0
encomenda = 0
repor_tecido = (False,0)
repor_algodao = (False,0)
repor_fio = (False,0)
repor_poliester = (False,0)


for num, item, tamanho in items:
    dia+=1
    tecido_encomenda = float(num)* tecido_por_tipo[item] * razao_tamanho[tamanho]
    algodao_encomenda = float(num) * algodao_por_tipo[item] * razao_tamanho[tamanho]
    fio_encomenda = float(num) * fio_por_tipo[item] * razao_tamanho[tamanho]
    poliester_encomenda = float(num) * poliester_por_tipo[item] * razao_tamanho[tamanho]

    #check for replenishment
    if(repor_tecido[0] == True and repor_tecido[1] == dia) :
        tecido+=quantidade_eco_encomenda
        repor_tecido = (False,0)

    if(repor_algodao[0] == True and repor_algodao[1] == dia) :
        algodao+=quantidade_eco_encomenda
        repor_algodao = (False,0)

    if(repor_fio[0] == True and repor_fio[1] == dia) :
        fio+=quantidade_eco_encomenda
        repor_fio = (False,0)

    if(repor_poliester[0] == True and repor_poliester[1] == dia) :
        poliester+=quantidade_eco_encomenda
        repor_poliester = (False,0)

    #atualizar o stock
    tecido -= tecido_encomenda
    algodao -= algodao_encomenda
    fio -= fio_encomenda
    poliester -= poliester_encomenda

    #Lista de compras no dia
    compras = []
    total = 0
    if (repor_tecido[0] == False and tecido <= ponto_encomenda):
        repor_tecido = (True, dia + 7)
        compras.append(['Tecido', '7,00', f"{int(round(quantidade_eco_encomenda)):02}", f"{round(quantidade_eco_encomenda * 7.00, 2):.2f}"])
        total += quantidade_eco_encomenda * 7.00

    if (repor_algodao[0] == False and algodao <= ponto_encomenda):
        repor_algodao = (True, dia + 7)
        compras.append(['Algodão', '5,50', f"{int(round(quantidade_eco_encomenda)):02}", f"{round(quantidade_eco_encomenda * 5.50, 2):.2f}"])
        total += quantidade_eco_encomenda * 5.50

    if (repor_fio[0] == False and fio <= ponto_encomenda):
        repor_fio = (True, dia + 7)
        compras.append(['Fio', '4,50', f"{int(round(quantidade_eco_encomenda)):02}", f"{round(quantidade_eco_encomenda * 4.50, 2):.2f}"])
        total += quantidade_eco_encomenda * 4.50

    if (repor_poliester[0] == False and poliester <= ponto_encomenda):
        repor_poliester = (True, dia + 7)
        compras.append(['Poliéster', '10,00', f"{int(round(quantidade_eco_encomenda)):02}", f"{round(quantidade_eco_encomenda * 10.00, 2):.2f}"])
        total += quantidade_eco_encomenda * 10.00
    if compras:
        encomenda += 1
        for compra in compras:
            print(f"Artigo: {compra[0]}, Preço: {compra[1]}, Quantidade: {compra[2]}, Subtotal: {compra[3]}")
        print(f"Encomenda : {encomenda}, Total: {round(quantidade_eco_encomenda * 10.00, 2):.2f}")