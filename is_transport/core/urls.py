from django.urls import path
from .import views
from . import views
from . import journal_pdf_views

urlpatterns = [
    path('expeditions/create/', views.expedition_create, name='expedition_create'),
    path('expeditions/', views.expedition_list, name='expedition_list'),
     path(
        'expeditions/<str:tracking>/add-colis/',
        views.add_colis,
        name='add_colis'
    ),
    path('expeditions/<str:tracking>/', views.expedition_detail, name='expedition_detail'),
    path('expedition/<str:tracking>/bon/', views.bon_expedition, name='bon_expedition'),
    path('expedition/<str:tracking>/suivi/', views.expedition_suivi, name='expedition_suivi'),
    
    path(
    'expedition/<str:tracking>/statut/<str:code>/',
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
    
    path('factures/', journal_pdf_views.journal_factures, name='journal_factures'),
    path('factures/create/', views.create_facture, name='create_facture'),
    path('factures/<str:id_facture>/update/', views.update_facture, name='update_facture'),
    path('factures/<str:id_facture>/delete/', views.delete_facture, name='delete_facture'),
    path('factures/<str:id_facture>/', journal_pdf_views.detail_facture, name='detail_facture'),
    path('factures/<str:id_facture>/pdf/', journal_pdf_views.facture_pdf, name='facture_pdf'),
    
    path('paiements/create/', views.create_paiement, name='create_paiement'),
    path('paiements/<str:id_paiement>/delete/', views.delete_paiement, name='delete_paiement'),
    path('paiements/<str:id_paiement>/update/', views.update_paiement, name='update_paiement'),
    path('paiements/', journal_pdf_views.journal_paiements, name='journal_paiements'),
    path('paiements/<str:id_paiement>/', journal_pdf_views.detail_paiement, name='detail_paiement'),
    path('paiements/<str:id_paiement>/pdf/', journal_pdf_views.paiement_pdf, name='paiement_pdf'),

    path('reclamations/', journal_pdf_views.journal_reclamations, name='journal_reclamations'),
    path('reclamations/create/', views.create_reclamation, name='create_reclamation'),
    path('reclamations/<str:id_reclamation>/update/', views.update_reclamation, name='update_reclamation'),
    path('reclamations/<str:id_reclamation>/delete/', views.delete_reclamation, name='delete_reclamation'),
    path('reclamations/<str:id_reclamation>/', journal_pdf_views.detail_reclamation, name='detail_reclamation'),
    path('reclamations/<str:id_reclamation>/etat/',views.changer_etat_reclamation, name='changer_etat_reclamation'),
    path('reclamations/<str:id_reclamation>/add-colis/',views.add_colis_to_reclamation,name='add_colis_to_reclamation'),
    
    path('', views.home, name='home'),
    path('incidents/', views.incident_list, name='incident_list'),
    path('incidents/create/', views.incident_create, name='incident_create'),
    path('incidents/<str:id_incident>/', views.incident_detail, name='incident_detail'),
    path('incidents/<str:id_incident>/delete/', views.incident_delete, name='incident_delete'),

   
]