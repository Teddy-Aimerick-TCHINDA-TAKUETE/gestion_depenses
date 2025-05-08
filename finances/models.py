from django.db import models
from django.contrib.auth.models import User  # Django gère déjà les utilisateurs de façon sécurisée

class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


CATEGORIES_DEPENSE = [
    ('Logement', 'Logement'),
    ('Transport', 'Transport'),
    ('Nourriture', 'Nourriture'),
    ('Loisirs', 'Loisirs'),
    ('Santé', 'Santé'),
    ('Autres', 'Autres'),
]

class Expense(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Dépense sans titre")  # nécessaire selon tes formulaires HTML
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50, choices=CATEGORIES_DEPENSE, default='Autres')
    date = models.DateField()
    description = models.TextField(blank=True, default="Dépense sans description")

    def __str__(self):
        return f"Depense: {self.title} de {self.amount} € le ({self.date})"


CATEGORIES_REVENUE = [
    ('Salaire', 'Salaire'),
    ('Prime', 'Prime'),
    ('Vente', 'Vente'),
    ('Cadeau', 'Cadeau'),
    ('Autres', 'Autres'),
]

class Revenue(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Revenue sans titre")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50, choices=CATEGORIES_REVENUE, default='Autres')
    date = models.DateField()
    description = models.TextField(blank=True, default="Revenue sans description")

    def __str__(self):
        return f"Revenue: {self.title} de {self.amount} € le {self.date}"