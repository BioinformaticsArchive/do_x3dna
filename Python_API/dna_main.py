#!/usr/bin/env python
#
#
# This file is part of do_x3dna
#
# Author: Rajendra Kumar
# Copyright (C) 2014  Rajendra Kumar
#
# do_x3dna uses 3DNA package (http://x3dna.org).
# Please cite the original publication of the 3DNA package:
# Xiang-Jun Lu & Wilma K. Olson (2003)
# 3DNA: a software package for the analysis, rebuilding and visualization of three-dimensional nucleic acid structures
# Nucleic Acids Res. 31(17), 5108-21.
#
# do_x3dna is a free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# do_x3dna is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with do_x3dna.  If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import numpy as np
import re, os, sys
import string, random
import subprocess as sub

class base_step:
	def __init__(self):
		self.shift = []
		self.slide = []
		self.rise = []
		self.tilt = []
		self.roll = []
		self.twist = []

		self.x_disp = []
		self.y_disp = []
		self.h_rise = []
		self.inclination = []
		self.tip = []
		self.h_twist = []

		self.hel_Xaxis = []
		self.hel_Yaxis = []
		self.hel_Zaxis = []

class base_pair():
	def __init__(self):
		self.shear = []
		self.stretch = []
		self.stagger = []
		self.buckle = []
		self.propeller = []
		self.opening = []
		
		self.hbond = []

		self.radS1 = []
		self.radS2 = []

