import pandas as pd
import numpy as np
from math import exp

# hardcoded data
-----
port_num = 6
disease_num = 3
port_code = {0: 'aqaba', 1: 'chittagong', 2: 'jakarta', 3: 'shenzhen', 4: 'tema', 5: 'valparaiso'}
disease_code = {0: 'LC', 1: 'CP', 2: 'ARI'}
pollutant_code = {0: 'fpm', 1: 'sox', 2: 'nox'}
beta = {'LC': 0.19292, 'CP': 0.17118, 'ARI': 0.0017}
cmin = {'LC': 5, 'CP': 5, 'ARI': 10}
base_em = {'fpm': 100, 'sox': 1000, 'nox': 1000}
ambient_conc_yr = [x for x in range(2001, 2011)]
# unit is tons per emission zone for all three

# import data from excel files, must use exact names and format 
-----
def get_data(filename):
	obj = {}
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "input", filename)
	matrix = get_data_from_file(DATA_PATH)
	for i in range(port_num):
		obj[port_code[i]] = matrix[i]
	return obj

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
				temp[disease_code[j]] = matrix[i][0]
			else:
				temp[disease_code[j]] = matrix[i]
			i = i+1
		obj[port_code[(i-1)/3]]= temp
	return obj
		

def get_data_from_file(filename):
	this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "input", filename)
	df = pd.read_excel(DATA_PATH)
	return df.as_matrix()

'''
-----
# calc population weighted conc from sarath's matrix and emission inputs
# real_em is from user input
def get_weighted_conc(base_conc, base_em, real_em):
	real_conc = np.zeros((5, 10))
	for pollutant in pollutant_code.values():
		real_conc[pollutant] += base_conc[pollutant] * (real_em[pollutant]/base_em[pollutant])
    return real_conc

# calc ymin
-----
def get_ymin(c0, cmin, beta, y0):
	ymin = {}
	for disease in disease_code.values():
		ymin[disease] = get_disease_ymin(c0, cmin[disease], beta[disease], y0[disease])

def get_disease_ymin(c0, cmin_specific, beta_specific, y0_specific):
	RR = (c0/cmin_specific)**beta_specific
	return y0_specific/RR

# calc delta RR
-----
def get_delta_RR(beta, cmin, real_conc, ambient_conc_cur_year):
	delta_RR = {}
	for disease in disease_code.values():
		if disease = 'ARI':
			delta_RR[disease] = get_delta_RR_ARI(beta[disease], cmin[disease], real_conc)
		else:
			delta_RR[disease] = get_delta_RR_others(beta[disease], cmin[disease], real_conc)
	return delta_RR

def get_delta_RR_ARI(beta_specific, cmin_specific, real_conc, ambient_conc_cur_year):
	return math.exp(beta_specific * (real_conc/0.92 + 2*(ambient_conc_cur_year - 
		real_conc) - 10)) - math.exp(beta_specific*(2*(ambient_conc_cur_year - real_conc) - 10))

def get_delta_RR_others(beta_specific, cmin_specific, real_conc, ambient_conc_cur_year):
	return ((cmin ** (-beta_specific)) * ((ambient_conc_cur_year ** beta_specific) - 
		((ambient_conc_cur_year - real_conc) ** beta_specific)) + (((cmin_specific + real_conc)/cmin_specific) ** beta_specific -
		1)) / 2
'''
# main
-----
ambient_conc = get_data('ambientConc.xlsx')
pop_struc = get_data('popStruc.xlsx')
pop = get_data('pop.xlsx')
y0 = get_nested_data('y0.xlsx')
ymin = get_ymin()

c0 = np.zeros((1, len(port_num)))
int i = 0
for value in ambient_conc.values):
	c0[i] = value[len(ambient_conc[0])-1]
	i = i + 1

#should be in specific port class...?
base_conc = {}
for pollutant in pollutant_code.values():
	this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "input/" + self.name, pollutant +'_base_conc.xlsx')
	base_conc[pollutant] = get_data(DATA_PATH)

weighted_conc = get_weighted_conc(base_conc, base_em, real_em)

