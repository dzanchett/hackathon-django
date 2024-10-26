from datetime import timedelta, datetime

from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view
from hackathonApp.models import Estoque
import re
import math

grafico_data = []

def home(request):
    template = loader.get_template("home.html")
    context = {
    }
    return HttpResponse(template.render(context, request))


def vendas(request):
    template = loader.get_template("vendas.html")
    context = {
    }
    return HttpResponse(template.render(context, request))


def estisticas(request):
    template = loader.get_template("estatisticas.html")
    context = {
        'dados': grafico_data
    }
    return HttpResponse(template.render(context, request))


def compras(request):
    template = loader.get_template("compras.html")
    context = {
    }
    return HttpResponse(template.render(context, request))


@api_view(['POST'])
def upload_encomenda(request):
    global grafico_data

    ficheiro_encomendas = request.FILES['ficheiro_encomenda'].read().decode("utf-8")
    e = Estoque.objects.first()

    # Definições de custo e parâmetros
    custo_encomenda = 10
    custo_posse = 0.70
    prazo_entrega = 7

    procura_anual = 50000

    # Estoques iniciais
    tecido = 2200 # TODO
    algodao = 2200 # TODO
    fio = 2200 # TODO
    poliester = 2200 # TODO

    quantidade_eco_encomenda = math.sqrt((2 * procura_anual * custo_encomenda) / custo_posse)
    procura_diaria = procura_anual / 365
    ponto_encomenda = procura_diaria * prazo_entrega + 1000

    # Dicionários de tipos e razões
    tecido_por_tipo = {
        'Tshirt': 1.00,
        'Calcoes': 0.80,
        'Camisola': 0.50,
        'Calcas': 1.20
    }
    algodao_por_tipo = {
        'Tshirt': 0.80,
        'Calcoes': 0.70,
        'Camisola': 0.35,
        'Calcas': 0.95
    }
    fio_por_tipo = {
        'Tshirt': 0.40,
        'Calcoes': 0.40,
        'Camisola': 0.50,
        'Calcas': 0.35
    }
    poliester_por_tipo = {
        'Tshirt': 1.00,
        'Calcoes': 0.80,
        'Camisola': 0.50,
        'Calcas': 1.20
    }

    razao_tamanho = {
        'XS': 0.50,
        'S': 0.75,
        'M': 1.00,
        'L': 1.50,
        'XL': 2.00
    }

    lines = ficheiro_encomendas.split('\r\n')

    # processa cada encomenda
    items = []
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            num = parts[0]
            type = parts[1]
            tamanho = parts[2]
            items.append((num, type, tamanho))
        elif len(parts) == 1:
            padrao = r'(\d+)(Camisola|Tshirt|Calcoes|Calcas)([LXS]{1,2})'
            conjuntos = re.findall(padrao, line.strip())
            for c in conjuntos:
                num = c[0]
                type = c[1]
                tamanho = c[2]
                items.append((num, type, tamanho))
        else:
            padrao = r'(\d+)\s+(Camisola|Tshirt|Calcoes|Calcas)\s+do\s+tamanho\s+([LXS]{1,2})'
            conjuntos = re.findall(padrao, line)
            for c in conjuntos:
                num = c[0]
                type = c[1]
                tamanho = c[2]
                items.append((num, type, tamanho))

    # Função para obter o próximo dia
    def proximo_dia(data):
        return data + timedelta(days=1)

    # inicializa a data e outros
    dia = 0
    dia_atual = datetime.strptime('2024-10-25', '%Y-%m-%d')
    encomenda = 0
    repor_tecido = (False, 0)
    repor_algodao = (False, 0)
    repor_fio = (False, 0)
    repor_poliester = (False, 0)

    out = []

    for num, type, tamanho in items:
        dia += 1
        tecido_encomenda = float(num) * tecido_por_tipo[type] * razao_tamanho[tamanho]
        algodao_encomenda = float(num) * algodao_por_tipo[type] * razao_tamanho[tamanho]
        fio_encomenda = float(num) * fio_por_tipo[type] * razao_tamanho[tamanho]
        poliester_encomenda = float(num) * poliester_por_tipo[type] * razao_tamanho[tamanho]

        # verifica se algo foi reabastecido
        if (repor_tecido[0] == True and repor_tecido[1] == dia):
            tecido += quantidade_eco_encomenda
            repor_tecido = (False, 0)

        if (repor_algodao[0] == True and repor_algodao[1] == dia):
            algodao += quantidade_eco_encomenda
            repor_algodao = (False, 0)

        if (repor_fio[0] == True and repor_fio[1] == dia):
            fio += quantidade_eco_encomenda
            repor_fio = (False, 0)

        if (repor_poliester[0] == True and repor_poliester[1] == dia):
            poliester += quantidade_eco_encomenda
            repor_poliester = (False, 0)

        # atualiza o stock # TODO
        tecido -= tecido_encomenda
        algodao -= algodao_encomenda
        fio -= fio_encomenda
        poliester -= poliester_encomenda

        out.append({
            'tecido': tecido,
            'algodao': algodao,
            'fio': fio,
            'poliester': poliester,
            'dia_atual': dia_atual
        })

        # Lista de compras no dia
        # compras = []
        # total = 0
        # if (repor_tecido[0] == False and tecido <= ponto_encomenda):
        #     repor_tecido = (True, dia + 7)
        #     compras.append(['Tecido', '7,00', f"{int(round(quantidade_eco_encomenda)):02}",
        #                     f"{round(quantidade_eco_encomenda * 7.00, 2):.2f}"])
        #     total += quantidade_eco_encomenda * 7.00
        #
        # if (repor_algodao[0] == False and algodao <= ponto_encomenda):
        #     repor_algodao = (True, dia + 7)
        #     compras.append(['Algodão', '5,50', f"{int(round(quantidade_eco_encomenda)):02}",
        #                     f"{round(quantidade_eco_encomenda * 5.50, 2):.2f}"])
        #     total += quantidade_eco_encomenda * 5.50
        #
        # if (repor_fio[0] == False and fio <= ponto_encomenda):
        #     repor_fio = (True, dia + 7)
        #     compras.append(['Fio', '4,50', f"{int(round(quantidade_eco_encomenda)):02}",
        #                     f"{round(quantidade_eco_encomenda * 4.50, 2):.2f}"])
        #     total += quantidade_eco_encomenda * 4.50
        #
        # if (repor_poliester[0] == False and poliester <= ponto_encomenda):
        #     repor_poliester = (True, dia + 7)
        #     compras.append(['Poliéster', '10,00', f"{int(round(quantidade_eco_encomenda)):02}",
        #                     f"{round(quantidade_eco_encomenda * 10.00, 2):.2f}"])
        #     total += quantidade_eco_encomenda * 10.00
        # if compras:
        #     encomenda += 1
        #     for compra in compras:
        #         print(f"Artigo: {compra[0]}, Preço: {compra[1]}, Quantidade: {compra[2]}, Subtotal: {compra[3]}")
        #     pdf.create_pdf(str(encomenda), dia_atual.strftime('%d/%m/%Y'), compras, str(round(total, 2)))
        # dia_atual = proximo_dia(dia_atual)

    grafico_data = out

    template = loader.get_template("upload_encomenda.html")
    context = {
        #'ficheiro_encomendas': grafico_data,
    }
    return HttpResponse(template.render(context, request))