class DNA:
	def __init__(self,num_bp):
		self.num_bp = num_bp
		self.num_step = num_bp-1
		self.time = []
		self.base_steps = []
		self.base_pairs = []

		for i in range(num_bp):
			self.base_pairs.append(base_pair())

		for i in range(self.num_step):
			self.base_steps.append(base_step())

	def get_parameters(self,parameter, bp, bp_range=True):
		"""To get the parameters over all frame for the given range of base pair/steps
		Args:
			parameter (string): [Name of the prameter]
			                    Shear
			                    Stretch
			                    Stagger
			                    Buckle
			                    Propeller
			                    Opening
			                    Shift
			                    Slide
			                    Rise
			                    Tilt
			                    Roll
			                    Twist
			                    X-disp
			                    Y-disp
			                    h-Rise
			                    Inclination
			                    Tip
			                    h-Twist
			                    Helical X-axis
			                    Helical Y-axis
			                    Helical Z-axis
			                    Radius S-1
			                    Radius S-2

			bp (list) or (numpy array): base-pairs to analyze
			      Example:
			        for base pair number 6:
			            bp = [6]                                #bp_range = False
			        for base pair number 4  to 15:
			            bp = [4,15]                             #bp_range = True
			            bp = range(4,15)                        #bp_range = False
			            bp = np.arange(4,15)                    #bp_range = False
			        for base pair number 2,5,6,7,9,12 and 18:
			            bp = [2,5,6,7,9,12,18]                  #bp_range = False

			bp_range (bool)	: Dfault=True: Shown above. if True, bp is taken as a range otherwise list or numpy array

		Return (list[bp][nframe]) : where bp is number of base pairs/steps and nframe is number of frames.
		"""
		bp_idx, dum = get_idx_of_bp_parameters(bp,[],bp_range)
		append = False
		empty = False
		Key = 'dum'
		idx = 0
		data=[]
		
		#Extracting data for given base pairs and parameters combination
		#Base pair parameters
		if(parameter=='Shear'):
			for i in range(len(bp_idx)):
				if (len(self.base_pairs[bp_idx[i]].shear) == 0):
					empty = True
					key = 'Shear'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].shear)
					append =True

		if(parameter=='Stretch'):
			for i in range(len(bp_idx)):
				if (len(self.base_pairs[bp_idx[i]].stretch)==0):
					empty = True
					key = 'Stretch'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].stretch)
					append = True

		if(parameter=='Stagger'):
			for i in range(len(bp_idx)):
				if(len(self.base_pairs[bp_idx[i]].stagger)==0):
					empty = True
					key = 'Stagger'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].stagger)
					append = True

		if(parameter=='Buckle'):
			for i in range(len(bp_idx)):
				if(len(self.base_pairs[bp_idx[i]].buckle)==0):
					empty = True
					key = 'Buckle'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].buckle)
					append = True

		if(parameter=='Propeller'):
			for i in range(len(bp_idx)):
				if(len(self.base_pairs[bp_idx[i]].propeller)==0):
					empty = True
					key = 'Propeller'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].propeller)
					append = True

		if(parameter=='Opening'):
			for i in range(len(bp_idx)):
				if(len(self.base_pairs[bp_idx[i]].opening)==0):
					empty = True
					key = 'Opening'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].opening)
					append = True
		
		if(parameter=='Radius S-1'):
			for i in range(len(bp_idx)):
				if(len(self.base_pairs[bp_idx[i]].radS1)==0):
					empty = True
					key = 'Radius S-1'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].radS1)
					append = True


		if(parameter=='Radius S-2'):
			for i in range(len(bp_idx)):
				if(len(self.base_pairs[bp_idx[i]].radS2)==0):
					empty = True
					key = 'Radius S-2'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_pairs[bp_idx[i]].radS2)
					append = True

		#Base step parameters
		if(parameter=='Shift'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].shift)==0):
					empty = True
					key = 'Shift'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].shift)
					append = True

		if(parameter=='Slide'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].slide)==0):
					empty = True
					key = 'Slide'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].slide)
					append = True

		if(parameter=='Rise'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].rise)==0):
					empty = True
					key = 'Rise'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].rise)
					append = True

		if(parameter=='Tilt'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].tilt)==0):
					empty = True
					key = 'Tilt'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].tilt)
					append = True

		if(parameter=='Roll'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].roll)==0):
					empty = True
					key = 'Roll'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].roll)
					append = True

		if(parameter=='Twist'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].twist)==0):
					empty = True
					key = 'Twist'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].twist)
					append = True

		#Base step helical parameters
		if(parameter=='X-disp'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].x_disp)==0):
					empty = True
					key = 'X-disp'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].x_disp)
					append = True

		if(parameter=='Y-disp'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].y_disp)==0):
					empty = True
					key = 'Y-disp'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].y_disp)
					append = True

		if(parameter=='h-Rise'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].h_rise)==0):
					empty = True
					key = 'h-Rise'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].h_rise)
					append = True

		if(parameter=='Inclination'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].inclination)==0):
					empty = True
					key = 'Inclination'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].inclination)
					append = True

		if(parameter=='Tip'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].tip)==0):
					empty = True
					key = 'Tip'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].tip)
					append = True

		if(parameter=='h-Twist'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].h_twist)==0):
					empty = True
					key = 'h-Twist'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].h_twist)
					append = True

		if(parameter=='Helical X-axis'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].hel_Xaxis)==0):
					empty = True
					key = 'Helical X-axis'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].hel_Xaxis)
					append = True

		if(parameter=='Helical Y-axis'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].hel_Yaxis)==0):
					empty = True
					key = 'Helical Y-axis'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].hel_Yaxis)
					append = True

		if(parameter=='Helical Z-axis'):
			for i in range(len(bp_idx)):
				if(len(self.base_steps[bp_idx[i]].hel_Zaxis)==0):
					empty = True
					key = 'Helical Z-axis'
					idx = bp_idx[i]
					break
				else:
					data.append(self.base_steps[bp_idx[i]].hel_Zaxis)
					append = True

		if(empty):
			print 'ERROR: The parameter \"{0}\" for base pair/step \"{1}\" is not set/loaded.\n' .format(key,idx+1)
			exit(1)

		return data, bp_idx

	def set_base_pair_parameters(self, filename, bp, parameters=range(1,7), bp_range=True):
		"""	To read the parameters and set to the base_pair
		Args:
		    filename (string) : output file from do_x3dna. e.g. L-BP_g.dat
		    
		    bp (range list) or (list) or (numpy array): base-pairs to analyze
			      Example:
			        for base pair number 6:
			            bp = [6]                                #bp_range = False
			        for base pair number 4  to 15:
			            bp = [4,15]                             #bp_range = True
			            bp = range(4,15)                        #bp_range = False
			            bp = np.arange(4,15)                    #bp_range = False
			        for base pair number 2,5,6,7,9,12 and 18:
			            bp = [2,5,6,7,9,12,18]                  #bp_range = False
             
		    parameters (list) : list of parameters number to analyze:
		                 shear      =>  1
		                 stretch    =>  2
		                 stagger    =>  3
		                 buckle     =>  4
		                 propeller  =>  5
		                 opening    =>  6
		          Example:
		            for shear, buckle, propeller:
		                parameters = [1,4,6]
		            for stretch to propeller
		                parameters = range(2,6)
		                parameters = [2,3,4,5]
		
		    bp_range (bool) : Shown above. if True, bp should be a range otherwise list or numpy array

		Return:   None
		"""
		if not (isinstance(bp,list) or isinstance(bp,np.ndarray)):
			raise AssertionError("type %s is not list or np.ndarray" % type(bp))
		if not (isinstance(parameters,list) or isinstance(parameters, np.ndarray)):
			raise AssertionError("type %s is not list or np.ndarray" % type(parameters))

		for parameter in parameters:
			if(parameter>6):
				print '\nWARNING: number of requested parameters exceeded to {0} as contrast to six !!\n' .format(parameter)
				print 'Setting number of parameters from one to six\n\n'
				parameters=range(1,6)
				break

		data, time = read_param_file(filename,parameters,bp,bp_range)
		
		if(len(self.time)==0):
			self.time = time
		else:
			if(len(time)!=len(self.time)):
				print '\nTime or number of frame mismatch in input files.\n Exiting...\n'
				exit(1)
		
		bp_idx, param_idx = get_idx_of_bp_parameters(bp,parameters,bp_range)	
		
		for i in range(len(data)):
			for j in range(len(data[i])):
				if(0==param_idx[j]):
					self.base_pairs[bp_idx[i]].shear = data[i][j]
				if(1==param_idx[j]):
					self.base_pairs[bp_idx[i]].stretch = data[i][j]
				if(2==param_idx[j]):
					self.base_pairs[bp_idx[i]].stagger = data[i][j]
				if(3==param_idx[j]):
					self.base_pairs[bp_idx[i]].buckle = data[i][j]
				if(4==param_idx[j]):
					self.base_pairs[bp_idx[i]].propeller = data[i][j]
				if(5==param_idx[j]):
					self.base_pairs[bp_idx[i]].opening = data[i][j]


	def set_helical_radius(self, filename, bp, atomname='P', full=False, bp_range=True):
		"""	To read the parameters and set to the base_pair
		Args:
		    filename (string) : output file from do_x3dna, e.g. HelixRad_g.dat
			
		    bp (range list) or (list) or (numpy array): base-pairs to analyze
			      Example:
			        for base pair number 6:
			            bp = [6]                                #bp_range = False
			        for base pair number 4  to 15:
			            bp = [4,15]                             #bp_range = True
			            bp = range(4,15)                        #bp_range = False
			            bp = np.arange(4,15)                    #bp_range = False
			        for base pair number 2,5,6,7,9,12 and 18:
			            bp = [2,5,6,7,9,12,18]                  #bp_range = False
			
		    atomname (string) : list of atom names to consider the DNA helix (accepted keywords: P O4*/O4' C1*/C1')

		    full (bool): To calculate full helical radius. Overrides atomname option and uses atom 'P', subsequently added 1 A to the radius calculated by 3DNA package.

		    bp_range (bool)   : Shown above. if True, bp should be a range otherwise list or numpy array

		Return: None
		"""
		if not (isinstance(bp,list) or isinstance(bp,np.ndarray)):
			raise AssertionError("type %s is not list or np.ndarray" % type(bp))

		if not ( (atomname=='P') or (atomname=='O4*') or (atomname=='C1*') ):
			print '\n This atomname {0} is not implemented... Exiting\n' .format(atomname)

		
		parameter = []
		if (atomname=='P') or (full):
			parameter = [1,4]
		
		if (atomname=='O4*') and (not full):
			parameter = [2,5]

		if (atomname=='C1*') and (not full):
			parameter = [3,6]

		data, time = read_param_file(filename, range(1,6), bp, bp_range)
		bp_idx, param_idx = get_idx_of_bp_parameters(bp,parameter, bp_range)
		
		if full:
			data = np.add(data, 1.0)
		
		for i in range(len(data)):
			if (atomname=='P') or (full):
				self.base_pairs[bp_idx[i]].radS1 = data[i][0]
				self.base_pairs[bp_idx[i]].radS2 = data[i][3]

			if (atomname=='O4*'):
				self.base_pairs[bp_idx[i]].radS1 = data[i][1]
				self.base_pairs[bp_idx[i]].radS2 = data[i][4]

			if (atomname=='C1*'):
				self.base_pairs[bp_idx[i]].radS1 = data[i][2]
				self.base_pairs[bp_idx[i]].radS2 = data[i][5]

	def set_base_step_parameters(self, filename, bp_step, parameters=range(1,7), step_range=True,helical=False):
		"""	To read the parameters and set to the base_pair
		Args:
		    filename (string) : output file from do_x3dna. e.g. L-BPS_g.dat or L-BPH_g.dat
		
		    bp_step (range list) or (list) or (numpy array): base-pairs step to analyze
			      Example:
			        for base pair number 6:
			            bp = [6]                                #bp_range = False
			        for base pair number 4  to 15:
			            bp = [4,15]                             #bp_range = True
			            bp = range(4,15)                        #bp_range = False
			            bp = np.arange(4,15)                    #bp_range = False
			        for base pair number 2,5,6,7,9,12 and 18:
			            bp = [2,5,6,7,9,12,18]                  #bp_range = False
			
		    parameters (list) : list of parameters number to analyze:
		            if "helical = False"
		                Shift       =>  1
		                Slide       =>  2
		                Rise        =>  3
		                Tilt        =>  4
		                Roll        =>  5
		                Twist       =>  6
		            if "helical = True"
		                X-disp      =>  1
		                Y-disp      =>  2
		                h-Rise      =>  3
		                Inclination =>  4
		                Tip         =>  5
		                h-Twist     =>  6
		            Example: 
		                for Shift, Tilt and Twist:
		                    parameters = [1,4,6]
		                for Slide to Roll:
		                    parameters = range(2,6)
		                    parameters = [2,3,4,5]

		    step_range (bool)  : Shown above. if True, bp_step should be a range otherwise list or numpy array
		
		Return  :    None
		"""
		if not (isinstance(bp_step,list) or isinstance(bp_step,np.ndarray)):
			raise AssertionError("type %s is not list or np.ndarray" % type(bp_step))
		if not (isinstance(parameters,list) or isinstance(parameters, np.ndarray)):
			raise AssertionError("type %s is not list or np.ndarray" % type(parameters))

		for parameter in parameters:
			if(parameter>6):
				print '\nWARNING: number of requested parameters exceeded to {0} as contrast to six !!\n' .format(parameter)
				print 'Setting number of parameters from one to six\n\n'
				parameters=range(1,6)
				break

		data, time = read_param_file(filename,parameters,bp_step,step_range)
		
		if(len(self.time)==0):
			self.time = time
		else:
			if(len(time)!=len(self.time)):
				print '\nTime or number of frame mismatch in input files.\n Exiting...\n'
				exit(1)
		
		bp_idx, param_idx = get_idx_of_bp_parameters(bp_step,parameters,step_range)	
		
		for i in range(len(data)):
			for j in range(len(data[i])):
				if(not helical):
					if(0==param_idx[j]):
						self.base_steps[bp_idx[i]].shift = data[i][j]
					if(1==param_idx[j]):
						self.base_steps[bp_idx[i]].slide = data[i][j]
					if(2==param_idx[j]):
						self.base_steps[bp_idx[i]].rise = data[i][j]
					if(3==param_idx[j]):
						self.base_steps[bp_idx[i]].tilt = data[i][j]
					if(4==param_idx[j]):
						self.base_steps[bp_idx[i]].roll = data[i][j]
					if(5==param_idx[j]):
						self.base_steps[bp_idx[i]].twist = data[i][j]
				if(helical):
					if(0==param_idx[j]):
						self.base_steps[bp_idx[i]].x_disp = data[i][j]
					if(1==param_idx[j]):
						self.base_steps[bp_idx[i]].y_disp = data[i][j]
					if(2==param_idx[j]):
						self.base_steps[bp_idx[i]].h_rise = data[i][j]
					if(3==param_idx[j]):
						self.base_steps[bp_idx[i]].inclination = data[i][j]
					if(4==param_idx[j]):
						self.base_steps[bp_idx[i]].tip = data[i][j]
					if(5==param_idx[j]):
						self.base_steps[bp_idx[i]].h_twist = data[i][j]
		
	def get_mean_error(self,bp,parameter,err_type='std',bp_range=True, merge_bp=1):
		"""To calculate average and error of the given parameter for the gieven set of base-pairs/steps
		Args:
		     bp (list) or (numpy array): base-pairs or base-steps to analyze
			      Example:
			        for base pair number 6:
			            bp = [6]                                #bp_range = False
			        for base pair number 4  to 15:
			            bp = [4,15]                             #bp_range = True
			            bp = range(4,15)                        #bp_range = False
			            bp = np.arange(4,15)                    #bp_range = False
			        for base pair number 2,5,6,7,9,12 and 18:
			            bp = [2,5,6,7,9,12,18]                  #bp_range = False

		     parameter (string): Name of the prameter. Currently accepted keywords as follows:
		                        Shear
		                        Stretch
		                        Stagger
		                        Buckle
		                        Propeller
		                        Opening
		                        Shift
		                        Slide
		                        Rise
		                        Tilt
		                        Roll
		                        Twist
		                        X-disp
		                        Y-disp
		                        h-Rise
		                        Inclination
		                        Tip
		                        Radius S1
		                        Radius S2

		     error (string)  :  Method of error estimation. Currently accepted method as follows:
		                        std   : Standard Deviation
		                        acf   : Standard error using autocorrelation time (requires: g_analyze)
		                        block : Standard error using block averaging method (requires: g_analyze)

		     bp_range (bool)    : Shown above. if True, bp should be a range otherwise list or numpy array

		     merge_bp (integer) : Number of base pair-step to merge

	Return   : [base_pairs/steps], [avg_parameter_values], [error]
	           base_pairs/steps :  base pair-steps number. if merge_bp>1, middle number will be returned
	           avg_parameter_value: average values of the parameter
	           error : corresponding error values
	"""
		merge=False

		if(not bp_range) and (merge_bp>1):
			print ("\nERROR: Merging of base pairs/steps only possible with given base pair/steps range\n")
			exit(1)

		if(bp_range) and (merge_bp>1):
			merge = True
		
		data, bp_idx = self.get_parameters(parameter,bp,bp_range)

		bp_number = np.add(bp_idx,1)
		data = np.array(data)

		# Merging base pairs/step data for the given parameters
		merge_data = []
		mid_bin = []
		if(merge):
			i=0
			while(1):
				start = i
				if((i + merge_bp)>=len(bp_idx)):
					end = i+(len(bp_idx)-i)
				else:
					end   = i + merge_bp	
				
				if(start < end):
					mid_bin.append(int(start+(end-start)/2))
					merge_data.append(np.mean(data[start:end],axis=0))
				
				if(i >= len(bp_idx)):
					break
				
				i += merge_bp

			merge_data = np.array(merge_data)
	
		
		if (err_type == 'std'):
			if(merge):
				error = np.std(merge_data,axis=1)
			else:
				error = np.std(data,axis=1)

		if (err_type =='acf' ) or (err_type =='block' ):
			if(merge):
				error = get_error(self.time, merge_data, len(mid_bin), err_type=err_type)
			else:
				error = get_error(self.time, data, len(bp_idx), err_type=err_type)

		if(merge):
			return mid_bin, np.mean(merge_data,axis=1), error
		else:
			return bp_number, np.mean(data,axis=1), error

	def set_helical_axis(self, filename, step_range=False,step=[]):
		"""	To read the parameters and set to the base_pair
		Args:
		    filename (string) : output file from do_x3dna. e.g. HelAxis_g.dat

		    step_range (bool) : 
		                        if "True"  : read axis coordinates of base-steps for the given range "step"
		                        if "False" : read axis coordinates of all base-steps

		    step (list): list containing lower and higher limit of base-steps range.
		                 This option only works with "step_range=True".
		                 This list should not contain more than two number. 
		                 First number should be less than second number.
		             Example:
		                 for base step number 4  to 15:
		                    step = [4,15]         #step_range = True

		Return   :  None
		"""

		if (step_range):
			if not isinstance(step,list):
				raise AssertionError("type %s is not list" % type(step))
			if (len(step)>2):
				print ("ERROR: Range for helical axis should be list of two numbers, e.g. step=[1, 20] \n")
				exit(1)

		if (step_range):
			data, time = read_param_file(filename,range(1,3),step,True)
		else:
			data, time = read_param_file(filename,range(1,3),[1,self.num_step],True)
		
		if(len(self.time)==0):
			self.time = time
		else:
			if(len(time)!=len(self.time)):
				print '\nTime or number of frame mismatch in input files.\n Exiting...\n'
				exit(1)

		if (step_range):
			bp_idx, param_idx = get_idx_of_bp_parameters(step,[],True)
		else:
			bp_idx, param_idx = get_idx_of_bp_parameters([1,self.num_step],[],True)

		for i in range(len(data)):
			for j in range(len(data[i])):
				if(0==j):
					self.base_steps[bp_idx[i]].hel_Xaxis = data[i][j]
				if(1==j):
					self.base_steps[bp_idx[i]].hel_Yaxis = data[i][j]
				if(2==j):
					self.base_steps[bp_idx[i]].hel_Zaxis = data[i][j]

