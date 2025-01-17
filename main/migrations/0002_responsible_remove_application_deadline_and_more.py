# Generated by Django 5.0.6 on 2024-11-01 19:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='application',
            name='deadline',
        ),
        migrations.AddField(
            model_name='application',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('completed', 'Выполненные'), ('incomplete', 'Невыполненные'), ('done', 'Исполнено'), ('in_progress', 'В процессе')], default='in_process', max_length=20),
        ),
        migrations.AlterField(
            model_name='application',
            name='title',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='application',
            name='responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.responsible'),
        ),
    ]
