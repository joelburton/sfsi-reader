# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.execute("ALTER TABLE resources_topic ADD search tsvector")
        db.execute("""
        CREATE FUNCTION topic_search_trigger() RETURNS trigger AS $$
        begin
          new.search := setweight(to_tsvector('pg_catalog.english', new.title), 'A') ||
                        setweight(to_tsvector('pg_catalog.english', new.description), 'B');
          return new;
        end
        $$ LANGUAGE plpgsql
        """)
        db.execute("""
        CREATE TRIGGER topic_search_update BEFORE INSERT OR UPDATE ON resources_topic
        FOR EACH ROW EXECUTE PROCEDURE topic_search_trigger();
        """)
        db.execute("""CREATE INDEX resources_topic_search ON resources_topic USING GIN ( "search" )""")

        db.execute("ALTER TABLE resources_resource ADD search tsvector")
        #db.add_column(u'resources_resource', 'body',
        #              self.gf('django.db.models.fields.TextField')(default=''),
        #              keep_default=True)
        db.execute("""
        CREATE FUNCTION resource_search_trigger() RETURNS trigger AS $$
        begin
          new.search := setweight(to_tsvector('pg_catalog.english', new.title), 'A') ||
                        setweight(to_tsvector('pg_catalog.english', new.description), 'B') ||
                        setweight(to_tsvector('pg_catalog.english', new.link), 'C') ||
                        setweight(to_tsvector('pg_catalog.english', new.file), 'C') ||
                        setweight(to_tsvector('pg_catalog.english', new.body), 'D');
          return new;
        end
        $$ LANGUAGE plpgsql
        """)
        db.execute("""
        CREATE TRIGGER resource_search_update BEFORE INSERT OR UPDATE ON resources_resource
        FOR EACH ROW EXECUTE PROCEDURE resource_search_trigger();
        """)


    def backwards(self, orm):
            db.execute("""DROP INDEX resources_topic_search""")
            db.execute("""DROP TRIGGER topic_search_update ON resources_topic""")
            db.execute("""DROP FUNCTION topic_search_trigger()""")
            db.execute("""ALTER TABLE resources_topic DROP search""")


    models = {
            u'resources.day': {
                'Meta': {'ordering': "[u'title']", 'unique_together': "[[u'slug'], [u'title']]", 'object_name': 'Day'},
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
