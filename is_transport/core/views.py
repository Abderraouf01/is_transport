from django.shortcuts import render
from is_transport.core.models import Client, Expedition, Tarification
from core.utils import generate_tracking
from django.shortcuts import get_object_or_404



def create_expedition(request):
    if request.method == "POST":

       
        client_id = request.POST.get("client")
        tarification_id = request.POST.get("tarification")

       
        client = get_object_or_404(Client, id=client_id)
        tarification = get_object_or_404(Tarification, id=tarification_id)

        expedition = Expedition.objects.create(
            tracking=generate_tracking(),
            client=client,
            tarification=tarification
        )
        expedition.montant_expedition = expedition.calculer_montant()
        expedition.save(update_fields=['montant_expedition'])



