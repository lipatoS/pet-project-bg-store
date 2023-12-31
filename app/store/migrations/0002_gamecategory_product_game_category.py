# Generated by Django 4.2.5 on 2023-09-21 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_category_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='game_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.gamecategory'),
        ),
    ]
