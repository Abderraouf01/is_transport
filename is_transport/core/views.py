from django.shortcuts import render
from .models import Client, Expedition, Tarification, Colis, Facture, Reclamation, TypeDeService, Paiement, ColisReclamation
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
        montant = Decimal(request.POST.get('montant'))
        
        paiement = Paiement.objects.create(
        id_paiement = request.POST.get('id_paiement'),
        mode_paiement=request.POST.get('mode_paiement'),
        date_paiement=request.POST.get('date_paiement'),
        montant_paiement=montant,
        client=client,
        facture=facture)

        return redirect('detail_paiement', id_paiement=paiement.id_paiement)


def create_facture(request):
    if request.method == "POST":
        client = get_object_or_404(Client, id_client=request.POST.get('client'))

        facture = Facture.objects.create(
            id_facture=request.POST.get('id_facture'),
            client=client
        )

        # lier les expéditions à la facture
        tracking_list = request.POST.getlist('expeditions')
        Expedition.objects.filter(tracking__in=tracking_list).update(facture=facture)

        # recalcul des montants
        facture.save()

        return redirect('detail_facture', id_facture=facture.id_facture)



def delete_facture(request, id_facture):
    facture=get_object_or_404(Facture, id_facture=id_facture)
    facture.delete()
    return redirect('journal_factures')

def create_reclamation(request):
    if request.method=='POST':
        client= get_object_or_404(Client, id_client=request.POST.get("client"))

        expedition=None
        if request.POST.get("expedition"):
            expedition=get_object_or_404(Expedition, tracking=request.POST.get("expedition"))
        
        facture=None
        if request.POST.get("facture"):
            facture=get_object_or_404(Facture, id_facture=request.POST.get("facture"))

        type_service= None
        if request.POST.get("service"):
            type_service= get_object_or_404(TypeDeService, code_service=request.POST.get("service"))

        Reclamation.objects.create(
            id_reclamation=request.POST['id_reclamation'],
            nature_reclamation=request.POST['nature'],
            client=client,
            expedition=expedition,
            facture=facture,
            type_service=type_service,
            agent_responsable=request.user
        )
        return redirect('journal_reclamations')

def add_colis_to_reclamation(request, id_reclamation):
    reclamation = get_object_or_404(Reclamation, id_reclamation=id_reclamation)

    if request.method == 'POST':
        listid_colis = request.POST.getlist('colis')

        for id_colis in listid_colis:
            colis = get_object_or_404(Colis, id_colis=id_colis)
            ColisReclamation.objects.create(
                reclamation=reclamation,
                colis=colis
            )

    return redirect('detail_reclamation', id_reclamation=id_reclamation)

def changer_etat_reclamation(request, id_reclamation):
    reclamation = get_object_or_404(Reclamation, id_reclamation=id_reclamation)

    if request.method == 'POST':
        nouvel_etat = request.POST.get('etat')
        reclamation.changer_etat(nouvel_etat, agent=request.user)

    return redirect('detail_reclamation', id_reclamation=id_reclamation)