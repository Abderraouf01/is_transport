from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from core.utils import generate_tracking
from django.utils import timezone



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
    


     

 
class Facture(models.Model):
    STATUTFCT_CHOICES=[('non_payee', 'Non payée'),
                    ('partielle','Partiellement payée'),
                    ('payee', 'Payée'),]
    id_facture= models.CharField(max_length=20,unique=True)
    date_facture= models.DateField(auto_now_add=True)
    montant_HT= models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    montant_TVA= models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    montant_TTC= models.DecimalField(max_digits=10, decimal_places=2,editable=False)
    statut_facture=models.CharField(max_length=20, choices=STATUTFCT_CHOICES, default='non_payee')
    client= models.ForeignKey(Client, on_delete=models.CASCADE, related_name='factures')

    def __str__(self):
        return f"Facture {self.id_facture}"
    
    def calculer_montantfct(self):
       # Une facture agrège plusieurs expéditions
       montant_HT=self.expeditions.aggregate(total=Sum('montant_expedition')) ['total'] or 0
       montant_TVA= montant_HT * Decimal('0.19')
       montant_TTC= montant_HT + montant_TVA
       return montant_HT,montant_TVA,montant_TTC
    
    def save(self, *args,**kwargs):
       montant_HT,montant_TVA,montant_TTC=self.calculer_montantfct()
       self.montant_HT=montant_HT
       self.montant_TVA=montant_TVA
       self.montant_TTC=montant_TTC
       super().save(*args, **kwargs)

    def total_paye(self):
        return self.paiements.aggregate(total=Sum('montant_paiement'))['total'] or 0

    def reste_payer(self):
         return self.montant_TTC - self.total_paye()

    def update_statut(self):
        total_paye=self.total_paye()
        if total_paye==0 : 
         self.statut_facture='non_payee'
        elif total_paye<self.montant_TTC:
         self.statut_facture='partielle'
        else:
            self.statut_facture='payee'

        self.save(update_fields=['statut_facture'])   

    def delete(self, *args, **kwargs):
        if self.statut_facture == 'payee':
           raise ValueError("Impossible de supprimer un facture payée")
        client=self.client
        total_paiements= self.paiements.aggregate(total=Sum('montant_paiement'))['total'] or 0
        montant_restant= self.montant_TTC - total_paiements
        client.solde-= montant_restant
        client.save(update_fields=['solde'])
        self.paiements.all().delete()
        super().delete(*args, **kwargs)


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
     chauffeur= models.ForeignKey(Chauffeur,on_delete=models.PROTECT, related_name='tournees')
     vehicule = models.ForeignKey(Vehicule,on_delete=models.PROTECT,related_name='tournees')
     def __str__(self):
        return self.id_tournee
     


class Destination(models.Model):
   id_destination= models.CharField(max_length=50, unique=True)
   pays_dest= models.CharField(max_length=50)
   ville_dest= models.CharField(max_length=50)
   zone_geographique= models.CharField(max_length=50)
   tarif_base= models.DecimalField(max_digits=10 , decimal_places=2)

   def __str__(self):
     return f"{self.ville_dest},{self.pays_dest}"
   


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

class Tarification(models.Model):
    type_service = models.ForeignKey(TypeDeService,on_delete=models.CASCADE,related_name='tarifications')
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='tarifications')
    tarif_poids = models.DecimalField(max_digits=10, decimal_places=2)
    tarif_volume = models.DecimalField(max_digits=10, decimal_places=2)
    tarif_final = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
     return f"Tarif {self.type_service.nom_service} → {self.destination.ville_dest} : {self.tarif_final}"



     
