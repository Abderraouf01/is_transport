from django.contrib import admin

<<<<<<< HEAD
from .models import Client,Reclamation,Chauffeur,Expedition,TypeDeService,Vehicule,Tournee,Incident
=======
from .models import Client,Reclamation,Chauffeur,Expedition,TypeDeService,Vehicule,suiviExpedition,Facture
>>>>>>> 481c133dd9b9583f0ce6f0c359ccf7f258d2b82a
admin.site.register(Client)
admin.site.register(Reclamation)
admin.site.register(Chauffeur)
admin.site.register(Expedition)
admin.site.register(TypeDeService)
admin.site.register(Vehicule)
<<<<<<< HEAD
admin.site.register(Tournee)
admin.site.register(Incident)
=======
admin.site.register(suiviExpedition)
admin.site.register(Facture)
>>>>>>> 481c133dd9b9583f0ce6f0c359ccf7f258d2b82a
