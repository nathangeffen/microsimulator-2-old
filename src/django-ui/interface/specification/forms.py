from django.forms import ModelForm
from specification.models import Simulation, State, SpecifiedInitialValue, \
    InitializationFunctionParameter, TransitionRecord, Entry

class SimulationForm(ModelForm):
    
    class Meta:
        model = Simulation

class InitializationFunctionParameterForm(ModelForm):
    
    class Meta:
        model = InitializationFunctionParameter

class TransitionRecordForm(ModelForm):
    
    class Meta:
        model = TransitionRecord

class EntryForm(ModelForm):
    
    class Meta:
        model = Entry