# Business rules related to expedition lifecycle and pricing
class Expedition(models.Model):
   STATUT_CHOICES=[('cree','Crée'),
                   ('transit', 'En transit'),
                    ('tri','En centre de tri'),
                     ('livraison', 'En cours de livraison'),
                      ('livree','Livrée'),
                       ('echec', 'Echec de livraison'), ]
   
   tracking=models.CharField(max_length=50, unique=True,editable=False)
   statut_expedition=models.CharField(max_length=20,choices=STATUT_CHOICES, default='cree')
   date_creation_exp=models.DateTimeField(auto_now_add=True)
   description_exp= models.TextField(blank=True, null=True)
   montant_expedition= models.DecimalField(max_digits=10, decimal_places=2, default=0,editable=False)
   client= models.ForeignKey(Client, on_delete=models.CASCADE,related_name='expeditions')
   tournee=models.ForeignKey(Tournee, on_delete=models.SET_NULL, related_name='expeditions', null=True, blank=True)
   facture=models.ForeignKey(Facture, on_delete=models.SET_NULL, related_name='expeditions', null=True, blank=True)
   tarification= models.ForeignKey(Tarification, on_delete=models.PROTECT, related_name='expeditions')

   def __str__(self):
      return self.tracking
   def calculer_montant(self):
        total_poids = self.colis.aggregate(total=Sum('poids_colis'))['total'] or 0
        total_volume = self.colis.aggregate(total=Sum('volume_colis'))['total'] or 0
        destination = self.tarification.destination
        type_service = self.tarification.type_service
        tarif_base_reel = destination.tarif_base * type_service.coefficient_service
        return tarif_base_reel + (total_poids * self.tarification.tarif_poids) + (total_volume * self.tarification.tarif_volume)

   def save(self, *args, **kwargs):
        if not self.tracking:
            self.tracking = generate_tracking()

        self.montant_expedition = self.calculer_montant()
        super().save(*args, **kwargs)


   def can_be_deleted(self):
    return self.tournee is None and self.facture is None

   def can_add_colis(self):
    return self.statut_expedition == 'cree'
   
   def can_change_statut(self, new_statut):

    if self.statut_expedition in ['livree', 'echec']:
     return False
    
    transitions = {
       'cree': ['transit'],
       'transit': ['tri'],
       'tri': ['livraison'],
       'livraison': ['livree', 'echec'],
       'livree': [],
       'echec': [],
    }

    return new_statut in transitions.get(self.statut_expedition, [])
   
   def change_statut(self, new_statut):
      if not self.can_change_statut(new_statut):
        raise ValueError("Transition de statut non autorisée")

      self.statut_expedition = new_statut
      self.save(update_fields=['statut_expedition'])






class Reclamation(models.Model):
    ETAT_CHOICES = [
        ('en_cours', 'en cours de traitement'),
        ('resolue', 'résolue'),
        ('annulee', 'annulée'),
    ]
    id_reclamation = models.CharField(max_length=20, unique=True)
    nature_reclamation = models.CharField(max_length=150)
    date_reclamation = models.DateField(auto_now_add=True)
    date_resolution = models.DateField(null=True, blank=True)
    etat_reclamation = models.CharField(max_length=20,choices=ETAT_CHOICES,default='en_cours' )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reclamations')
    expedition = models.ForeignKey(Expedition,to_field='tracking',on_delete=models.PROTECT,null=True,blank=True,related_name='reclamations')  
    type_service = models.ForeignKey(TypeDeService,on_delete=models.PROTECT,null=True,blank=True,related_name='reclamations')
    facture= models.ForeignKey(Facture, on_delete=models.PROTECT, null=True, blank=True, related_name='reclamations')              
    agent_responsable= models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True, related_name='reclamations')
    def __str__(self):
      return self.id_reclamation
    
    def changer_etat(self, nouvel_etat, agent=None):
        if nouvel_etat not in dict(self.ETAT_CHOICES):
            raise ValueError("État invalide")
        self.etat_reclamation = nouvel_etat

        if nouvel_etat == 'resolue':
            self.date_resolution = timezone.now().date()

        if agent:
            self.agent_responsable = agent
        self.save(update_fields=['etat_reclamation', 'agent_responsable', 'date_resolution'])

class Colis(models.Model):
   id_colis= models.CharField(max_length=50, unique=True)
   poids_colis= models.DecimalField(max_digits=10 , decimal_places=2)
   volume_colis= models.DecimalField(max_digits=10 , decimal_places=2)
   description_colis= models.TextField()
   expedition= models.ForeignKey('Expedition',to_field='tracking',on_delete=models.CASCADE,related_name='colis')
  
   def __str__(self):
    return f"colis {self.id_colis}"
   
