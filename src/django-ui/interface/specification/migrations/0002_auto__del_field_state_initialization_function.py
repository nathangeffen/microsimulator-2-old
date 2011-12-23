# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'State.initialization_function'
        db.delete_column('specification_state', 'initialization_function')


    def backwards(self, orm):
        
        # Adding field 'State.initialization_function'
        db.add_column('specification_state', 'initialization_function', self.gf('django.db.models.fields.CharField')(default='0', max_length=3), keep_default=False)


    models = {
        'specification.entry': {
            'Meta': {'object_name': 'Entry'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lower': ('django.db.models.fields.FloatField', [], {}),
            'match_function': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'transition_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.TransitionRecord']"}),
            'upper': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'specification.initializationfunctionparameter': {
            'Meta': {'object_name': 'InitializationFunctionParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'specification.specifiedinitialvalue': {
            'Meta': {'object_name': 'SpecifiedInitialValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'probability': ('django.db.models.fields.FloatField', [], {}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'specification.state': {
            'Meta': {'object_name': 'State'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'specification.transitionrecord': {
            'Meta': {'object_name': 'TransitionRecord'},
            'assign_function': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'probability': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'probability_normalize_function': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'probability_time_period': ('django.db.models.fields.FloatField', [], {'default': '365.25'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'value_normalize_function': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'value_time_period': ('django.db.models.fields.FloatField', [], {'default': '365.25'})
        }
    }

    complete_apps = ['specification']
