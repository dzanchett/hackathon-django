from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view


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
    }
    return HttpResponse(template.render(context, request))


def compras(request):
    template = loader.get_template("compras.html")
    context = {
    }
    return HttpResponse(template.render(context, request))


@api_view(['POST'])
def upload_encomenda(request):
    ficheiro_encomendas = request.FILES['ficheiro_encomenda'].read()

    template = loader.get_template("upload_encomenda.html")
    context = {
        'ficheiro_encomendas': ficheiro_encomendas,
    }
    return HttpResponse(template.render(context, request))
