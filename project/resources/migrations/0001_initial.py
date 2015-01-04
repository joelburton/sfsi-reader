# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='published', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('published', 'Published'), ('private', 'Private')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('absolute_url', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='published', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('published', 'Published'), ('private', 'Private')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('absolute_url', models.CharField(max_length=100)),
                ('link', models.URLField(help_text='Full URL to an externally-hosted resource.', blank=True)),
                ('file', models.FileField(upload_to='resources', blank=True)),
                ('file_size', models.PositiveIntegerField(null=True, blank=True)),
                ('file_mimetype', models.CharField(max_length=255, blank=True)),
                ('key', models.BooleanField(default=False, verbose_name='Key Resource?')),
                ('required', models.BooleanField(default=False, verbose_name='Required Reading?')),
                ('is_more', models.BooleanField(default=False, help_text='Check if this is the resource that should show up as "additional resources"', verbose_name='Additional Resources')),
                ('body', models.TextField(help_text='This is the extracted body of the PDF/remote link, used for searching.', blank='')),
            ],
            options={
                'ordering': ['-key', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=70, verbose_name='subject')),
                ('description', models.TextField(help_text='Describe the suggested resource.', blank=True)),
                ('topic', models.CharField(max_length=100, blank=True)),
                ('link', models.CharField(help_text='For web-based resources, please paste the URL here.', max_length=200, blank=True)),
                ('file', models.FileField(help_text='For file-based resources, please upload the file here.', upload_to='suggestions', blank=True)),
                ('name', models.CharField(help_text="If you'd like your submission to be confidential, you can clear this.", max_length=100, verbose_name='your name', blank=True)),
                ('email', models.EmailField(help_text="If you'd like your submission to be confidential, you can clear this.", max_length=75, verbose_name='your email', blank=True)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', model_utils.fields.StatusField(default='published', max_length=100, verbose_name='status', no_check_for_status=True, choices=[('published', 'Published'), ('private', 'Private')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('absolute_url', models.CharField(max_length=100)),
                ('position', models.PositiveSmallIntegerField(default=0, help_text='Ordering position with the day.')),
                ('day', models.ForeignKey(to='resources.Day')),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together=set([('title',), ('slug',)]),
        ),
        migrations.AddField(
            model_name='resource',
            name='topic',
            field=models.ForeignKey(to='resources.Topic'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('topic', 'slug'), ('topic', 'title')]),
        ),
        migrations.AlterIndexTogether(
            name='resource',
            index_together=set([('key', 'title')]),
        ),
        migrations.AlterUniqueTogether(
            name='day',
            unique_together=set([('title',), ('slug',)]),
        ),
    ]
