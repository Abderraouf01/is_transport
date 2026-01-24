
from pyexpat.errors import messages
from django.shortcuts import render ,redirect 
from .models import Client, Expedition, Tarification, Colis ,Chauffeur,Vehicule,Destination,TypeDeService,SuiviExpedition,Facture,Reclamation,Paiement,ColisReclamation
from django.shortcuts import get_object_or_404,redirect
from .forms import ClientForm, FactureForm 
from .forms import ChauffeurForm
from .forms import VehiculeForm
from .forms import DestinationForm
from .forms import TypeDeServiceForm
from .forms import TarificationForm
from .forms import IncidentForm
from .models import Incident
from django.shortcuts import render
from .models import Client, Expedition, Tarification, Colis, Facture, Reclamation, TypeDeService, Paiement, ColisReclamation
from django.shortcuts import get_object_or_404,redirect
from decimal import Decimal




def expedition_create(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        tarification_id = request.POST.get("tarification")

        if client_id and tarification_id:
            client = get_object_or_404(Client, id=client_id)
            tarification = get_object_or_404(Tarification, id=tarification_id)

            expedition = Expedition.objects.create(
                client=client,
                tarification=tarification
            )

            return redirect('expedition_detail', tracking=expedition.tracking)

    # fallback: always return a response
    return render(request, 'core/expedition_create.html', {
        'clients': Client.objects.all(),
        'tarifications': Tarification.objects.all(),
    })





def expedition_delete(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)

    if not expedition.can_be_deleted():
        messages.error(request, "Impossible de supprimer cette expédition")
        return redirect('expedition_list')

    expedition.delete()
    messages.success(request, "Expédition supprimée")
    return redirect('expedition_list')




def expedition_change_statut(request, tracking, new_statut):
    expedition = get_object_or_404(Expedition, tracking=tracking)

    try:
        expedition.change_statut(new_statut)

        SuiviExpedition.objects.create(
            suivi_expedition=expedition,
            statut=new_statut,
            lieu_passage="Mise à jour manuelle",
            commentaire=f"Changement de statut vers {new_statut}"
        )

    except ValueError:
        pass

    return redirect('expedition_detail', tracking=tracking)



def expedition_list(request):
    expeditions = Expedition.objects.all()
    clients = Client.objects.all()

    statut = request.GET.get('statut')
    client_id = request.GET.get('client')

    if statut:
        expeditions = expeditions.filter(statut_expedition=statut)

    if client_id:
        expeditions = expeditions.filter(client_id=client_id)

    return render(request, 'core/expedition_list.html', {
        'expeditions': expeditions,
        'clients': clients,
    })




def expedition_detail(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)
    colis = expedition.colis.all()

    return render(request, 'core/expedition_detail.html', {
        'expedition': expedition,
        'colis': colis
    })


def expedition_suivi(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)
    suivis = expedition.suivi.all().order_by('-date_passage')

    return render(request, 'core/expedition_suivi.html', {
        'expedition': expedition,
        'suivis': suivis
    })

def bon_expedition(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)
    return render(request, 'core/bon_expedition.html', {
        'expedition': expedition
    })




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



def home(request):
    return render(request, 'core/home.html')

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'core/client_list.html', {'clients': clients})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Ajouter un Client'})

def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Modifier le Client'})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'core/client_confirm_delete.html', {'object': client, 'type': 'Client'})



def chauffeur_list(request):
    chauffeurs = Chauffeur.objects.all()
    return render(request, 'core/chauffeur_list.html', {'chauffeurs': chauffeurs})

def chauffeur_create(request):
    if request.method == 'POST':
        form = ChauffeurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chauffeur_list')
    else:
        form = ChauffeurForm()
    return render(request, 'core/chauffeur_form.html', {'form': form })

def chauffeur_update(request, pk):
    chauffeur = get_object_or_404(Chauffeur, pk=pk)
    if request.method == 'POST':
        form = ChauffeurForm(request.POST, instance=chauffeur)
        if form.is_valid():
            form.save()
            return redirect('chauffeur_list')
    else:
        form = ChauffeurForm(instance=chauffeur)
    return render(request, 'core/chauffeur_form.html', {'form': form , 'action': 'Modifier'})

def chauffeur_delete(request, pk):
    chauffeur = get_object_or_404(Chauffeur, pk=pk)
    if request.method == 'POST':
        chauffeur.delete()
        return redirect('chauffeur_list')
    return render(request, 'core/chauffeur_confirm_delete.html', {'chauffeur': chauffeur})


