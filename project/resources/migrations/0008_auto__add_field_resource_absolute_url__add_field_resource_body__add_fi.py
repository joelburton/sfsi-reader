# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Resource.absolute_url'
        db.add_column(u'resources_resource', 'absolute_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Resource.body'
        db.add_column(u'resources_resource', 'body',
                      self.gf('django.db.models.fields.TextField')(default='', blank=u''),
                      keep_default=False)

        # Adding field 'Day.absolute_url'
        db.add_column(u'resources_day', 'absolute_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Topic.absolute_url'
        db.add_column(u'resources_topic', 'absolute_url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Resource.absolute_url'
        db.delete_column(u'resources_resource', 'absolute_url')

        # Deleting field 'Resource.body'
        db.delete_column(u'resources_resource', 'body')

        # Deleting field 'Day.absolute_url'
        db.delete_column(u'resources_day', 'absolute_url')

        # Deleting field 'Topic.absolute_url'
        db.delete_column(u'resources_topic', 'absolute_url')


    models = {
        u'resources.day': {
            'Meta': {'ordering': "[u'title']", 'unique_together': "[[u'slug'], [u'title']]", 'object_name': 'Day'},
            'absolute_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'Meta': {'ordering': "[u'-key', u'title']", 'unique_together': "[[u'topic', u'slug'], [u'topic', u'title']]", 'object_name': 'Resource', 'index_together': "[[u'key', u'title']]"},
            'absolute_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': "u''"}),
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
            'Meta': {'ordering': "[u'position']", 'unique_together': "[[u'day', u'slug'], [u'day', u'title']]", 'object_name': 'Topic'},
            'absolute_url': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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