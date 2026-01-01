from django.shortcuts import render
from is_transport.core.models import Client, Expedition, Tarification
from django.shortcuts import get_object_or_404




def create_expedition(request):
    if request.method == "POST":
        client = get_object_or_404(Client, id=request.POST.get("client"))
        tarification = get_object_or_404(Tarification, id=request.POST.get("tarification"))

        Expedition.objects.create(
            client=client,
            tarification=tarification
        )







