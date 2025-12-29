from django.db import models


class Client(models.Model):
    id_client = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
      return f"{self.nom} {self.prenom}"

class Reclamation(models.Model):
    id_reclamation = models.CharField(max_length=20, unique=True)
    nature_reclamation = models.CharField(max_length=150)
    date_reclamation = models.DateField(auto_now_add=True)
    etat_reclamation =models.CharField(max_length=50, default='En cours')
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reclamations')
                                
    def __str__(self):
      return self.id_reclamation