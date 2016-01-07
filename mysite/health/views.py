from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import numpy as np
import calc

from .forms import InputForm, OptionalForm

def index(request):
	#return HttpResponse(reverse('health: index'))
	return render(request, 'health/index.html')

#port, year, em1, em2, em3
def input(request):
	#blank form
	# temporary random initial values for testing
	temp_initial = {'port': 'Shenzhen', 'year': 2010, 'total_pm10': 350, 'em_fpm_port': 100, 'em_fpm_on': 100, 'em_fpm_off': 100, 'em_sox_port': 100, 'em_sox_on': 100, 'em_sox_off': 100, \
	'em_nox_port': 100, 'em_nox_on': 100, 'em_nox_off': 100}
	#eturn HttpResponse(reverse('health: input', {'form': InputForm()}))
	return render(request, 'health/input.html', {'form': InputForm(temp_initial)})

# pass pop, conc, y1, y2, y3? to optionalinput page
# process input with function in calc
def optionalinput(request):
	form = InputForm(request.POST)
	if form.is_valid():
		em = {}
		em['fpm'] = np.array([form.cleaned_data['em_fpm_port'], form.cleaned_data['em_fpm_on'], form.cleaned_data['em_fpm_off']])
		em['SOx'] = np.array([form.cleaned_data['em_sox_port'], form.cleaned_data['em_sox_on'], form.cleaned_data['em_sox_off']])
		em['NOx'] = np.array([form.cleaned_data['em_nox_port'], form.cleaned_data['em_nox_on'], form.cleaned_data['em_nox_off']])
		ratio = sum(em['fpm'])*1.0/form.cleaned_data['total_pm10']
		result = calc.process_input(form.cleaned_data['port'], form.cleaned_data['year'], em, form.cleaned_data['direction'], ratio)
    	#get underlying data pop, conc, y1, y2, y3
		context = {'pop': result['pop'], 'conc': result['conc']}
		# mimic user input for testing purpose
		#context = {'pop': result['pop'], 'conc': result['conc'], 'y_LC_30_34': 2.2, 'y_LC_35_39': 4.55, 'y_LC_40_44': 10.1, 'y_LC_45_49': 20.45,\
		#'y_LC_50_54': 40.9, 'y_LC_55_59': 72.45, 'y_LC_60_64': 117.05, 'y_LC_65_69': 173.5, 'y_LC_70_74': 249.95, 'y_LC_75_79': 326.7, 'y_LC_80': 431.6, 'y_CP_30_34': 52.45, \
		#'y_CP_35_39': 86.85, 'y_CP_40_44': 157, 'y_CP_45_49': 274.45, 'y_CP_50_54': 493.25, 'y_CP_55_59': 835.95, 'y_CP_60_64': 1511.75, 'y_CP_65_69': 2688, 'y_CP_70_74': 4786.9, 'y_CP_75_79': 8224.6,\
		#'y_CP_80': 21836.05, 'y_ARI': 2272.8}
		#return HttpResponse(reverse('health: optionalinput', kwargs = context))
		return render(request,'health/optionalinput.html', {'form': OptionalForm(context)})
	#form not valid, render a blank form. need some kind of warning..?
	#return HttpResponse(reverse('health: input'), {'form': InputForm()})
	return render(request, 'health/input.html', {'form': InputForm()})	

def result(request):
	# TODO if general port and either one of the op input is not supplied
	# warning, can't proceed
	# calc impact
	# TODO need to see if y in inputed
	# pass value to calc.process_op_input
	indicator = 0
	form = OptionalForm(request.POST)
	# TODO only if user inputs all data will we use his y
	if form.is_valid():
		if ((form.cleaned_data['y_LC_30_34'] is not None) and (form.cleaned_data['y_LC_35_39'] is not None) and (form.cleaned_data['y_LC_40_44'] is not None) and \
		(form.cleaned_data['y_LC_45_49'] is not None) and (form.cleaned_data['y_LC_50_54'] is not None) and (form.cleaned_data['y_LC_55_59'] is not None) and (form.cleaned_data['y_LC_60_64'] is not None) and \
		(form.cleaned_data['y_LC_65_69'] is not None) and (form.cleaned_data['y_LC_70_74'] is not None) and (form.cleaned_data['y_LC_75_79'] is not None) and (form.cleaned_data['y_LC_80'] is not None) and \
		(form.cleaned_data['y_CP_30_34'] is not None) and (form.cleaned_data['y_CP_35_39'] is not None) and (form.cleaned_data['y_CP_40_44'] is not None) and \
		(form.cleaned_data['y_CP_45_49'] is not None) and (form.cleaned_data['y_CP_50_54'] is not None) and (form.cleaned_data['y_CP_55_59'] is not None) and (form.cleaned_data['y_CP_60_64'] is not None) and \
		(form.cleaned_data['y_CP_65_69'] is not None) and (form.cleaned_data['y_CP_70_74'] is not None) and (form.cleaned_data['y_CP_75_79'] is not None) and (form.cleaned_data['y_CP_80'] is not None) and \
		(form.cleaned_data['y_ARI'] is not None)):
			indicator = 1
			y = {}
			y['LC'] = np.array([0, form.cleaned_data['y_LC_30_34'], form.cleaned_data['y_LC_35_39'], form.cleaned_data['y_LC_40_44'], form.cleaned_data['y_LC_45_49'], \
			form.cleaned_data['y_LC_50_54'], form.cleaned_data['y_CP_55_59'], form.cleaned_data['y_LC_60_64'], form.cleaned_data['y_LC_65_69'], form.cleaned_data['y_LC_70_74'], form.cleaned_data['y_LC_75_79'], form.cleaned_data['y_LC_80']])
			y['CP'] = np.array([0, form.cleaned_data['y_CP_30_34'], form.cleaned_data['y_CP_35_39'], form.cleaned_data['y_CP_40_44'], form.cleaned_data['y_CP_45_49'], \
			form.cleaned_data['y_CP_50_54'], form.cleaned_data['y_CP_55_59'], form.cleaned_data['y_CP_60_64'], form.cleaned_data['y_CP_65_69'], form.cleaned_data['y_CP_70_74'], form.cleaned_data['y_LC_75_79'], form.cleaned_data['y_CP_80']])
			y['ARI'] = np.array([form.cleaned_data['y_ARI']])
	if form.is_valid():
		if indicator == 0:
			results = calc.process_optional_input(pop = form.cleaned_data['pop'], conc = form.cleaned_data['conc'])
		else:
			results = calc.process_optional_input(pop = form.cleaned_data['pop'], conc = form.cleaned_data['conc'], port_y = y)
	# pass to template. try age table first
	context = {'indicator': results['indicator'], 'age': results['age'], 'time': results['time'], 'zone': results['zone'], 'yll': results['yll'], 'zone_num': range(1, results['zone']['ARI'].size + 1)}
	#return HttpResponse(reverse('health:result', kwargs = context))
	return render(request, 'health/result.html', context)
