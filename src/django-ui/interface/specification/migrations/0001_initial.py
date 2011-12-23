# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'State'
        db.create_table('specification_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('initialization_function', self.gf('django.db.models.fields.CharField')(default='0', max_length=3)),
        ))
        db.send_create_signal('specification', ['State'])

        # Adding model 'SpecifiedInitialValue'
        db.create_table('specification_specifiedinitialvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['specification.State'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('probability', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('specification', ['SpecifiedInitialValue'])

        # Adding model 'InitializationFunctionParameter'
        db.create_table('specification_initializationfunctionparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['specification.State'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('specification', ['InitializationFunctionParameter'])

        # Adding model 'TransitionRecord'
        db.create_table('specification_transitionrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['specification.State'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('assign_function', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('new_value', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('value_time_period', self.gf('django.db.models.fields.FloatField')(default=365.25)),
            ('value_normalize_function', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('probability', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('probability_time_period', self.gf('django.db.models.fields.FloatField')(default=365.25)),
            ('probability_normalize_function', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('specification', ['TransitionRecord'])

        # Adding model 'Entry'
        db.create_table('specification_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transition_record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['specification.TransitionRecord'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['specification.State'])),
            ('match_function', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lower', self.gf('django.db.models.fields.FloatField')()),
            ('upper', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('specification', ['Entry'])


    def backwards(self, orm):
        
        # Deleting model 'State'
        db.delete_table('specification_state')

        # Deleting model 'SpecifiedInitialValue'
        db.delete_table('specification_specifiedinitialvalue')

        # Deleting model 'InitializationFunctionParameter'
        db.delete_table('specification_initializationfunctionparameter')

        # Deleting model 'TransitionRecord'
        db.delete_table('specification_transitionrecord')

        # Deleting model 'Entry'
        db.delete_table('specification_entry')


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
            'initialization_function': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '3'}),
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
