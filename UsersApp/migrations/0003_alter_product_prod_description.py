# Generated by Django 4.2.11 on 2024-03-24 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UsersApp', '0002_alter_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prod_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
