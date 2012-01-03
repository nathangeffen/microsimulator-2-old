# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Simulation'
        db.create_table('specification_simulation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('public_status', self.gf('django.db.models.fields.CharField')(default='P', max_length=2)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('specification', ['Simulation'])

        # Adding field 'State.simulation'
        db.add_column('specification_state', 'simulation', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['specification.Simulation']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Simulation'
        db.delete_table('specification_simulation')

        # Deleting field 'State.simulation'
        db.delete_column('specification_state', 'simulation_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'specification.simulation': {
            'Meta': {'ordering': "['name']", 'object_name': 'Simulation'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'public_status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '2'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'simulation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['specification.Simulation']"})
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