def parameters_vs_axis(dnaRef, dnaSubj, parameter, bp, axis ='Z', bp_range=True, windows=10, err_type='block'):
	"""To calculate parameter deviation of a DNA to reference DNA along given axis
	   Deviation = Reference_DNA(parameter) - Subject_DNA(parameter)
	Args:
	     dnaRef  (DNA object):   Reference DNA

	     dnaSubj (DNA object):   Subject DNA

	     parameter (string)  :   Name of parameter
		
	     bp (list) or (numpy array): base-pairs to analyze
	         Example:
			        for base pair number 6:
			            bp = [6]                                #bp_range = False
			        for base pair number 4  to 15:
			            bp = [4,15]                             #bp_range = True
			            bp = range(4,15)                        #bp_range = False
			            bp = np.arange(4,15)                    #bp_range = False
			        for base pair number 2,5,6,7,9,12 and 18:
			            bp = [2,5,6,7,9,12,18]                  #bp_range = False

	     bp_range (bool)      : Shown above. if True, bp should be range otherwise list or numpy array
	    
	     windows  (integer)	  : Number of bins along the axis

	Return  : [deviation], [error], [axis], [axis_error]
	        deviation   (numpy array): length = no. of windows; Deviation in the parameter for two given DNA
	        error       (numpy array): length = no. of windows; Standard error in deviation fo each window/bin
	        axis        (numpy array): length = no. of windows; average position of window/bin along given axis
	        axis_error  (numpy array): length = no. of windows; Standard error in average position of window/bin along given axis
	"""
	RefParam, ref_bp_idx = dnaRef.get_parameters(parameter,bp,bp_range)
	RefAxis, dummy = dnaRef.get_parameters('Helical {0}-axis' .format(axis),bp,bp_range)
	SubjParam, subj_bp_idx = dnaSubj.get_parameters(parameter,bp,bp_range)

	mean_axis = np.mean(RefAxis,axis=1)
	meanRefParam = np.mean(RefParam,axis=1)
	meanSubjParam = np.mean(SubjParam,axis=1)
	
	maxAxis = np.amax(mean_axis)
	minAxis = np.amin(mean_axis)
	axis_range = (maxAxis-minAxis)/windows

	Ref_param_error = get_error(dnaRef.time, RefParam, len(ref_bp_idx), err_type=err_type)
	Ref_axis_error = get_error(dnaRef.time, RefAxis, len(ref_bp_idx), err_type=err_type)
	subj_param_error = get_error(dnaSubj.time, SubjParam, len(subj_bp_idx), err_type=err_type)

	merged_ref_param =[]
	merged_subj_Param = []
	merged_Ref_param_error = []
	merged_Ref_axis_error = []
	merged_subj_param_error = []

	final_axis = []

	for i in range(windows):
		start = minAxis+(i*axis_range)
		end = start + axis_range
		idx = []
		for j in range(len(mean_axis)):
			if((start <= mean_axis[j]) and (end>mean_axis[j])):
				idx.append(j)
		if(len(idx)>0):
			merged_ref_param.append(meanRefParam[idx])
			merged_subj_Param.append(meanSubjParam[idx])
			final_axis.append( start + (end-start)/2 )
			merged_Ref_param_error.append(Ref_param_error[idx])
			merged_Ref_axis_error.append(Ref_axis_error[idx])
			merged_subj_param_error.append(subj_param_error[idx])


	final_ref_param = []
	final_subj_param = []
	final_ref_param_error = []
	final_ref_axis_error = []
	final_subj_param_error = []
	for i in range(len(merged_ref_param)):
		final_ref_param.append(np.sum(merged_ref_param[i]))
		final_subj_param.append(np.sum(merged_subj_Param[i]))
		
		final_ref_axis_error.append(np.sqrt( (merged_Ref_axis_error[i]**2).sum() ))
		final_ref_param_error.append(np.sqrt( (merged_Ref_param_error[i]**2).sum() ))
		final_subj_param_error.append(np.sqrt( (merged_subj_param_error[i]**2).sum() ))

	deviation,error = get_deviation(final_ref_param,final_ref_param_error,final_subj_param,final_subj_param_error)
	
	return deviation, error, final_axis, final_ref_axis_error

	

