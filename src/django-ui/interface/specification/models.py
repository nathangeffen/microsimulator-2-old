from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

PUBLIC_STATUS = (
    ("P", _("This is a private simulation")),                 
    ("RW", _("Anyone can edit this simulation")),
    ("R", _("Anyone can view this simulation (but not edit it)")), 
)

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
    public_status = models.CharField(max_length=2, choices=PUBLIC_STATUS,
                                     default='P')
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Simulation')
        verbose_name_plural = _('Simulations')
        ordering = ['name',]    

class State(models.Model):
    simulation = models.ForeignKey(Simulation)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)
    initialization_function = models.CharField(max_length=3, 
                                               choices=INITIALIZATION_FUNCTIONS,
                                               default="0")
                
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ['name',]

class SpecifiedInitialValue(models.Model):
    state = models.ForeignKey(State)
    description = models.CharField(max_length=300, blank=True)
    value = models.FloatField()
    probability = models.FloatField()
    
    class Meta:
        verbose_name = _('Initial value for a state')
        verbose_name_plural = _('Initial values for states')
        ordering = ['state', 'value', 'probability',]

class InitializationFunctionParameter(models.Model):
    state = models.ForeignKey(State)
    description = models.CharField(max_length=300, blank=True)
    position = models.PositiveIntegerField(default=0)    
    value = models.FloatField()
    
    class Meta:
        verbose_name = _('Parameter for initialization function')
        verbose_name_plural = _('Parameters for initialization functions')
        ordering = ['state', 'position',]
    
class TransitionRecord(models.Model):
    state = models.ForeignKey(State)
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

    def __unicode__(self):
        return self.state.name + ':' + unicode(self.id) + ' - ' + \
            self.description
            
    class Meta:
        verbose_name = _('Transition Record')
        verbose_name_plural = _('Transition Records')
        ordering = ['state', 'position',]

class Entry(models.Model):
    transition_record = models.ForeignKey(TransitionRecord)
    description = models.CharField(max_length=200, blank=True)
    position = models.PositiveIntegerField(default=0)    
    state = models.ForeignKey(State)
    match_function = models.CharField(max_length=200, choices=MATCH_FUNCTIONS)
    lower = models.FloatField()
    upper = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.transition_record) + ':' + unicode(self.id) + ' - ' +\
            self.description

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = ('Entries')
        ordering = ['transition_record', 'position',]
        