# Generated by Django 4.1.11 on 2023-09-12 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction_chat_open_at', models.DateTimeField()),
                ('auction_chat_close_at', models.DateTimeField(blank=True, null=True)),
                ('auction_chat_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.products')),
                ('auction_users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-auction_chat_open_at'],
            },
        ),
    ]