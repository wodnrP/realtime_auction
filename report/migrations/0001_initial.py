from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
# <<<<<<< suhyun
#         ('auction', '0001_initial'),
# =======
# >>>>>>> develop
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('profanity', '욕설'), ('advertisement', '광고'), ('spam', '스팸 및 도배')], max_length=30)),
                ('report_at', models.DateTimeField(auto_now_add=True)),
                ('report_content', models.TextField()),
                ('report_chatting_room', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auction.auction')),
                ('report_suspect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suspects', to=settings.AUTH_USER_MODEL)),
                ('reporter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reports',
                'ordering': ['-report_at'],
            },
        ),
    ]
