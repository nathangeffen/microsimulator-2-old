from specification.models import State, TransitionRecord, Entry, \
    SpecifiedInitialValue, InitializationFunctionParameter
     
from django.contrib import admin
from django.utils.translation import ugettext as _

class SpecifiedInitialValueInline(admin.TabularInline):
    model = SpecifiedInitialValue
    extra = 0

class InitializationFunctionParameterInline(admin.TabularInline):
    model = InitializationFunctionParameter
    extra = 0
    sortable_field_name = 'position'

class EntryInline(admin.TabularInline):
    model = Entry
    extra = 0
    sortable_field_name = 'position'    

class TransitionRecordAdmin(admin.ModelAdmin):
    fieldsets = (
                 (None, 
                 {'fields' : ('state','description','position',)}),
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
    list_display = ('id', 'state', 'description', 'position','assign_function',
                    'new_value', 'value_time_period', 
                    'value_normalize_function', 'probability', 
                    'probability_time_period', 'probability_normalize_function',)
    list_editable = ('state', 'description', 'position', 'assign_function',                    'new_value', 'value_time_period', 
                    'value_normalize_function', 'probability', 
                    'probability_time_period', 'probability_normalize_function',)
    list_filter = ('state',)
    inlines = [EntryInline,]

class StateAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name','description',)
    list_editable = ('name','description',)
    inlines = [SpecifiedInitialValueInline, 
               InitializationFunctionParameterInline,]

admin.site.register(State, StateAdmin)
admin.site.register(TransitionRecord, TransitionRecordAdmin)
