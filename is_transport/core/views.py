from django.shortcuts import render
from .models import Client, Expedition, Tarification, Colis, Facture, Reclamation, TypeDeService, Paiement
from django.shortcuts import get_object_or_404,redirect
from decimal import Decimal



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


def create_paiement(request):
    if request.method == "POST":
        client = get_object_or_404(Client, id_client=request.POST.get('client'))
        facture = get_object_or_404(Facture, id_facture=request.POST.get('facture'))
        
        paiement = Paiement.object.create(
        id_paiement = request.POST.get('id_paiement'),
        mode_paiement=request.POST.get('mode_paiement'),
        date_paiement=request.POST.get('date_paiement'),
        montant_paiement=request.POST.get('montant'),
        client=client,
        facture=facture)

        return redirect('detail_paiement', id_paiement=paiement.id_paiement)


def create_facture(request):
    if request.method == "POST":
        client = get_object_or_404(Client, id_client=request.POST.get('client'))

    facture=Facture.objects.create(
        id_facture=request.POST.get('id_facture'),
        client=client
    )

    # lier les expéditions à la facture
    tracking_list= request.POST.getlist('expeditions')
    Expedition.objects.filter(tracking__in=tracking_list).update(facture=facture)
     
    return redirect('detail_facture', id_facture=facture.id_facture)




def delete_facture(request, id_facture):
    facture=get_object_or_404(Facture, id_facture=id_facture)
    facture.delete()
    return redirect('journal_factures')

def create_reclamation(request):
    if request.method=='POST':
        client= get_object_or_404(Client, id=request.POST.get("client"))

        expedition=None
        if request.POST.get("expedition"):
            expedition=get_object_or_404(Expedition, tracking=request.POST.get("expedition"))
        
        facture=None
        if request.POST.get("facture"):
            facture=get_object_or_404(Facture, id_facture=request.POST.get("facture"))

        type_service= None
        if request.POST.get("service"):
            type_service= get_object_or_404(TypeDeService, id=request.POST.get("service"))

        Reclamation.objects.create(
            id_reclamation=request.POST['id'],
            nature_reclamation=request.POST['nature'],
            description=request.POST.get('description',''),
            client=client,
            expedition=expedition,
            facture=facture,
            type_service=type_service
        )
        return redirect('liste_reclamations')
