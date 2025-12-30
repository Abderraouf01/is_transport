from django.db import models
from django.contrib.auth.models import User

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
   
   tracking=models.CharField(max_length=50, unique=True)
   statut_expedition=models.CharField(max_length=20,choices=STATUT_CHOICES, default='cree')
   date_creation_exp=models.DateTimeField(auto_now_add=True)
   description_exp= models.TextField()
   montant_expedition= models.DecimalField(max_digits=10, decimal_places=2, default=0)
   client= models.ForeignKey(Client, on_delete=models.CASCADE,related_name='expeditions')
   def __str__(self):
      return self.tracking


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
    coefficient_service = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.nom_service


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reclamations')
    expedition = models.ForeignKey(Expedition,on_delete=models.SET_NULL,null=True,blank=True,related_name='reclamations')  
    type_service = models.ForeignKey(TypeDeService,on_delete=models.SET_NULL,null=True,blank=True,related_name='reclamations')                    

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
     return f"{self.nom_chauffeur} {self.prenom_chauffeur}"
    


    
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


class Tournee(models.Model):
     id_tournee = models.CharField(max_length=20, unique=True)
     date_tournee = models.DateField()
     kilometrage = models.FloatField()
     duree = models.PositiveIntegerField(help_text="duree de la tournee par heurs")
     note = models.TextField (blank=True, null=True)
     chauffeur= models.ForeignKey(Chauffeur,to_field='num_permis',on_delete=models.CASCADE, related_name='tournees')
     vehicule = models.ForeignKey(Vehicule,to_field='immatriculation',on_delete=models.CASCADE,related_name='tournees')
     def __str__(self):
        return self.id_tournee
     
     
class Incident(models.Model):
     id_incident = models.CharField(max_length=20, unique=True)
     type_incident = models.CharField(max_length=100)
     date_incident = models.DateField()
     description_incident = models.TextField()
     tournee = models.ForeignKey(Tournee,to_field='id_tournee',on_delete=models.CASCADE,related_name='incidents')
     expedition = models.ForeignKey(Expedition,to_field='tracking',on_delete=models.CASCADE,related_name='incidents')

     def __str__(self):
        return self.id_incident


    

class SuiviExpedition(models.Model):
    id_suivi= models.CharField(max_length=20, unique=True)
    date_passage= models.DateTimeField(auto_now_add=True)
    lieu_passage= models.CharField(max_length=50)
    commentaire= models.TextField()
    suivi_expedition= models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='suivi')

    def __str__(self):
        return f"Suivi {self.suivi_expedition.tracking} - {self.lieu_passage}"

class Facture(models.Model):
    STATUTFCT_CHOICES=[('non_payee', 'Non payée'),
                    ('partielle','Partiellement payée'),
                    ('payee', 'Payée'),]
    id_facture= models.CharField(max_length=20,unique=True)
    date_facture= models.DateField(auto_now_add=True)
    montant_HT= models.DecimalField(max_digits=10, decimal_places=2)
    montant_TVA= models.DecimalField(max_digits=10, decimal_places=2)
    montant_TTC= models.DecimalField(max_digits=10, decimal_places=2)
    statut_facture=models.CharField(max_length=20, choices=STATUTFCT_CHOICES, default='non_payee')
    client= models.ForeignKey(Client, on_delete=models.CASCADE, related_name='factures')

    def __str__(self):
        return f"Facture {self.id_facture}"
    

class Destination(models.Model):
   id_destination= models.CharField(max_length=50, unique=True)
   pays_dest= models.CharField(max_length=50)
   ville_dest= models.CharField(max_length=50)
   zone_geographique= models.CharField(max_length=50)
   tarif_base= models.DecimalField(max_digits=10 , decimal_places=2)

   def __str__(self):
     return f"{self.ville_dest},{self.pays_dest}"
   
class Colis(models.Model):
   id_colis= models.CharField(max_length=50, unique=True)
   poids_colis= models.DecimalField(max_digits=10 , decimal_places=2)
   volume_colis= models.DecimalField(max_digits=10 , decimal_places=2)
   description_colis= models.TextField()
   statue_colis= models.CharField(max_length=50)
   expedition= models.ForeignKey('Expedition',on_delete=models.CASCADE,related_name='colis')
  
   def __str__(self):
    return f"colis {self.id_colis} - {self.statue_colis}"
   
class Paiement(models.Model):
    id_paiement = models.CharField(max_length=50,unique=True)
    mode_paiement = models.CharField(max_length=50)
    date_paiement = models.DateField()
    montant_paiement = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey('Client',on_delete=models.CASCADE,related_name='paiements')
    facture = models.ForeignKey('Facture',on_delete=models.CASCADE,related_name='paiements')

    def __str__(self):
        return f"Paiement {self.id_paiement} - {self.montant_paiement}"
    
class Tarification(models.Model):
    type_service = models.ForeignKey('TypeDeService',on_delete=models.CASCADE,related_name='tarifications',blank=True,null=True)
    destination = models.ForeignKey('Destination',on_delete=models.CASCADE,related_name='tarifications',blank=True,null=True)
    tarif_poids = models.DecimalField(max_digits=10, decimal_places=2)
    tarif_volume = models.DecimalField(max_digits=10, decimal_places=2)
    tarif_final = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
     return f"Tarif {self.type_service.nom_service} → {self.destination.ville_dest} : {self.tarif_final}"
 
 

class ColisReclamation(models.Model):
    reclamation=models.ForeignKey(Reclamation,on_delete=models.CASCADE,related_name='colis_reclamations')
    colis=models.ForeignKey(Colis,on_delete=models.CASCADE,related_name='colis_reclamations')

    def __str__(self):
     return f"{self.reclamation.id_reclamation} / {self.colis.id_colis}"
    


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('AGENT', 'Agent'),
        ('RESP', 'Responsable'),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=10,choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"



  
   

