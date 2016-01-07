import pandas as pd
import os.path
import numpy as np
from port import Port

port_num = 7
disease_num = 3
port_code = {0: 'Aqaba', 1: 'Chittagong', 2: 'Jakarta', 3: 'Shenzhen', 4: 'Tema', 5: 'Valparaiso', 6: 'General'}
disease_code = {0: 'LC', 1: 'CP', 2: 'ARI'}
port_reverse_code = {'Aqaba': 0, 'Chittagong': 1, 'Jakarta': 2, 'Shenzhen': 3, 'Tema': 4, 'Valparaiso': 5, 'General': 6}
pollutant_code = {0: 'fpm', 1: 'SOx', 2: 'NOx'}
zone_division = {'Aqaba': [2, 2, 3], 'Chittagong': [5, 2, 3], 'Jakarta': [5, 2, 3], 'Shenzhen': [5, 2, 3], 'Tema': [1, 2, 3], 'Valparaiso': [1, 2, 3], 'General': [1, 1, 2]}
ambient_conc_yr = [x for x in range(2001, 2011)]
age_group = 12
time_interval = 5

# get port data from file
# @param excel filename e.g. conc.xlsx
# @return dict, keys are port names, values are arrays
def get_data(filename):
	obj = {}
	this_dir, this_filename = os.path.split(__file__)
	DATA_PATH = os.path.join(this_dir, "input", filename)
	matrix = get_data_from_file(DATA_PATH)
	for i in range(port_num):
		obj[port_code[i]] = matrix[i]
	return obj

# get port data from file, used for 2-level hierarchy such as y
# @param excel filename e.g. conc.xlsx
# @return 2-level dict, keys are port names and disease names, values are arrays
def get_nested_data(filename):
	obj = {}
	this_dir, this_filename = os.path.split(__file__)
	DATA_PATH = os.path.join(this_dir, "input", filename)
	matrix = get_data_from_file(DATA_PATH)
	i = 0
	while i < disease_num*port_num:
		temp = {}
		for j in range(disease_num):
			if j == 2:
				temp[disease_code[j]] = np.array([matrix[i][0]])
			else:
				temp[disease_code[j]] = matrix[i]
			i = i+1
		obj[port_code[(i-1)/3]]= temp
	return obj
		
# get port data matrix from file
# @param excel filename e.g. conc.xlsx
# @return data matrix (ndarray)
def get_data_from_file(filename):
	this_dir, this_filename = os.path.split(__file__)
	DATA_PATH = os.path.join(this_dir, "input", filename)
	df = pd.read_excel(DATA_PATH)
	return df.as_matrix()

# TODO general port is included, but value is 0 if does not have an initial value. Substitute with user input later
# only has pop_struc and life_exp for general as real input here
ambient_conc = get_data('ambientConc.xlsx')
pop_struc = get_data('popStruc.xlsx')
pop = get_data('pop.xlsx')
# 2010 y0 data
y0 = get_nested_data('y0.xlsx')
life_exp = get_data_from_file('lifeExp.xlsx')[0]

# latest ambient conc data, 2010
c0 = np.zeros(port_num)
i = 0
for value in port_code.values():
	c0[i] = ambient_conc[value][len(ambient_conc['Aqaba'])-1] 
	i = i + 1

# two functions here that can be called by view
# process_input(first sets of inputs), return underlying data for second sets
# prcocess_optional_input(second sets of inputs), return impact
# em and y are passed in as list/array
# use global var to access outer scope

port_name = port_ambient_conc = port_y0 = port_c0 = port_pop_struc = \
port_pop = port_direction = port_real_em = base_conc = ratio = None