def get_error(time,x,sets,err_type='acf'):
	"""To estimate error using block averaging method
	It requires 'g_analyze' of Gromacs package. If 'g_analyze' is not in PATH, this function will not work.

	Args:
		time (list or numpy array):		Containing time
		x	 (list or numpy array): of shape (nset,nframe); where nset is number of set and nframe is number of frame.
										nframe should be equal to length of time list/array
		sets (integer)			  : Number of sets
	
		err_type (string)		  : Error estimation by autocorrelation time 'acf' or block avearaging method 'block'	
	Return:
		error (numpy error)	: of length = sets
	"""
	for i in range(sets):
		if (len(time) != len(x[i])):
			print '\nError: number of frame in time {0} mismatched with {1} of x[{2}]!!\n' .format(len(time),len(x[i]),i)
			exit(1)
	if not((err_type=='block') or (err_type=='acf')):
		print '\nWarning: Method {0} is not implemented. Swtiching to \'acf\'.\n' .format(err_type)
		err_type = 'acf'

	error = []
	char_set = string.ascii_lowercase
	name = ''.join(random.sample(string.ascii_lowercase, 10))
	
	filename = name+'.xvg'
	eefile = 'ee_'+name+'.xvg'
	acfile = 'acf_'+name+'.xvg'

	fout = open(filename,'w')
	for i in range(len(time)):
		fout.write('{0}' .format(time[i]))
		for j in range(sets):
			fout.write('\t{0}' .format(x[j][i]))
		fout.write("\n")
	fout.close()

	command = 'g_analyze -f {0} -ee {1} -ac {2} -fitfn exp' .format(filename,eefile,acfile)
	p = sub.Popen(command.split(), stdout=sub.PIPE, stderr=sub.PIPE)
	out, outputerror = p.communicate()
	lines = out.split('\n')

	if (err_type=='block'):
		for line in lines:
			if(re.match('Set',line)):
				temp = line.split()
				error.append(float(temp[3]))

	if (err_type=='acf'):
		acf_time = []
		for line in lines:
			if(re.match('COR: Correlation time',line)):
				temp = line.split('=')
				acf_time.append(abs(float(temp[1].split()[0])))
	
		total_time = float(time[-1])-float(time[0])
		dt = total_time/len(time)
		for i in range(sets):
			if(acf_time[i]>=dt):
				n_indp = total_time/acf_time[i]
				tmp_err = np.std(x[i])/np.sqrt(n_indp)
			else:
				tmp_err = np.std(x[i])/np.sqrt(len(time))
			error.append(tmp_err)
	
	os.remove(filename)
	os.remove(eefile)
	os.remove(acfile)
	if os.path.isfile('fitlog.log'):
		os.remove('fitlog.log')
	return np.array(error)

