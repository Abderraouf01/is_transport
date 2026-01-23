from django.urls import path
from . import views
from . import journal_pdf_views

urlpatterns = [
    path(
        'expedition/<str:tracking>/statut/<str:new_statut>/',
        views.expedition_change_statut,
        name='expedition_change_statut'
    ),
    path('factures/create/', views.create_facture, name='create_facture'),

    path('factures/<str:id_facture>/delete/', views.delete_facture, name='delete_facture'),

    path('factures/', journal_pdf_views.journal_factures, name='journal_factures'),
    
    path('factures/<str:id_facture>/', journal_pdf_views.detail_facture, name='detail_facture'),
    
    path('factures/<str:id_facture>/pdf/', journal_pdf_views.facture_pdf, name='facture_pdf'),
    
    path('paiements/create/', views.create_paiement, name='create_paiement'),

    path('paiements/', journal_pdf_views.journal_paiements, name='journal_paiements'),
    
    path('paiements/<str:id_paiement>/', journal_pdf_views.detail_paiement, name='detail_paiement'),
    
    path('paiements/<str:id_paiement>/pdf/', journal_pdf_views.paiement_pdf, name='paiement_pdf'),

    path('reclamations/', journal_pdf_views.journal_reclamations, name='journal_reclamations'),

    path('reclamations/create/', views.create_reclamation, name='create_reclamation'),

    path('reclamations/<str:id_reclamation>/', journal_pdf_views.detail_reclamation, name='detail_reclamation'),

    path('reclamations/<str:id_reclamation>/etat/',views.changer_etat_reclamation, name='changer_etat_reclamation'),

    path('reclamations/<str:id_reclamation>/colis/',views.add_colis_to_reclamation,name='add_colis_to_reclamation'),

    path('reclamations/rapport/', journal_pdf_views.rapport_reclamations, name='reclamations_rapport'),

]