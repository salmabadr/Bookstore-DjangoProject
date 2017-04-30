# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 00:16
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bornAt', models.DateField()),
                ('diedAt', models.DateField()),
                ('contact', models.IntegerField()),
                ('bio', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('publishedAt', models.DateField()),
                ('summary', models.CharField(max_length=300)),
                ('country', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FavouriteCat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Category')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowingAuthor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Author')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBookRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('status', models.CharField(choices=[('read', 'read'), ('wish', 'add to wishlist'), ('reading', 'reading')], max_length=100)),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Book')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='usersids',
            field=models.ManyToManyField(through='library.FavouriteCat', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='usersids',
            field=models.ManyToManyField(through='library.UserBookRel', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Author'),
        ),
        migrations.AddField(
            model_name='author',
            name='usersids',
            field=models.ManyToManyField(through='library.FollowingAuthor', to=settings.AUTH_USER_MODEL),
        ),
    ]