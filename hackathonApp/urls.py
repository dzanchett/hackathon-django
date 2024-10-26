from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-encomenda", views.upload_encomenda, name="upload_encomenda"),
]