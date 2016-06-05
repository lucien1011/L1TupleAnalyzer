
import ROOT
from Framework.Core.Process import Process
from Framework.Core.Sequence import Sequence
from Framework.Core.Parser import option
from Framework.Core.Analyzer import Analyzer
from Framework.Core.Drawer import Drawer
from Framework.MyUtils import makeBinoHist 

class PrefireAnalyzer(Analyzer):
    def beginJob(self):
        # pretrigger rates
        self.hists["dem"] = ROOT.TH1D("dem","dem",len(self.jetPtThresholds),-0.5,len(self.jetPtThresholds)-0.5)
        for pretriggerThreshold in self.pretriggerThresholds:
            self.hists["num_%s"%pretriggerThreshold] = ROOT.TH1D("num_JetPt%s"%pretriggerThreshold,"num",len(self.jetPtThresholds),-0.5,len(self.jetPtThresholds)-0.5)
            nbins = self.hists["num_%s"%pretriggerThreshold].GetNbinsX()
            for ibin in range(1,nbins+1):
                self.hists["num_%s"%pretriggerThreshold].GetXaxis().SetBinLabel(ibin,str(self.jetPtThresholds[ibin-1]))
        # jet eta
        self.hists["EtaPhi"] = ROOT.TH2D("EtaPhi","Eta vs Phi",20,-5.,5.,20,-3.14,3.14)

    def analyze(self,event):
        indexBx0,jetEtBx0 = self.getLeadingJet(event.jetEt,event.jetBx,0)
        indexBxM1,jetEtBxM1 = self.getLeadingJet(event.jetEt,event.jetBx,-1)
        for ibin,jetPtThreshold in enumerate(self.jetPtThresholds):
            if jetEtBx0 >= jetPtThreshold:
                self.hists["dem"].Fill(ibin)
                for pretriggerThreshold in self.pretriggerThresholds:
                    if jetEtBxM1 >= pretriggerThreshold:
                        self.hists["num_%s"%pretriggerThreshold].Fill(ibin)
                        self.hists["EtaPhi"].Fill(event.jetEta[indexBxM1],event.jetPhi[indexBxM1])
        return True

    def endJob(self):
        #super(PrefireAnalyzer,self).endJob()
        drawDict = {}
        tempList = []
        for pretriggerThreshold in self.pretriggerThresholds:
            tempList.append(makeBinoHist(self.hists["num_%s"%pretriggerThreshold],self.hists["dem"]))
        drawDict["PrefireRate.pdf"] = [tempList]
        drawDict["EtaPhi.pdf"] = [self.hists["EtaPhi"]]

        Drawer.drawEverything(drawDict,self.outputDir)


    @staticmethod
    def getLeadingJet(EtCollection,bxCollection,bx):
        index = -1
        maxJetEt = -1
        for ijet,jetEt in enumerate(EtCollection):
            if bxCollection[ijet] != bx: continue
            if jetEt > maxJetEt:
                maxJetEt = jetEt
                index = ijet
        return index,maxJetEt

# ____________________________________________________________________________________________________ ||
# Preparation
process                 = Process()
sequence                = Sequence()
process.sequence        = sequence

prefireAna                          = PrefireAnalyzer("Prefire")
prefireAna.pretriggerThresholds     = [60.,90.,120.,150.,180.]
prefireAna.jetPtThresholds          = [120.,150.,180.,210.,240.]
prefireAna.outputDir                = option.outputDir

sequence.load(prefireAna)

# ____________________________________________________________________________________________________ ||
# Configurables
process.inputDir        = option.inputDir
process.outputPath      = option.outputDir+"/PrefireResult.root"
process.treePaths       = ["l1UpgradeTree/L1UpgradeTree","l1EventTree/L1EventTree"]

# ____________________________________________________________________________________________________ ||
# Run!
process.run()

# ____________________________________________________________________________________________________ ||
