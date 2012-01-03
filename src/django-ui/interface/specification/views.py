from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms.models import modelformset_factory
from django.http import Http404
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from specification.models import Simulation, State, SpecifiedInitialValue, \
    InitializationFunctionParameter, TransitionRecord, Entry
from specification.forms import SimulationForm

def get_simulations(user_pk, simulation_pk=0):
    user = get_object_or_404(User, pk=user_pk)
    simulations =  Simulation.objects.filter( \
                            Q(owner=user) | Q(public_status="RW") |
                            Q(public_status='R') )
        
    if simulation_pk and simulations:  
        simulations =  simulations.filter(pk=simulation_pk)

    for s in simulations:
        s.editable = False
        if s.owner.pk == user_pk:
            s.editable = True
        elif s.public_status == 'RW':
            s.editable = True
                  
    return simulations    
    

class SimulationListView(ListView):
        
    context_object_name = "simulations"
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            simulations = get_simulations(self.request.user.pk)
            return simulations                
        else:
            raise Http404 

class DashboardView(DetailView):
    context_object_name = "simulation"
    model = Simulation

    def get_queryset(self):
        if self.request.user.is_authenticated:
            try:
                simulations = get_simulations(self.request.user.pk, 
                                          int(self.kwargs['pk']))
            except: 
                raise Http404
            
            if not simulations:
                raise Http404
            else:
                return simulations                
        else:
            raise Http404 

def dashboard_view(request, pk=None):

    if  pk == None:
        simulation = Simulation()
    else:
        simulation = Simulation.objects.get(pk = pk) 

    StateFormSet = inlineformset_factory(Simulation, State, can_delete=True,
                                         can_order=True)    
    
    if request.method == "POST":
        simulationform = SimulationForm(request.POST, instance=simulation)
        stateformset  = StateFormSet(request.POST, request.FILES, 
                                     instance=simulation)
        
        if simulationform.is_valid() and stateformset.is_valid():
            simulationform.save()
            stateformset.save()

            # Redirect to somewhere
            if '_save' in request.POST:
                return HttpResponseRedirect('/specification/dashboard')
            if '_addanother' in request.POST:
                return HttpResponseRedirect('/specification/dashboard/add/')
                
    else:
        simulationform      = SimulationForm(instance=simulation)
        stateformset    = StateFormSet(instance=simulation)

    return render_to_response('specification/dashboard.html', {
        'simulationform'    : simulationform,
        'stateformset'  : stateformset,
    }, context_instance=RequestContext(request))
