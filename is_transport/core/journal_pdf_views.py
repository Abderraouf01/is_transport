from django.shortcuts import render, get_object_or_404
from .models import Facture, Paiement
from django.http import HttpResponse
from weasyprint import HTML


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
        'factures': factures}

    return render(request, 'journal_factures.html', context)

def detail_facture(request,id_facture):
    facture=get_object_or_404(Facture, id_facture=id_facture)
    paiements= facture.paiements.all()
    expeditions= facture.expeditions.all()
    context={ 'facture': facture,
             'expeditions':expeditions,
             'paiements':paiements,
             }
    return render(request, 'detail_facture.html', context)

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

    return render(request, 'journal_paiements.html', {'paiements':paiements })


def detail_paiement(request, id_paiement):
    paiement=get_object_or_404(Paiement, id_paiement=id_paiement)
    context={'paiement': paiement}

    return render(request, 'detail_paiement.html',context)


def facture_pdf(request, id_facture):
    facture= get_object_or_404(Facture, id_facture=id_facture)
    expeditions=facture.expeditions.all()
    paiements= facture.paiements.all()
    
    context={
        'facture':facture,
        'expeditions': expeditions,
        'paiements': paiements,
    }

    html_string= render(request, 'factures/detail_facture.html', context).content.decode('utf-8')

    # création du PDF
    pdf_file= HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="facture_{facture.id_facture}.pdf"'
    return response

def paiement_pdf(request, id_paiement):
    paiement=get_object_or_404(Paiement, id_paiement=id_paiement)
    context={'paiement':paiement}
    html_string= render(request, 'paiements/detail_paiement.html', context).content.decode('utf-8')

    # création du PDF
    pdf_file=HTML(string=html_string).write_pdf()

    # Retourne le PDF au navigateur avec un nom de fichier
    response= HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="paiement_{paiement.id_paiement}.pdf"'
    return response