def vehicule_list(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'core/vehicule_list.html', {'vehicules': vehicules})

def vehicule_create(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm()
    return render(request, 'core/vehicule_form.html', {'form': form })

def vehicule_update(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'core/vehicule_form.html', {'form': form})

def vehicule_delete(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        vehicule.delete()
        return redirect('vehicule_list')
    return render(request, 'core/vehicule_confirm_delete.html', {'vehicule': vehicule})



def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'core/destination_list.html', {'destinations': destinations})

def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm()
    return render(request, 'core/destination_form.html', {'form': form})

def destination_update(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'core/destination_form.html', {'form': form})

def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('destination_list')
    return render(request, 'core/destination_confirm_delete.html', {'destination': destination})


def service_list(request):
    services =TypeDeService.objects.all()
    return render(request, 'core/service_list.html', {'services': services})

def service_create(request):
    if request.method == 'POST':
        form = TypeDeServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = TypeDeServiceForm()
    return render(request, 'core/service_form.html', {'form': form})

def service_update(request, pk):
    service = get_object_or_404(TypeDeService, pk=pk)
    if request.method == 'POST':
        form = TypeDeServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = TypeDeServiceForm(instance=service)
    return render(request, 'core/service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(TypeDeService, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'core/service_confirm_delete.html', {'service': service})



def tarification_list(request):
    tarifications = Tarification.objects.all()
    return render(request, 'core/tarification_list.html', {'tarifications': tarifications})

def tarification_create(request):
    if request.method == 'POST':
        form = TarificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tarification_list')
    else:
        form = TarificationForm()
    return render(request, 'core/tarification_form.html', {'form': form})


def tarification_update(request, pk):
    tarification = get_object_or_404(Tarification, pk=pk)
    if request.method == 'POST':
        form = TarificationForm(request.POST, instance=tarification)
        if form.is_valid():
            form.save()
            return redirect('tarification_list')
    else:
        form = TarificationForm(instance=tarification)
    return render(request, 'core/tarification_form.html', {'form': form})


def tarification_delete(request, pk):
    tarification = get_object_or_404(Tarification, pk=pk)
    if request.method == 'POST':
        tarification.delete()
        return redirect('tarification_list')
    return render(request, 'core/tarification_confirm_delete.html', {'tarification': tarification})





def incident_list(request):
    incidents = Incident.objects.all()
    return render(request, 'core/incident_list.html', {'incidents': incidents})

def incident_create(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incident_list')
    else:
        form = IncidentForm()
    return render(request, 'core/incident_form.html', {'form': form})

def incident_detail(request, id_incident):
    incident = get_object_or_404(Incident, id_incident=id_incident)
    return render(request, 'core/incident_detail.html', {'incident': incident})

def incident_delete(request, id_incident):
    incident = get_object_or_404(Incident, id_incident=id_incident)
    if request.method == 'POST':
        incident.delete()
        return redirect('incident_list')
    return render(request, 'core/incident_confirm_delete.html', {'incident': incident})


def home(request):
    expeditions = Expedition.objects.all()  # or .order_by('-id')
    return render(request, 'core/home.html', {
        'expeditions': expeditions
    })








def add_colis(request, tracking):
    expedition = get_object_or_404(Expedition, tracking=tracking)

    if not expedition.can_add_colis():
        return redirect('expedition_detail', tracking=tracking)


    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('incident_list')
    else:
        form = IncidentForm()
    return render(request, 'core/incident_form.html', {'form': form})


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/client_form.html', {'form': form, 'title': 'Modifier le Client'})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'core/client_confirm_delete.html', {'object': client, 'type': 'Client'})



def chauffeur_list(request):
    chauffeurs = Chauffeur.objects.all()
    return render(request, 'core/chauffeur_list.html', {'chauffeurs': chauffeurs})

def chauffeur_create(request):
    if request.method == 'POST':
        form = ChauffeurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chauffeur_list')
    else:
        form = ChauffeurForm()
    return render(request, 'core/chauffeur_form.html', {'form': form })

def chauffeur_update(request, pk):
    chauffeur = get_object_or_404(Chauffeur, pk=pk)
    if request.method == 'POST':
        form = ChauffeurForm(request.POST, instance=chauffeur)
        if form.is_valid():
            form.save()
            return redirect('chauffeur_list')
    else:
        form = ChauffeurForm(instance=chauffeur)
    return render(request, 'core/chauffeur_form.html', {'form': form , 'action': 'Modifier'})

def chauffeur_delete(request, pk):
    chauffeur = get_object_or_404(Chauffeur, pk=pk)
    if request.method == 'POST':
        chauffeur.delete()
        return redirect('chauffeur_list')
    return render(request, 'core/chauffeur_confirm_delete.html', {'chauffeur': chauffeur})


def vehicule_list(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'core/vehicule_list.html', {'vehicules': vehicules})

def vehicule_create(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm()
    return render(request, 'core/vehicule_form.html', {'form': form })

def vehicule_update(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        form = VehiculeForm(request.POST, instance=vehicule)
        if form.is_valid():
            form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm(instance=vehicule)
    return render(request, 'core/vehicule_form.html', {'form': form})

def vehicule_delete(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == 'POST':
        vehicule.delete()
        return redirect('vehicule_list')
    return render(request, 'core/vehicule_confirm_delete.html', {'vehicule': vehicule})



def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'core/destination_list.html', {'destinations': destinations})

def destination_create(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm()
    return render(request, 'core/destination_form.html', {'form': form})

def destination_update(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'core/destination_form.html', {'form': form})

def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        return redirect('destination_list')
    return render(request, 'core/destination_confirm_delete.html', {'destination': destination})


def service_list(request):
    services =TypeDeService.objects.all()
    return render(request, 'core/service_list.html', {'services': services})

def service_create(request):
    if request.method == 'POST':
        form = TypeDeServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = TypeDeServiceForm()
    return render(request, 'core/service_form.html', {'form': form})

def service_update(request, pk):
    service = get_object_or_404(TypeDeService, pk=pk)
    if request.method == 'POST':
        form = TypeDeServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = TypeDeServiceForm(instance=service)
    return render(request, 'core/service_form.html', {'form': form})

def service_delete(request, pk):
    service = get_object_or_404(TypeDeService, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'core/service_confirm_delete.html', {'service': service})



def tarification_list(request):
    tarifications = Tarification.objects.all()
    return render(request, 'core/tarification_list.html', {'tarifications': tarifications})

def tarification_create(request):
    if request.method == 'POST':
        form = TarificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tarification_list')
    else:
        form = TarificationForm()
    return render(request, 'core/tarification_form.html', {'form': form, 'action': 'Ajouter'})


def tarification_update(request, pk):
    tarification = get_object_or_404(Tarification, pk=pk)
    if request.method == 'POST':
        form = TarificationForm(request.POST, instance=tarification)
        if form.is_valid():
            form.save()
            return redirect('tarification_list')
    else:
        form = TarificationForm(instance=tarification)
    return render(request, 'core/tarification_form.html', {'form': form})


def tarification_delete(request, pk):
    tarification = get_object_or_404(Tarification, pk=pk)
    if request.method == 'POST':
        tarification.delete()
        return redirect('tarification_list')
    return render(request, 'core/tarification_confirm_delete.html', {'tarification': tarification})



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
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save(commit=False)
            facture.save()

            # Lier les expéditions
            expeditions = form.cleaned_data['expeditions']
            Expedition.objects.filter(
                tracking__in=[e.tracking for e in expeditions]
            ).update(facture=facture)

            # Recalcul des montants
            facture.recalculer()

            return redirect('detail_facture', id_facture=facture.id_facture)
    else:
        form = FactureForm()

    return render(request, 'core/facture_form.html', {
        'form': form,
        'title': 'Créer une facture',
        'facture': None
    })

def update_facture(request, id_facture):
    facture = get_object_or_404(Facture, id_facture=id_facture)

    if request.method == "POST":
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            facture = form.save()

            Expedition.objects.filter(facture=facture).update(facture=None)

            expeditions = form.cleaned_data['expeditions']
            Expedition.objects.filter(
                tracking__in=[e.tracking for e in expeditions]
            ).update(facture=facture)

            return redirect('detail_facture', id_facture=facture.id_facture)
    else:
        form = FactureForm(instance=facture)

    return render(request, 'core/facture_form.html', {
        'form': form,
        'title': 'Modifier la facture',
        'facture': facture
    })


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

def home(request):
    incidents = Incident.objects.all()  
    return render(request, 'core/home.html', {'incidents': incidents})

