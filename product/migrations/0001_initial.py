# Generated by Django 3.0.3 on 2023-03-06 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Opinions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('recommended', models.CharField(max_length=200)),
                ('stars', models.CharField(max_length=200)),
                ('trust', models.CharField(max_length=200)),
                ('opinion_date', models.CharField(max_length=200)),
                ('buy_date', models.CharField(max_length=200)),
                ('useful_counter', models.CharField(max_length=200)),
                ('unuseful_counter', models.CharField(max_length=200)),
                ('opinion_desc', models.TextField()),
                ('pros', models.TextField()),
                ('cons', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Product')),
            ],
        ),
    ]
