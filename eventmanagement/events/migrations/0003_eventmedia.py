# Generated by Django 3.1.7 on 2021-06-24 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20210624_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='events/media/')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventmedia', to='events.event')),
            ],
            options={
                'verbose_name': 'event media',
                'verbose_name_plural': 'event media',
                'ordering': ('-created',),
                'default_related_name': 'eventmedia',
            },
        ),
    ]