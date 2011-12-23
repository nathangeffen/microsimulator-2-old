# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'InitializationFunctionParameter.description'
        db.add_column('specification_initializationfunctionparameter', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True), keep_default=False)

        # Adding field 'InitializationFunctionParameter.position'
        db.add_column('specification_initializationfunctionparameter', 'position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'SpecifiedInitialValue.description'
        db.add_column('specification_specifiedinitialvalue', 'description', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True), keep_default=False)

        # Adding field 'Entry.position'
        db.add_column('specification_entry', 'position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)

        # Adding field 'TransitionRecord.position'
        db.add_column('specification_transitionrecord', 'position', self.gf('django.db.models.fields.PositiveIntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'InitializationFunctionParameter.description'
        db.delete_column('specification_initializationfunctionparameter', 'description')

        # Deleting field 'InitializationFunctionParameter.position'
        db.delete_column('specification_initializationfunctionparameter', 'position')

        # Deleting field 'SpecifiedInitialValue.description'
        db.delete_column('specification_specifiedinitialvalue', 'description')

        # Deleting field 'Entry.position'
        db.delete_column('specification_entry', 'position')

        # Deleting field 'TransitionRecord.position'
        db.delete_column('specification_transitionrecord', 'position')


    models = {
        'specification.entry': {
            'Meta': {'ordering': "['transition_record', 'position']", 'object_name': 'Entry'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lower': ('django.db.models.fields.FloatField', [], {}),
            'match_function': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'transition_record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.TransitionRecord']"}),
            'upper': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'specification.initializationfunctionparameter': {
            'Meta': {'ordering': "['state', 'position']", 'object_name': 'InitializationFunctionParameter'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'specification.specifiedinitialvalue': {
            'Meta': {'ordering': "['state', 'value', 'probability']", 'object_name': 'SpecifiedInitialValue'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'probability': ('django.db.models.fields.FloatField', [], {}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'specification.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initialization_function': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'specification.transitionrecord': {
            'Meta': {'ordering': "['state', 'position']", 'object_name': 'TransitionRecord'},
            'assign_function': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'probability': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'probability_normalize_function': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'probability_time_period': ('django.db.models.fields.FloatField', [], {'default': '365.25'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.State']"}),
            'value_normalize_function': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'value_time_period': ('django.db.models.fields.FloatField', [], {'default': '365.25'})
        }
    }

    complete_apps = ['specification']
