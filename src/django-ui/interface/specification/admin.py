from specification.models import State, TransitionRecord, Entry, \
    SpecifiedInitialValue, InitializationFunctionParameter, Simulation
     
from django.contrib import admin
from django.utils.translation import ugettext as _


class SimulationAdmin(admin.ModelAdmin):
    raw_id_fields = ['owner',]
    filter_vertical = ['state',]

class TransitionRecordAdmin(admin.ModelAdmin):
    fieldsets = (
                 (None, 
                 {'fields' : ('description','position',)}),
                 (_('Specify how to change the state'), {'fields': 
                        ('assign_function','new_value', 
                         'value_time_period', 'value_normalize_function',) },
                 
                 ),
                 (_('Specify the probability with which the state will change'),
                 {'fields' : ('probability', 'probability_time_period',
                              'probability_normalize_function',) }
                 )
    )
    
    search_fields = ('state__name',)
    list_display = ('id', 'description', 'position','assign_function',
                    'new_value', 'value_time_period', 
                    'value_normalize_function', 'probability', 
                    'probability_time_period', 'probability_normalize_function',)
    list_editable = ('description', 'position', 'assign_function',                    'new_value', 'value_time_period', 
                    'value_normalize_function', 'probability', 
                    'probability_time_period', 'probability_normalize_function',)


class StateAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name','description',)
    list_editable = ('name','description',)
    
admin.site.register(Simulation, SimulationAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(TransitionRecord, TransitionRecordAdmin)