# Generated by Django 5.0.6 on 2024-06-29 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LaTiendita', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='LaTiendita/media/productos/', verbose_name='Imagen del producto'),
        ),
        migrations.AlterField(
            model_name='carrito',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre cliente'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
