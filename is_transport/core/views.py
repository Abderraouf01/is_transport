from django.shortcuts import render
from .models import Client, Expedition, Tarification, Colis
from django.shortcuts import get_object_or_404,redirect



def create_expedition(request):
    if request.method == "POST":
        client = get_object_or_404(Client, id=request.POST.get("client"))
        tarification = get_object_or_404(Tarification, id=request.POST.get("tarification"))

        Expedition.objects.create(
            client=client,
            tarification=tarification
        )



def expedition_change_statut(request, tracking, new_statut):
    expedition = get_object_or_404(Expedition, tracking=tracking)

    try:
        expedition.change_statut(new_statut)
    except ValueError:
    
        pass

    return redirect('expedition_detail', tracking=tracking)

def add_colis(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)

    if not expedition.can_add_colis():
        return redirect('expedition_detail', tracking=tracking)

    if request.method == 'POST':
        Colis.objects.create(
            id_colis=request.POST['id_colis'],
            poids_colis=request.POST['poids'],
            volume_colis=request.POST['volume'],
            description_colis=request.POST['description'],
            expedition=expedition
        )

    return redirect('expedition_detail', tracking=tracking)



def delete_expedition(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)

    if expedition.can_be_deleted():
        expedition.delete()

    return redirect('expedition_list')


