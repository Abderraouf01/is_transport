from django.urls import path
from . import views

urlpatterns = [
    path(
        'expedition/<str:tracking>/statut/<str:new_statut>/',
        views.expedition_change_statut,
        name='expedition_change_statut'
    ),
]