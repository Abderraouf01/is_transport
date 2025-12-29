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
    


class Expedition(models.Model):
   STATUT_CHOICES=[('cree','Crée'),
                   ('transit', 'En transit'),
                    ('tri','En centre de tri'),
                     ('livraison', 'En cours de livraison'),
                      ('livree','Livrée'),
                       ('echec', 'Echec de livraison'), ]
   
   Tracking=models.CharField(max_length=50, unique=True)
   Statut_expedition=models.CharField(max_length=20,choices=STATUT_CHOICES, default='cree')
   Date_creation_exp=models.DateTimeField(auto_now_add=True)
   Description_exp= models.TextField()
   Montant_expedition= models.DecimalField(max_digits=10, decimal_places=2, default=0)
   id_client= models.ForeignKey(Client, on_delete=models.CASCADE,related_name='expeditions')
   def __str__(self):
      return self.Tracking
   


class Reclamation(models.Model):
    ETAT_CHOICES = [
        ('en_cours', 'en cours de traitement'),
        ('resolue', 'résolue'),
        ('annulee', 'annulée'),
    ]
    id_reclamation = models.CharField(max_length=20, unique=True)
    nature_reclamation = models.CharField(max_length=150)
    date_reclamation = models.DateField(auto_now_add=True)
    etat_reclamation = models.CharField(max_length=20,choices=ETAT_CHOICES,default='en_cours' )
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reclamations')
    Tracking_Expedition = models.ForeignKey(Expedition,on_delete=models.SET_NULL,null=True,blank=True,related_name='reclamations')                       
    def __str__(self):
      return self.id_reclamation
    

    
class Chauffeur(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'disponible'),
        ('non_disponible', 'non disponible'),
    ]
    num_permis = models.CharField(max_length=20, unique=True)
    nom_chauffeur = models.CharField(max_length=100)
    prenom_chauffeur = models.CharField(max_length=100)
    adresse_chauffeur = models.TextField()
    statut_chauffeur =models.CharField(max_length=20,choices=STATUT_CHOICES,default='disponible')
    email_chauffeur = models.EmailField(unique=True)
    tel_chauffeur = models.CharField(max_length=10)
    categ_permis = models.CharField(max_length=20)
    date_embauchement = models.DateField()
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    



class TypeDeService(models.Model):
    TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('express', 'Express'),
        ('international', 'International'),
    ]

    code_service = models.CharField(max_length=20, unique=True)
    nom_service = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description_service = models.TextField(blank=True)
    delai_estime = models.PositiveIntegerField(help_text="Délai estimé en jours")
    CoefficientService = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.nom_service
    

    
class Vehicule(models.Model):
    ETAT_CHOICES = [
        ('disponible', 'Disponible'),
        ('en_panne', 'En panne'),
        ('en_tournee', 'En tournée'),
    ]

    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=50)
    capacite_kg = models.FloatField()
    consommation_litre_100km = models.FloatField()
    etat_vehicule = models.CharField(max_length=20,choices=ETAT_CHOICES,default='disponible')

    def __str__(self):
        return self.immatriculation


