from django.shortcuts import render, get_object_or_404
from .models import Facture, Paiement, Reclamation,Client,Colis
from django.http import HttpResponse
from weasyprint import HTML
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from django.utils.timezone import now
from django.template.loader import render_to_string

def journal_factures(request):
    factures=Facture.objects.all()

    client= request.GET.get('client')
    statut= request.GET.get('statut')
    date_debut=request.GET.get('date_debut')
    date_fin=request.GET.get('date_fin')

    if client:
        factures=factures.filter(client__id_client=client)
    if statut:
        factures=factures.filter(statut_facture=statut)
    if date_debut and date_fin:
        factures=factures.filter(date_facture__range=[date_debut, date_fin])
    elif date_debut:
        factures=factures.filter(date_facture__gte=date_debut)
    elif date_fin:
        factures=factures.filter(date_facture__lte=date_fin)
        
    context= {
        'factures': factures,
        'clients': Client.objects.all(),
        'statuts': Facture.STATUTFCT_CHOICES,}

    return render(request, 'core/journal_factures.html', context)

def detail_facture(request,id_facture):
    facture=get_object_or_404(Facture, id_facture=id_facture)
    paiements= facture.paiements.all()
    expeditions= facture.expeditions.all()
    context={ 'facture': facture,
             'expeditions':expeditions,
             'paiements':paiements,
             }
    return render(request, 'core/detail_facture.html', context)

def journal_paiements(request):
    paiements=Paiement.objects.all()

    client=request.GET.get('client')
    date_debut=request.GET.get('date_debut')
    date_fin=request.GET.get('date_fin')
    mode_paiement=request.GET.get('mode_paiement')

    if client:
        paiements=paiements.filter(client__id_client=client)
    if mode_paiement:
        paiements=paiements.filter(mode_paiement=mode_paiement)
    if date_debut and date_fin:
        paiements=paiements.filter(date_paiement__range=[date_debut,date_fin])
    elif date_debut:
        paiements=paiements.filter(date_paiement__gte=date_debut)
    elif date_fin:
        paiements=paiements.filter(date_paiement__lte=date_fin)
        
    return render(request, 'core/journal_paiements.html', {
        'paiements': paiements,
        'clients': Client.objects.all(),
        'modes': Paiement.MODE_PAIEMENT_CHOICES,
    })

def detail_paiement(request, id_paiement):
    paiement=get_object_or_404(Paiement, id_paiement=id_paiement)
    context={'paiement': paiement}

    return render(request, 'core/detail_paiement.html',context)

def journal_reclamations(request):
    reclamations=Reclamation.objects.all()

    client=request.GET.get('client')
    etat=request.GET.get('etat')
    date_debut=request.GET.get('date_debut')
    date_fin=request.GET.get('date_fin')

    if client:
        reclamations=reclamations.filter(client__id_client=client)
    if etat:
        reclamations=reclamations.filter(etat_reclamation=etat)
    if date_debut and date_fin:
        reclamations = reclamations.filter(date_reclamation__range=[date_debut, date_fin])
    elif date_debut:
        reclamations = reclamations.filter(date_reclamation__gte=date_debut)
    elif date_fin:
        reclamations = reclamations.filter(date_reclamation__lte=date_fin)
    
    stats_par_etat = (
        Reclamation.objects.values('etat_reclamation').annotate(total=Count('id'))
    )

    ETAT_LABELS = dict(Reclamation.ETAT_CHOICES)
    for s in stats_par_etat:
        s['etat_reclamation'] = ETAT_LABELS.get(s['etat_reclamation'], s['etat_reclamation'])
    reclamations_resolues=Reclamation.objects.filter(
        etat_reclamation='resolue',
        date_resolution__isnull=False
    )
    delai_moyen = reclamations_resolues.annotate(
        delai=ExpressionWrapper(F('date_resolution') - F('date_reclamation'), output_field=DurationField())
    ).aggregate(moyenne=Avg('delai'))['moyenne']

    motifs_recurrents = Reclamation.objects.values('nature_reclamation') \
        .annotate(total=Count('id')).order_by('-total')

    context={'reclamations': reclamations,
        'etats': Reclamation.ETAT_CHOICES,
        'clients': Client.objects.all(),
        'stats_par_etat': stats_par_etat,
        'delai_moyen': delai_moyen,
        'motifs_recurrents': motifs_recurrents,
    }
    return render(request, 'core/journal_reclamations.html', context)

def detail_reclamation(request, id_reclamation):
    reclamation= get_object_or_404(Reclamation, id_reclamation=id_reclamation)
    colis_disponibles = []
    if reclamation.expedition:
        colis_disponibles = Colis.objects.filter(
            expedition=reclamation.expedition
        )

    context = {
        'reclamation': reclamation,
        'colis_disponibles': colis_disponibles,
    }

    return render(request, 'core/detail_reclamation.html',context)

    


def facture_pdf(request, id_facture):
    facture = get_object_or_404(Facture, id_facture=id_facture)
    expeditions = facture.expeditions.all()
    paiements = facture.paiements.all()
    
    facture.recalculer()
    
    context = {
        'facture': facture,
        'expeditions': expeditions,
        'paiements': paiements,
    }

    html_string = render_to_string('core/facture_pdf.html', context)

    # création du PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # retourne le pdf au navigateur avec un nom de fichier
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="facture_{facture.id_facture}.pdf"'
    return response



def paiement_pdf(request, id_paiement):
    paiement = get_object_or_404(Paiement, id_paiement=id_paiement)
    context = {'paiement': paiement}

    html_string = render_to_string('core/paiement_pdf.html', context)

    # création du PDF
    pdf_file = HTML(string=html_string).write_pdf()

    # Retourne le PDF au navigateur avec un nom de fichier
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="paiement_{paiement.id_paiement}.pdf"'
    return response


