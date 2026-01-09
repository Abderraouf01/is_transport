from django.urls import path
from . import views
from . import journal_pdf_views

urlpatterns = [
    path(
        'expedition/<str:tracking>/statut/<str:new_statut>/',
        views.expedition_change_statut,
        name='expedition_change_statut'
    ),
    path('factures/', journal_pdf_views.journal_factures, name='journal_factures'),
    
    path('factures/<str:id_facture>/', journal_pdf_views.detail_facture, name='detail_facture'),
    
    # path('factures/<str:id_facture>/pdf/', journal_pdf_views.facture_pdf, name='facture_pdf'),
    
    path('paiements/', journal_pdf_views.journal_paiements, name='journal_paiements'),
    
    path('paiements/<str:id_paiement>/', journal_pdf_views.detail_paiement, name='detail_paiement'),
    
    # path('paiements/<str:id_paiement>/pdf/', journal_pdf_views.paiement_pdf, name='paiement_pdf'),
]