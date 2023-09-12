from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, null=True, verbose_name='사용자 이름')),
                ('phone_number', models.CharField(max_length=255, unique=True, verbose_name='핸드폰 번호')),
                ('nickname', models.CharField(max_length=255, unique=True, verbose_name='닉네임')),
                ('address', models.TextField(verbose_name='주소')),
                ('profile_image', models.ImageField(blank=True, upload_to='profile_image', verbose_name='프로필 사진')),
                ('is_admin', models.BooleanField(default=False, verbose_name='관리자 권한')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
