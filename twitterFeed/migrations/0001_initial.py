# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TwitterAuthToken'
        db.create_table(u'twitterFeed_twitterauthtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('timeline', self.gf('django.db.models.fields.TextField')()),
            ('last', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'twitterFeed', ['TwitterAuthToken'])


    def backwards(self, orm):
        # Deleting model 'TwitterAuthToken'
        db.delete_table(u'twitterFeed_twitterauthtoken')


    models = {
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