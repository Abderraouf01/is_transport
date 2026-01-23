from django.urls import path
from .import views

urlpatterns = [
    path(
        'expedition/<str:tracking>/statut/<str:new_statut>/',
        views.expedition_change_statut,
        name='expedition_change_statut'
    ),

    path('',views.home , name='home'),

    path('clients/', views.client_list ,name='client_list' ),
    path('clients/add/', views.client_create ,name='client_create'),
    path('clients/<int:pk>/edit/', views.client_update, name= 'client_update'),
    path('clients/<int:pk>/delete/', views.client_delete , name= 'client_delete'),

    path('Chauffeurs/', views.chauffeur_list , name='chauffeur_list'),
    path('Chauffeurs/ajouter/', views.chauffeur_create ,name='chauffeur_create'),
    path('Chauffeurs/<int:pk>/update/' , views.chauffeur_update , name = 'chauffeur_update'),
    path('Chauffeurs/<int:pk>/delete' , views.chauffeur_delete , name='chauffeur_delete'),

    path('vehicules/', views.vehicule_list, name='vehicule_list'),
    path('vehicules/add/', views.vehicule_create, name='vehicule_create'),
    path('vehicules/<int:pk>/edit/', views.vehicule_update, name='vehicule_update'),
    path('vehicules/<int:pk>/delete/', views.vehicule_delete, name='vehicule_delete'),

    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/add/', views.destination_create, name='destination_create'),
    path('destinations/<int:pk>/edit/', views.destination_update, name='destination_update'),
    path('destinations/<int:pk>/delete/', views.destination_delete, name='destination_delete'),

    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_update, name='service_update'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),

    path('tarifications/', views.tarification_list, name='tarification_list'),
    path('tarifications/add/', views.tarification_create, name='tarification_create'),
    path('tarifications/<int:pk>/edit/', views.tarification_update, name='tarification_update'),
    path('tarifications/<int:pk>/delete/', views.tarification_delete, name='tarification_delete'),

]