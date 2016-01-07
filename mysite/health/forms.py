from django import forms
from calc import port_code, ambient_conc_yr, age_group

class InputForm(forms.Form):
	port = forms.ChoiceField(choices = zip(port_code.values(), port_code.values()), label = 'Port')
	yearChoice = zip(ambient_conc_yr, ambient_conc_yr)
	yearChoice.extend([(2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014)])
	year = forms.ChoiceField(choices = yearChoice, label = 'Modeled year')
	total_pm10 = forms.FloatField(label = 'Total annual PM10 emissions (ton)', min_value = 0.0001)
	direction = forms.ChoiceField(choices = [('Blank', ''), ('North', 'North'), ('East', 'East'), ('West', 'West'), ('South', 'South')], label = 'Direction (only applies to general ports)', required = False)
	
	'''
	class EmForm(forms.Form):
	    em_port = forms.FloatField(label = 'Annual emissions - Port')
	    em_on = forms.FloatField(label = 'Annual emissions - Onshore')
	    em_off = forms.FloatField(label = 'Annual emissions - Offshore')
	EmFormSet = formset_factory(EmForm, extra = 2)
	'''
	em_fpm_port = forms.FloatField(label = 'Annual primary PM2.5 emissions - Port')
	em_fpm_on = forms.FloatField(label = 'Annual primary PM2.5 emissions - Onshore')
	em_fpm_off = forms.FloatField(label = 'Annual primary PM2.5 emissions - Offshore')
	em_sox_port = forms.FloatField(label = 'Annual SOx emissions - Port')
	em_sox_on = forms.FloatField(label = 'Annual SOx emissions - Onshore')
	em_sox_off = forms.FloatField(label = 'Annual SOx emissions - Offshore')
	em_nox_port = forms.FloatField(label = 'Annual NOx emissions - Port')
	em_nox_on = forms.FloatField(label = 'Annual NOx emissions - Onshore')
	em_nox_off = forms.FloatField(label = 'Annual NOx emissions - Offshore')
	
'''
	class Meta:
		fieldsets = [
			('General', {
				'fields':('port', 'year')
				}),
			('Primary PM emissions', {
				'fields':('em_fpm_port', 'em_fpm_on', 'em_fpm_off')
				}),
			('Primary SOx emissions', {
				'fields':('em_sox_port', 'em_sox_on', 'em_sox_off')
				}),
			('Primary NOx emissions', {
				'fields':('em_nox_port', 'em_nox_on', 'em_nox_off')
				})
			]
'''
class OptionalForm(forms.Form):
	pop = forms.FloatField(label = 'Population', required = False)
	conc = forms.FloatField(label = 'Ambient concentration of PM2.5 (micro-grams/m3)', required = False)
	# TODO set default
	#y_LC_0_4 = forms.FloatField(label = 'Incidence rate for lung cancer 0-4', max_value = 100000, required = False)
	y_LC_30_34 = forms.FloatField(label = 'Incidence rate for lung cancer 30-34', max_value = 100000, required = False)
	y_LC_35_39 = forms.FloatField(label = 'Incidence rate for lung cancer 35-39', max_value = 100000, required = False)
	y_LC_40_44 = forms.FloatField(label = 'Incidence rate for lung cancer 40-44', max_value = 100000, required = False)
	y_LC_45_49 = forms.FloatField(label = 'Incidence rate for lung cancer 45-49', max_value = 100000, required = False)
	y_LC_50_54 = forms.FloatField(label = 'Incidence rate for lung cancer 50-54', max_value = 100000, required = False)
	y_LC_55_59 = forms.FloatField(label = 'Incidence rate for lung cancer 55-59', max_value = 100000, required = False)
	y_LC_60_64 = forms.FloatField(label = 'Incidence rate for lung cancer 60-64', max_value = 100000, required = False)
	y_LC_65_69 = forms.FloatField(label = 'Incidence rate for lung cancer 65-69', max_value = 100000, required = False)
	y_LC_70_74 = forms.FloatField(label = 'Incidence rate for lung cancer 70-74', max_value = 100000, required = False)
	y_LC_75_79 = forms.FloatField(label = 'Incidence rate for lung cancer 75-79', max_value = 100000, required = False)
	y_LC_80 = forms.FloatField(label = 'Incidence rate for lung cancer 80+', max_value = 100000, required = False)
	#y_CP_0_4 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 0-4', max_value = 100000, required = False)
	y_CP_30_34 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 30-34', max_value = 100000, required = False)
	y_CP_35_39 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 35-39', max_value = 100000, required = False)
	y_CP_40_44 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 40-44', max_value = 100000, required = False)
	y_CP_45_49 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 45-49', max_value = 100000, required = False)
	y_CP_50_54 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 50-54', max_value = 100000, required = False)
	y_CP_55_59 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 55-59', max_value = 100000, required = False)
	y_CP_60_64 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 60-64', max_value = 100000, required = False)
	y_CP_65_69 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 65-69', max_value = 100000, required = False)
	y_CP_70_74 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 70-74', max_value = 100000, required = False)
	y_CP_75_79 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 75-79', max_value = 100000, required = False)
	y_CP_80 = forms.FloatField(label = 'Incidence rate for cardiopulmonary diseases 80+', max_value = 100000, required = False)
	y_ARI = forms.FloatField(label = 'Incidence rate for acute respiratory infections 0-4', max_value = 100000, required = False)