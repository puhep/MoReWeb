# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
	def CustomInit(self):
		self.Name='CMSPixel_ModuleTestGroup_Module_Dummy_TestResult'
		self.NameSingle='Dummy'
		self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
		self.Title = '_'
	def SetStoragePath(self):
		pass
		
	def PopulateResultData(self):
		pass