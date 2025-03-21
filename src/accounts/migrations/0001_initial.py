# Generated by Django 5.1.7 on 2025-03-14 09:41

import django.contrib.auth.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(blank=True, choices=[('Homme', 'Homme'), ('Femme', 'Femme'), ('Autre', 'Autre')], max_length=10)),
                ('nationality', models.CharField(blank=True, max_length=50)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('city', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_active', models.DateTimeField(blank=True, null=True)),
                ('languages', models.JSONField(blank=True, default=list, null=True)),
                ('followers_count', models.PositiveIntegerField(default=0)),
                ('following_count', models.PositiveIntegerField(default=0)),
                ('like_count', models.PositiveIntegerField(default=0)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('user_type', models.CharField(choices=[('client', 'Client'), ('model', 'Model'), ('administrator', 'Administrator')], default='client', max_length=15)),
                ('is_verified', models.BooleanField(default=False)),
                ('two_factor_enabled', models.BooleanField(default=False, verbose_name='two-factor authentication')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ['-date_joined'],
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40, verbose_name='session key')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP address')),
                ('user_agent', models.TextField(verbose_name='user agent')),
                ('device_type', models.CharField(max_length=20, verbose_name='device type')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='location')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='started at')),
                ('last_activity', models.DateTimeField(auto_now=True, verbose_name='last activity')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user session',
                'verbose_name_plural': 'user sessions',
                'ordering': ['-last_activity'],
            },
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user following',
                'verbose_name_plural': 'user followings',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'following_user')},
            },
        ),
    ]
