from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

MATCH_FUNCTIONS = (
    ("EQ", _("== - Equals")),
    ("GTE_LTE", _(">= && <= - Greater than or equal to and less than or equal to")),
    ("GTE_LT", _(">= && < - Greater than or equal to and less than")),
    ("GT_LTE", _("> && <= - Greater than and less than or equal to")),
    ("GT_LT", _("> & < - Greater than and less than")),
)

ASSIGN_FUNCTIONS = (
    ('AS', _('Assign')),
    ('IN', _('Increment')),
)

NORMALIZE_FUNCTIONS = (
    ("0", _("No normalisation")),
    ("1", _("Linear normalisation")),
    ("2", _("Compound normalisation")),
)

INITIALIZATION_FUNCTIONS = (
    ("0", _('Manually enter values and their probabilities')),
    ("1", _('Undefined')),
)

class Simulation(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(User)
    state = models.ManyToManyField('State', blank=True, null=True)    

    def __unicode__(self):
        return self.name + ': ' + self.description
    
    class Meta:
        verbose_name = _('Simulation')
        verbose_name_plural = _('Simulations')
        ordering = ['name',]    

class State(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    initialization_function = models.CharField(max_length=3, 
                                               choices=INITIALIZATION_FUNCTIONS,
                                               default="0")
    specified_initial_value = models.ManyToManyField('SpecifiedInitialValue', 
                                                     blank=True, null=True)
    initialization_function_parameter = models.ManyToManyField(
                    'InitializationFunctionParameter', blank=True, null=True)
    transition_record = models.ManyToManyField('TransitionRecord', 
                                               blank=True, null=True)            
                
    def __unicode__(self):
        return self.name + ': ' + self.description
    
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ['name',]

class SpecifiedInitialValue(models.Model):
    description = models.CharField(max_length=300, blank=True)
    value = models.FloatField()
    probability = models.FloatField()
    
    def __unicode__(self):
        return unicode(self.pk) + ': ' + self.description
    
    class Meta:
        verbose_name = _('Initial value for a state')
        verbose_name_plural = _('Initial values for states')
        ordering = ['value', 'probability',]

class InitializationFunctionParameter(models.Model):
    description = models.CharField(max_length=300, blank=True)
    position = models.PositiveIntegerField(default=0)    
    value = models.FloatField()
    
    class Meta:
        verbose_name = _('Parameter for initialization function')
        verbose_name_plural = _('Parameters for initialization functions')
        ordering = ['position',]
    
class TransitionRecord(models.Model):
    description = models.CharField(max_length=200, blank=True)
    position = models.PositiveIntegerField(default=0)

    assign_function = models.CharField(max_length=2, choices=ASSIGN_FUNCTIONS)
    new_value = models.FloatField(default=1.0)
    value_time_period = models.FloatField(default=365.25)
    value_normalize_function = models.CharField(max_length=2,
                                                choices=NORMALIZE_FUNCTIONS)

    probability = models.FloatField(default=1.0)
    probability_time_period = models.FloatField(default=365.25)
    probability_normalize_function = models.CharField(max_length=2, 
                                                    choices=NORMALIZE_FUNCTIONS)

    entry = models.ManyToManyField('Entry', blank=True, null=True)
    def __unicode__(self):
        return self.description
            
    class Meta:
        verbose_name = _('State Transition')
        verbose_name_plural = _('State Transition')
        ordering = ['position',]

class Entry(models.Model):
    description = models.CharField(max_length=200, blank=True)
    position = models.PositiveIntegerField(default=0)    
    state = models.ForeignKey(State)
    match_function = models.CharField(max_length=200, choices=MATCH_FUNCTIONS)
    lower = models.FloatField()
    upper = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return self.name + ': ' + self.description

    class Meta:
        verbose_name = _('Condition')
        verbose_name_plural = ('Conditions')
        ordering = [ 'position',]
        