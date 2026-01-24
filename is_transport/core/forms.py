from django import forms 
from .models import Client ,Chauffeur , Vehicule , Destination ,TypeDeService,Tarification 

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

      