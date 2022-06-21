# Generated by Django 4.0.5 on 2022-06-21 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '__first__'),
        ('shoppers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('amount', models.CharField(max_length=16)),
                ('created_at', models.CharField(max_length=20)),
                ('completed_at', models.CharField(max_length=20)),
                ('disembursed', models.BooleanField(default=False)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='merchants.merchant')),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shoppers.shopper')),
            ],
        ),
    ]