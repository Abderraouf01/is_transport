from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_facture_montant_ht_alter_facture_montant_ttc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_colis', models.CharField(max_length=50, unique=True)),
                ('poids_colis', models.DecimalField(max_digits=10, decimal_places=2)),
                ('volume_colis', models.DecimalField(max_digits=10, decimal_places=2)),
                ('description_colis', models.TextField()),
                ('expedition', models.ForeignKey(
                    to='core.Expedition', 
                    to_field='tracking', 
                    on_delete=models.CASCADE, 
                    related_name='colis'
                )),
            ],
        ),
    ]
