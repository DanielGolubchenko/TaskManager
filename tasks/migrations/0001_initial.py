# Generated by Django 5.1.7 on 2025-03-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'), ('Urgent', 'Urgent')], max_length=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('In progress', 'In progress'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], max_length=15)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tags', models.CharField(blank=True, choices=[('Work', 'Work'), ('Studies', 'Studies'), ('Home', 'Home'), ('Meetings', 'Meetings'), ('Goals', 'Goals'), ('Reading', 'Reading'), ('Shopping', 'Shopping'), ('Bills', 'Bills')], max_length=50, null=True)),
            ],
        ),
    ]
