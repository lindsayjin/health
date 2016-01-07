# Port class that has port characteristics and is used to calc data for a specific port

import numpy as np
import math

class Port:
	disease_code = {0: 'LC', 1: 'CP', 2: 'ARI'}
	pollutant_code = {0: 'fpm', 1: 'SOx', 2: 'NOx'}
	beta = {'LC': 0.19292, 'CP': 0.17118, 'ARI': 0.0017}
	cmin = {'LC': 5, 'CP': 5, 'ARI': 10}
	base_em = {'fpm': np.array([25, 25, 25, 25, 100]), 'SOx': np.array([250, 250, 250, 250, 1000]), 'NOx': np.array([250, 250, 250, 250, 1000])}
	disease_num = 3
	age_group = 12
	time_interval_num = 5


	def __init__(self, name, ambient_conc, y0, c0, pop_struc, pop, base_conc, real_em, ratio):
		self.name = name
		self.ambient_conc = ambient_conc
		self.y0 = y0
		self.c0 = c0
		self.pop_struc = pop_struc
		self.pop = pop
		self.base_conc = base_conc
		# time interval * num of zones
		self.real_em = real_em
		self.ratio = ratio
		# atttibutes that need to be calculated inside class
		self.real_conc = np.zeros((self.time_interval_num, real_em['fpm'].shape[1]))
		self.risk_pop = None
		self.ymin = {}
		self.delta_RR = {}
		self.base_em_zone = {}
		#---testing 92% assumption
		self.real_conc_pollutant = {}


	# calc population weighted conc from sarath's matrix and emission inputs
	# real_em is from user input and process, should be in same format as base_conc
	def get_weighted_conc(self):
		zone_num = self.real_em['fpm'].shape[1]
		for pollutant in self.pollutant_code.values():
			self.base_em_zone[pollutant] = self.base_em[pollutant]*1.0/zone_num
			#base_t = self.base_conc[pollutant]
			#base_em_zone_t = self.base_em_zone[pollutant]
			#real_em_t = self.real_em[pollutant]
			#print base_t.key
			# conc here is the total PM conc of three pollutants
			self.real_conc += self.base_conc[pollutant] * (1.0 * (self.real_em[pollutant])/self.base_em_zone[pollutant][:, None])
			#---testing 92% assumption
			self.real_conc_pollutant[pollutant] = self.base_conc[pollutant] * (1.0 * (self.real_em[pollutant])/self.base_em_zone[pollutant][:, None])
		#real_t = self.real_conc
		#base_t = self.base_conc
		#base_em_t = self.base_em
		#base_em_zone_t = self.base_em_zone
		#real_em_t = self.real_em
		#print real_t.key

	# @return an array of 12 age groups, each value is num of people in that age group
	def get_risk_pop(self):
		self.risk_pop = np.array(self.pop * self.pop_struc)
		risk_pop_t = self.risk_pop
		#print risk_pop_t.key

	# helper of the method below
	def get_disease_ymin(self, disease):
		if disease == 'ARI':
			RR = math.exp(self.beta[disease]*(self.c0 - self.cmin[disease]))
		else:
			RR = (1.0*self.c0/self.cmin[disease])**self.beta[disease]
		beta_t = self.beta[disease]
		c0_t = self.c0
		cmin_t = self.cmin[disease]
		#print RR.key
		return self.y0[disease]*1.0/RR

	# @return a dict of diseases, values are arrays of len(age groups)
	def get_ymin(self):
		for disease in self.disease_code.values():
			self.ymin[disease] = np.array(self.get_disease_ymin(disease))

    # two helpers of the method above
	def get_delta_RR_ARI(self, disease):
		#---testing 92% assumption
		fpm = sum(self.real_conc_pollutant['fpm'][4,:])
		nox = sum(self.real_conc_pollutant['NOx'][4,:])
		sox = sum(self.real_conc_pollutant['SOx'][4,:])
		#ratio is primary pm/total pm10 emissions/conc; final ratio includes secondary pm
		final_ratio = 1.0*(fpm + nox + sox)/(1.0*fpm/self.ratio + nox + sox)
		# ARI based on pm10, fpm is 92% of pm10
		#print 
		#return np.exp(self.beta[disease] * (self.real_conc/0.92 + 2 * (self.ambient_conc - \
		#self.real_conc) - self.cmin[disease])) - np.exp(self.beta[disease]*(2*(self.ambient_conc - self.real_conc) - self.cmin[disease]))
		return np.exp(self.beta[disease] * (self.real_conc/final_ratio + 2 * (self.ambient_conc - \
		self.real_conc) - self.cmin[disease])) - np.exp(self.beta[disease]*(2*(self.ambient_conc - self.real_conc) - self.cmin[disease]))
	def get_delta_RR_others(self, disease):
		return ((self.cmin[disease] ** (-self.beta[disease])) * ((self.ambient_conc ** self.beta[disease]) - \
		((self.ambient_conc - self.real_conc) ** self.beta[disease])) + ((1.0*(self.cmin[disease] + self.real_conc)/(1.0*self.cmin[disease])) ** self.beta[disease] - \
		1)) / 2.0


    # get RR for the current calc
	def get_delta_RR(self):
		for disease in self.disease_code.values():
			if disease == 'ARI':
				self.delta_RR[disease] = np.array(self.get_delta_RR_ARI(disease))
			else:
				self.delta_RR[disease] = np.array(self.get_delta_RR_others(disease))


	def get_disease_impact(self, disease):
		if disease != 'ARI':
			temp = self.risk_pop * self.ymin[disease]/100000.0
		else:
			#a = self.risk_pop[0]
			#b = self.ymin[disease]
			temp = self.risk_pop[0] * self.ymin[disease]/100000.0
		#risk_pop_t = self.risk_pop
		#ymin_t = self.ymin
		#print risk_pop_t.key
		count = 0
		#risk_t = self.risk_pop
		#ymin_t = self.ymin
		#print temp.key
		age_impact = np.empty([self.age_group, self.time_interval_num, self.delta_RR['LC'].shape[1]])
		for x in temp:
			age_impact[count, :, :] = x * self.delta_RR[disease]
			count += 1
		#a = age_impact
		#print b
		return age_impact

	def get_RR(self, conc, disease):
		if disease != 'ARI':
			return ((1.0*conc/self.cmin[disease])**self.beta[disease])
		else:
			#a = (1 - 1.0/(np.exp(self.beta[disease]*(conc - self.cmin[disease]))))
			#print a.key
			return (np.exp(self.beta[disease]*(conc - self.cmin[disease])))
	#get the annual avg total pm2.5 conc from real_conc
	#def get_port_conc(self):
	#	return sum(self.real_conc[4, :])

	def get_disease_impact_alternative(self, disease):
		# when use this method, y0 is user's y when passed in
		if disease != 'ARI':
			# y0 is in the unit of deaths per 100,000 people in that age group and that year
			temp = self.risk_pop * self.y0[disease]/100000.0
		else:
			temp = self.risk_pop[0] * self.y0[disease]/100000.0
		count = 0
		#port_conc = self.get_port_conc()
		#temp_risk = self.risk_pop
		#temp_t = temp
		#print temp.key
		#age_impact = np.empty(self.age_group)
		age_impact = np.empty([self.age_group, self.time_interval_num, self.delta_RR['LC'].shape[1]])
		for x in temp:
			#if disease != 'ARI':
				#age_impact[count, :, :] = x * (1 - 1.0/((1.0*self.ambient_conc/self.cmin[disease])**self.beta[disease]))
			if disease == 'LC':
				a = self.get_RR(conc = (self.ambient_conc - self.real_conc), disease = disease)
				#b = 1.0/self.get_RR(conc = self.ambient_conc, disease = disease)
				#print a,key
			age_impact[count, :, :] = x * (1.0/self.get_RR(conc = (self.ambient_conc - self.real_conc), disease = disease)) - x * (1.0/self.get_RR(conc = self.ambient_conc, disease = disease))
			#else:
				#age_impact[count, :, :] = x * (1 - 1.0/(math.exp(self.beta[disease]*(self.ambient_conc - self.cmin[disease]))))
				#age_impact[count, :, :] = x * (1.0/self.get_RR_ARI(ambient_conc - port_conc) - 1.0/self.get_RR_ARI(ambient_conc))
			count += 1
		return age_impact

	#intended for external use
	#indicator = 0 when use ymin, indicator = 1 when use user's y. get it from view
	def get_impact(self, indicator = 0):
		self.get_weighted_conc()
		self.get_risk_pop()
		if indicator == 0:
			self.get_ymin()
		self.get_delta_RR()
		#delta_RR_t = self.delta_RR
		#print delta_RR_t.key
		impact = {}
		for disease in self.disease_code.values():
			if indicator == 0:
				impact[disease] = self.get_disease_impact(disease)
			else:
				impact[disease] = self.get_disease_impact_alternative(disease)
		#impact_t = impact['LC']
		#print impact_t.key
		return impact


