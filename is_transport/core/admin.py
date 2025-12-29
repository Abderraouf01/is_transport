from django.contrib import admin

from .models import Client,Reclamation,Chauffeur,Expedition
admin.site.register(Client)
admin.site.register(Reclamation)
admin.site.register(Chauffeur)
admin.site.register(Expedition)
