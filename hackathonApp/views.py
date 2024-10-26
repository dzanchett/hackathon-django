from django.http import HttpResponse
from django.template import loader
from rest_framework.decorators import api_view


def index(request):
    template = loader.get_template("index.html")
    context = {
    }
    return HttpResponse(template.render(context, request))


@api_view(['POST'])
def upload_encomenda(request):
    ficheiro_encomendas = request.FILES['ficheiro_encomenda'].read()

    return HttpResponse(ficheiro_encomendas)
