from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nom} {self.prenom}"