from django.contrib import admin

from .models import Client,Reclamation,Chauffeur,Expedition,TypeDeService,Vehicule,suiviExpedition,Facture
admin.site.register(Client)
admin.site.register(Reclamation)
admin.site.register(Chauffeur)
admin.site.register(Expedition)
admin.site.register(TypeDeService)
admin.site.register(Vehicule)
admin.site.register(suiviExpedition)
admin.site.register(Facture)