# first set
# from user, get port name, year, em(dict with pollutants as key, each value is an array with three
# values for port, on shore and offshore); required input
# save/get name, c0(name), y0(name), pop_struc(name), pop(name, year), ambient conc(name, year), real_em, base_conc
# return pop, ambient conc
def process_input(name, year, em, direction, r):
	global port_name, port_c0, port_y0, port_pop_struc, port_pop, port_ambient_conc, port_real_em, port_direction, base_conc, ratio
	ratio = r
	port_real_em =  {}
	base_conc = {}
	if (name == 'General') and (direction in ('North', 'East', 'West', 'South')):
		port_direction = direction
	port_name = name
	port_c0 = c0[port_reverse_code[name]]
	port_y0 = y0[name]
	port_pop_struc = pop_struc[name]
	# our ambient conc data only from 2001- 2010, user can input their own on next page
	if year > 2010: 
		year = 2010
	port_pop = pop[name][int(year) - ambient_conc_yr[0]]
	port_ambient_conc = ambient_conc[name][int(year) - ambient_conc_yr[0]]
	# calc port real em matrix [5*num zone]
	for pollutant in pollutant_code.values():
		annual = np.repeat(em[pollutant]/zone_division[name], zone_division[name])
		#name_t = port_name
		#annual_t = annual
		#print name_t.key
		seasonal = annual/4.0
		em_matrix = np.empty([time_interval, len(annual)])
		for i in range(time_interval):
			if i == time_interval - 1:
				em_matrix[i] = annual
			else:
				em_matrix[i] = seasonal
		port_real_em[pollutant] = em_matrix
	# get base_conc from excel
	for pollutant in pollutant_code.values():
		this_dir, this_filename = os.path.split(__file__)
		if port_direction is None:
			DATA_PATH = os.path.join(this_dir, 'input/' + port_name + '_' + pollutant + '_base_conc.xlsx')
		else:
			DATA_PATH = os.path.join(this_dir, 'input/' + port_name + '_' + direction + '_' + pollutant + '_base_conc.xlsx')
		base_conc[pollutant] = get_data_from_file(DATA_PATH)
	#em_t = port_real_em
	#c0_t = port_c0
	#y0_t = port_y0
	#pop_struct_t = port_pop_struc
	#pop_t = port_pop
	#ambient_t = port_ambient_conc
	#base_t = base_conc
	#print em_t.key
	return {'pop': port_pop, 'conc': port_ambient_conc}

# add the 'Total' row below each table
def add_total(dic, length = age_group + 1):
	dic['Total'] = np.zeros(length)
	for i in range(length):
		for key in dic.keys():
			if key!= 'Total':
				dic['Total'][i] = dic['Total'][i] + float(dic[key][i])

# fill pop, ambient conc
# from user, get pop, cur ambient conc, y123
# if the user use our data, just click continue(specify what ymin we use)
# If general port, have to input all three, else can't process
# If for all other ports, user can input any one or several of them
# But for years > 2010, underlying pop and conc will be data in 2010
# Rely on user check completeness of data, or check as below
# return impact
# TODO
# if there is one ymin blank, we will not use your data
# Use whatever is submitted. check each ymin. if any is still blank, use our own ymin approach; otherwise, use 
# the other approach. This check should be done in view. call diff funcs

# TODO: check if methods work with ARI

