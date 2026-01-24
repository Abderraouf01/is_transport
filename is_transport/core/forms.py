from django import forms 
from .models import Client ,Chauffeur , Vehicule , Destination ,TypeDeService,Tarification , Incident, Expedition, Facture, Paiement

class ClientForm (forms.ModelForm):
    class Meta :
        model = Client 
        fields = '__all__'
        widgets = {
            'adresse' : forms.Textarea(attrs={'rows': 3}),
        }

class ChauffeurForm(forms.ModelForm):
    class Meta:
        model = Chauffeur
        fields = '__all__'
        widgets = {
            'adresse_chauffeur': forms.Textarea(attrs={'rows': 3}),
            'date_embauchement': forms.DateInput(attrs={'type': 'date'}),
        }

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = '__all__'

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'

class TypeDeServiceForm(forms.ModelForm):
    class Meta:
        model = TypeDeService
        fields = '__all__'
        widgets = {
            'description_service': forms.Textarea(attrs={'rows': 3}),
        }

class TarificationForm(forms.ModelForm):
    class Meta:
        model = Tarification
        fields = '__all__'

      

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['id_incident', 'type_incident', 'date_incident', 'description_incident', 'tournee', 'expedition', 'colis']
        widgets = {
            'date_incident': forms.DateInput(attrs={'type': 'date'}),
            'description_incident': forms.Textarea(attrs={'rows': 3}),
        }

class FactureForm(forms.ModelForm):
    expeditions = forms.ModelMultipleChoiceField(
        queryset=Expedition.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Expéditions associées"
    )

    class Meta:
        model = Facture
        fields = ['id_facture', 'client']

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['id_paiement', 'client', 'facture', 'date_paiement', 'montant_paiement', 'mode_paiement']
        widgets = {
            'date_paiement': forms.DateInput(attrs={'type': 'date'}),
            'mode_paiement': forms.Select(),
        }

    def clean_montant_paiement(self):
        montant = self.cleaned_data['montant_paiement']
        facture = self.cleaned_data.get('facture')
        if facture and montant > facture.reste_payer():
            raise forms.ValidationError("Le montant du paiement est supérieur au reste à payer de la facture.")
        return montant