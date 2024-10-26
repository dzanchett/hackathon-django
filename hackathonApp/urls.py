from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("vendas", views.vendas, name="vendas"),
    path("estatisticas", views.estisticas, name="estatisticas"),
    path("compras", views.compras, name="compras"),
    path("upload-encomenda", views.upload_encomenda, name="upload_encomenda"),
]