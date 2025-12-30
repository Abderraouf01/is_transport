from django.contrib import admin
from .models import Client,Reclamation,Chauffeur,Expedition,TypeDeService
from .models import Vehicule,Tournee,Incident,suiviExpedition,Facture
from .models import Destination ,Colis,Tarification,Paiement

admin.site.register(Client)
admin.site.register(Reclamation)
admin.site.register(Chauffeur)
admin.site.register(Expedition)
admin.site.register(TypeDeService)
admin.site.register(Vehicule)
admin.site.register(Tournee)
admin.site.register(Incident)
admin.site.register(suiviExpedition)
admin.site.register(Facture)
admin.site.register(Destination)
admin.site.register(Colis)
admin.site.register(Tarification)
admin.site.register(Paiement)

