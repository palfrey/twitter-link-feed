# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ListData'
        db.create_table(u'twitterFeed_listdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterFeed.TwitterAuthToken'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('last', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'twitterFeed', ['ListData'])


    def backwards(self, orm):
        # Deleting model 'ListData'
        db.delete_table(u'twitterFeed_listdata')


    models = {
        u'twitterFeed.listdata': {
            'Meta': {'object_name': 'ListData'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['twitterFeed.TwitterAuthToken']"})
        },
        u'twitterFeed.twitterauthtoken': {
            'Meta': {'object_name': 'TwitterAuthToken'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'last': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'timeline': ('django.db.models.fields.TextField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['twitterFeed']