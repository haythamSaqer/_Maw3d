# Generated by Django 3.2.15 on 2022-08-20 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import invite.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('inviteID', models.CharField(blank=True, editable=False, max_length=8, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('image', models.ImageField(default='/static/invites/images/placeholders/profile_image.jpg', upload_to=invite.models._get_invite_image_url, verbose_name='Invite Image')),
                ('duration', models.DurationField()),
                ('slotIncrement', models.IntegerField(choices=[(5, '5 minutes'), (10, '10 minutes'), (15, '15 minutes'), (20, '20 minutes'), (30, '30 minutes'), (60, '1 hour'), (120, '2 hours')], default=30)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('starDate', models.CharField(max_length=150)),
                ('endDate', models.CharField(max_length=150, null=True)),
                ('timezone', models.CharField(max_length=50)),
                ('preventConflict', models.BooleanField()),
                ('date_rang', models.DurationField()),
                ('eventNameFormat', models.CharField(blank=True, max_length=100)),
                ('displayedTimezone', models.IntegerField(choices=[(0, 'Invitee Local Timezone'), (1, 'Locked Timezone')], default=0)),
                ('showIntro', models.BooleanField()),
                ('showInYourProfilePage', models.BooleanField()),
                ('minimumNotice', models.IntegerField()),
                ('bufferBeforeEvent', models.IntegerField()),
                ('bufferAfterEvent', models.IntegerField()),
                ('limitMaxNumberEvents', models.BooleanField()),
                ('maxNumberEvents', models.IntegerField()),
                ('maxNumberEventsPer', models.CharField(blank=True, max_length=100)),
                ('allowGuests', models.BooleanField()),
                ('maxInvitees', models.IntegerField()),
                ('link_invite', models.URLField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_invites', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField()),
                ('rrule', models.CharField(max_length=255)),
                ('invite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='invite.invite')),
            ],
            options={
                'verbose_name': 'Availability',
                'verbose_name_plural': 'Invite Availability',
            },
        ),
    ]