def get_deviation(Ref,RefErr,x,xerr):
	if (len(Ref) != len (x)):
		print "\nErrori: Number of base pairs/steps mismatch from reference to target!!\n"
		exit(1)
	Ref = np.array(Ref)
	RefErr = np.array(RefErr)
	x = np.array(x)
	xerr = np.array(xerr)

	covariance = np.cov(Ref,x)

	deviation = Ref-x
	error = np.sqrt( (RefErr*RefErr) + (xerr*xerr))

	return deviation, error
	

def read_data_file(FileName,cols_equal=True):
	infile = open(FileName,'r')
	data = []
	len_data = 0
	i=1
	for line in infile:
		line = line.rstrip('\n')
		if not line.strip():
			continue
		if(re.match('#|@',line)==None):
			temp = map(float,line.split())
			if(cols_equal):
				if (i==1):
					len_data = len(temp)
				if (len(temp) != len_data):
					print 'WARNING: Number of column mis match at line {0} in {1}; skipping remaining part\n' .format(i,FileName)
					break
				data.append(temp)
			i = i+1
	data = np.array(data).T
	return data

def get_idx_of_bp_parameters(bp,parameters,bp_range):
	param_idx = []
	if(bp_range):
		bp_idx = np.arange(bp[0]-1,bp[1])
	else:
		bp_idx = np.subtract(bp,1)
	
	if(len(parameters)!=0):
		param_idx = np.hstack((np.subtract(parameters,1),[parameters[-1]]))
	return bp_idx, param_idx

