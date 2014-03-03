# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Day', fields ['slug']
        db.delete_unique(u'resources_day', ['slug'])

        # Adding unique constraint on 'Day', fields ['slug', 'title']
        db.create_unique(u'resources_day', ['slug', 'title'])


    def backwards(self, orm):
        # Removing unique constraint on 'Day', fields ['slug', 'title']
        db.delete_unique(u'resources_day', ['slug', 'title'])

        # Adding unique constraint on 'Day', fields ['slug']
        db.create_unique(u'resources_day', ['slug'])


    models = {
        u'resources.day': {
            'Meta': {'ordering': "[u'title']", 'unique_together': "([u'slug', u'title'],)", 'object_name': 'Day'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "u'private'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'resources.resource': {
            'Meta': {'ordering': "[u'-key', u'title']", 'unique_together': "([u'topic', u'slug'],)", 'object_name': 'Resource'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'file_mimetype': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'file_size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "u'private'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resources.Topic']"})
        },
        u'resources.topic': {
            'Meta': {'ordering': "[u'position']", 'unique_together': "([u'day', u'slug'],)", 'object_name': 'Topic'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['resources.Day']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "u'private'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'status_changed': ('model_utils.fields.MonitorField', [], {'default': 'datetime.datetime.now', u'monitor': "u'status'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['resources']