# use our own ymin if y is not supplied, else use the user's y
# y is input by the user, view.py format it as y0 and pass it to calc
# for general port, all three need to be supplied by the user
def process_optional_input(pop = None, conc = None, port_y = None):
	global port_name, port_ambient_conc, port_y0, port_c0, port_pop_struc, port_pop, base_conc, port_real_em, ratio
	if pop is not None:
		port_pop = pop
	if conc is not None:
		port_ambient_conc = conc
	# call Port class to do calc, if use inputs his own y, then pass y to port class instead of y0 to calc ymin
	if port_y is None:
		port = Port(port_name, port_ambient_conc, port_y0, port_c0, port_pop_struc, port_pop, base_conc, port_real_em, ratio)
		indicator = 0
	else:
		port = Port(port_name, port_ambient_conc, port_y, port_c0, port_pop_struc, port_pop, base_conc, port_real_em, ratio)
		indicator = 1
	name_t = port_name
	ambient_t = port_ambient_conc
	y0_t = port_y0
	c0_t = port_c0
	pop_struc_t = port_pop_struc
	pop_t = port_pop
	base_t = base_conc
	em_t = port_real_em
	#print impact.key
	impact = port.get_impact(indicator)
	
	# process/aggregate the impact in some way
	result_disease_age = {}
	result_disease_time = {}
	result_disease_zone = {}
	result_disease_age_yll = {}
	for key in impact.keys():
		if key != 'ARI':
			impact_all_age = np.empty(age_group)
			for i in range(age_group):
				impact_all_age[i] = sum(impact[key][i][4, :])
			result_disease_age[key] = np.around(impact_all_age, 2)
		else:
			result_disease_age[key] = np.around(np.array([sum(impact[key][0][4, :])]),2)
	# does not matter if ARI or not
	for key in impact.keys():
		impact_sum_age = sum(impact[key])
		result_disease_zone[key] = np.around(impact_sum_age[4, :],2)
		#print impact_sum_age.key
		temp = np.empty(time_interval)
		for i in range(time_interval):
			temp[i] = sum(impact_sum_age[i, :])
		result_disease_time[key] = np.around(temp, 2)
		#sum_age_t = impact_sum_age
		#print sum_age_t.key
	for key in impact.keys():
		if key != "ARI":
			result_disease_age_yll[key] = np.around(np.array(life_exp) * result_disease_age[key], 2)
			#-- add total col for yll except its ARI
			result_disease_age_yll[key] = np.append(result_disease_age_yll[key], sum(result_disease_age_yll[key]))
			#-- add total col for age except its ARI
			result_disease_age[key] = np.append(result_disease_age[key], sum(result_disease_age[key]))
		else:
			result_disease_age_yll[key] = np.around(np.array(life_exp[0]) * result_disease_age[key], 2)
	#exp_t = life_exp
	#age_t = result_disease_age_yll["ARI"]
	#print exp_t.key
	#--- Add N/A and total in cols for ARI
	result_disease_age['ARI'] = np.append(result_disease_age['ARI'], np.array([ 0 for i in range(age_group - 1)]))
	result_disease_age['ARI'] = np.append(result_disease_age['ARI'], result_disease_age['ARI'][0])
	result_disease_age_yll['ARI'] = np.append(result_disease_age_yll['ARI'], np.array([ 0 for i in range(age_group - 1)]))
	result_disease_age_yll['ARI'] = np.append(result_disease_age_yll['ARI'], result_disease_age_yll['ARI'][0])
	#-- add total row below each table
	#result_disease_age['Total'] = np.zeros(age_group + 1)
	#result_disease_time['Total'] = np.zeros(age_group + 1)
	#result_disease_age_yll['Total'] = np.zeros(age_group + 1)
	#result_disease_zone['Total'] = np.zeros(age_group + 1)
	#for i in range(age_group + 1):
	#	for key in result_disease_age.keys():
	#		if key!= 'Total' and result_disease_age[key][i] != 'N/A':
	#			result_disease_age['Total'][i] = result_disease_age['Total'][i] + float(result_disease_age[key][i])
	#-- get rid of 0-4 value for age time before adding up cols
	#result_disease_age['LC'][0] = 0
	#result_disease_age['CP'][0] = 0
	#result_disease_age_yll['LC'][0] = 0
	#result_disease_age_yll['CP'][0] = 0
	#-- add total row below table
	add_total(result_disease_age)
	add_total(result_disease_time, time_interval)
	add_total(result_disease_age_yll)
	add_total(result_disease_zone, len(result_disease_zone['ARI']))
	return {'age': result_disease_age, 'time': result_disease_time, 'zone': result_disease_zone, 'yll': result_disease_age_yll, 'indicator': indicator}

	