class Incident(models.Model):
     id_incident = models.CharField(max_length=20, unique=True)
     TYPE_INCIDENT_CHOICES = [
        ('retard', 'Retard'),
        ('perte', 'Perte'),
        ('endommagement', 'Endommagement'),
        ('probleme_technique', 'Problème technique'),]

     type_incident = models.CharField(
        max_length=30,
        choices=TYPE_INCIDENT_CHOICES)

     date_incident = models.DateField()
     description_incident = models.TextField()
     tournee = models.ForeignKey(Tournee,on_delete=models.PROTECT,related_name='incidents',null=True,blank=True)
     expedition = models.ForeignKey(Expedition,to_field='tracking',on_delete=models.PROTECT,related_name='incidents',null=True,blank=True)
     colis = models.ForeignKey(Colis,on_delete=models.PROTECT,related_name='incidents',null=True,blank=True)

     def __str__(self):
        return self.id_incident
     def save(self, *args, **kwargs):
          super().save(*args, **kwargs)
          expeditions = []
          if self.expedition:
              expeditions.append(self.expedition)

    
          elif self.colis and self.colis.expedition:
              expeditions.append(self.colis.expedition)
          elif self.tournee:
              expeditions = self.tournee.expeditions.all()
          for expedition in expeditions:
              if self.type_incident in ['perte', 'endommagement']:
                  expedition.statut_expedition = 'echec'

              elif self.type_incident == 'retard':
                  expedition.statut_expedition = 'transit'

              expedition.save(update_fields=['statut_expedition'])
              SuiviExpedition.objects.create(
                  id_suivi=f"SUIV-{self.id_incident}-{expedition.tracking}",
                  suivi_expedition=expedition,
                  lieu_passage="Incident déclaré",
                  commentaire=f"{self.type_incident} : {self.description_incident}" )
       


    

class SuiviExpedition(models.Model):
    id_suivi= models.CharField(max_length=20, unique=True,editable=False)
    date_passage= models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=Expedition.STATUT_CHOICES,default='cree')
    lieu_passage= models.CharField(max_length=50)
    commentaire= models.TextField()
    suivi_expedition= models.ForeignKey(Expedition,to_field='tracking', on_delete=models.CASCADE, related_name='suivi')

    def __str__(self):
        return f"Suivi {self.suivi_expedition.tracking} - {self.lieu_passage}"

    def save(self, *args, **kwargs):
     if not self.id_suivi:
        self.id_suivi = generate_tracking()
     super().save(*args, **kwargs)


   

class Paiement(models.Model):
    id_paiement = models.CharField(max_length=50,unique=True)
    mode_paiement = models.CharField(max_length=50)
    date_paiement = models.DateField()
    montant_paiement = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey('Client',on_delete=models.CASCADE,related_name='paiements' ,db_column='id_client_id' )
    facture = models.ForeignKey('Facture',on_delete=models.CASCADE,related_name='paiements' , db_column='id_facture_id')

    def __str__(self):
        return f"Paiement {self.id_paiement} - {self.montant_paiement}"

    def save(self, *args, **kwargs):
        if self.montant_paiement>self.facture.reste_payer():
           raise ValueError("Le montant du paiement est supérieur au reste à payer")
        super().save(* args, **kwargs)
        facture=self.facture
        facture.update_statut()
        reste= facture.reste_payer()
        facture.client.solde= max(reste,0)
        facture.client.save(update_fields=['solde'])


class ColisReclamation(models.Model):
    reclamation=models.ForeignKey(Reclamation,on_delete=models.CASCADE,related_name='colis_reclamations')
    colis=models.ForeignKey(Colis,on_delete=models.CASCADE,related_name='colis_reclamations')

    def __str__(self):
     return f"{self.reclamation.id_reclamation} / {self.colis.id_colis}"
    







   

