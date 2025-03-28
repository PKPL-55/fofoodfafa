# Generated by Django 5.1.7 on 2025-03-27 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Dikonfirmasi', 'Dikonfirmasi'), ('Selesai', 'Selesai')], default='Dikonfirmasi', max_length=20)),
                ('discount', models.JSONField(blank=True, null=True)),
                ('payment', models.JSONField(blank=True, null=True)),
                ('cart_items', models.ManyToManyField(to='checkout.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
