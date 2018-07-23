# Generated by Django 2.0.7 on 2018-07-23 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ej_conversations', '0008_auto_20180722_2258'),
        ('ej_users', '0003_user_board_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_conversations',
            field=models.ManyToManyField(to='ej_conversations.Conversation'),
        ),
        migrations.AlterField(
            model_name='user',
            name='board_name',
            field=models.CharField(blank=True, default='defaultboard', help_text='The name of the conversation board of an user.', max_length=140, verbose_name='Board name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
