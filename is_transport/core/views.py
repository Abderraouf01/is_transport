from django.shortcuts import render ,redirect 
from .models import Client, Expedition, Tarification, Colis ,Chauffeur,Vehicule,Destination,TypeDeService
from django.shortcuts import get_object_or_404,redirect
from .forms import ClientForm 
from .forms import ChauffeurForm
from .forms import VehiculeForm
from .forms import DestinationForm
from .forms import TypeDeServiceForm
from .forms import TarificationForm




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


