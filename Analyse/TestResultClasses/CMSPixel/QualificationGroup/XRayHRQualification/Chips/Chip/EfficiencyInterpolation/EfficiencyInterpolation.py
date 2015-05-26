# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_EfficiencyInterpolation_TestResult'
        self.NameSingle = 'EfficiencyInterpolation'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'InterpolatedEfficiency50': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Interpolated Efficiency 50'
            },
            'InterpolatedEfficiency150': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Interpolated Efficiency 150'
            },
        }
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        RealHitrateList = array.array('d', [0])
        EfficiencyList = array.array('d', [100])
        ScalingFactor = 1e-6
        for Rate in Rates:
            RealHitRate = float(self.ParentObject.ResultData['SubTestResults']['BackgroundMap_{:d}'.format(Rate)].ResultData['KeyValueDictPairs']['RealHitrate']['Value'])
            RealHitrateList.append(RealHitRate*ScalingFactor)
            Efficiency = float(self.ParentObject.ResultData['SubTestResults']['EfficiencyDistribution_{:d}'.format(Rate)].ResultData['KeyValueDictPairs']['mu']['Value'])
            EfficiencyList.append(Efficiency)
        
        self.Canvas.Clear()
        print RealHitrateList
        
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(RealHitrateList),RealHitrateList,EfficiencyList)
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            
            
            self.ResultData['Plot']['ROOTObject'].Fit('pol2')
            InterpolationFunction = self.ResultData['Plot']['ROOTObject'].GetFunction('pol2')
            
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 110.);
            self.ResultData['Plot']['ROOTObject'].Draw();
            
            line50 = ROOT.TLine().DrawLine(
                50e6*ScalingFactor, 0,
                50e6*ScalingFactor, 100)
            line50.SetLineWidth(2);
            line50.SetLineStyle(2)
            line50.SetLineColor(ROOT.kRed)
            line150 = ROOT.TLine().DrawLine(
                150e6*ScalingFactor, 0,
                150e6*ScalingFactor, 100)
            line150.SetLineWidth(2);
            line150.SetLineStyle(2)
            line150.SetLineColor(ROOT.kRed)
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0 * self.ResultData['Plot'][
            #    'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Hitrate [MHz/cm2]");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Efficiency [%]");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency50']['Value'] = '{:1.2f}'.format(InterpolationFunction.Eval(50e6*ScalingFactor))
            self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency150']['Value'] = '{:1.2f}'.format(InterpolationFunction.Eval(150e6*ScalingFactor))
            self.ResultData['KeyList'] += ['InterpolatedEfficiency50','InterpolatedEfficiency150'] 

        self.SaveCanvas()
        self.Title = 'Efficiency Interpolation: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        