def read_param_file(FileName,parameters,bp,bp_range):

	sys.stdout.write("\nReading file : %s\n" % FileName)
	sys.stdout.flush()
	
	def get_frame_data(block,parameters,bp_idx):
		block = np.array(block).T
		temp_data = (block[parameters,:])[:,bp_idx].copy()
		return temp_data

	def get_time(line):
		dummy, temp_time = line.split('=')
		return temp_time 

	infile = open(FileName,'r')
	data = []
	time = []
	frame_number = 0

	bp_idx, param_idx = get_idx_of_bp_parameters(bp,parameters,bp_range)

	block = []
	for line in infile:

		#Removing last new line charecter
		line = line.rstrip('\n')
		
		#Skipping blank/empty line
		if not line.strip():
			continue
		
		#Getting Time tag and time => Starting of new frame
		if(re.match('# Time',line)!=None):
			
			if((frame_number<100) and (frame_number%10==0)) or ((frame_number<1000) and (frame_number%100==0)) or ((frame_number<10000) and (frame_number%1000==0)) or ((frame_number<100000) and (frame_number%10000==0)) or ((frame_number<1000000) and (frame_number%100000==0)):
				sys.stdout.write("\rReading frame %d" % frame_number)
				sys.stdout.flush()
			
			frame_number += 1
			
			#if(frame_number==5000):
				#break
			
			#Getting time
			time.append(get_time(line))
			
			#Getting parameters/values for base-pairs
			if(len(block)>0):
				data.append(get_frame_data(block,param_idx,bp_idx))
			block = []
			continue

		#Skipping other lines starting with '#' tag
		if(re.match('#',line)!=None):
			continue
		
		block.append(map(float,line.split()))
	
	#For last frame
	data.append(get_frame_data(block,param_idx,bp_idx))
	block= []
	data_transpose = np.array(data).T

	sys.stdout.write("\nFinishid reading.... Total number of frame read =  %d\n" % frame_number)
	sys.stdout.flush()

	return data_transpose, time