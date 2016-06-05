import ROOT
from Framework.Core.Analyzer import Analyzer
from Framework.Core.Drawer import Drawer
from Framework.MyUtils.histFunc import makeBinoHist 
from Framework.MyUtils.deltaR import deltaR

class PrefireAnalyzer(Analyzer):
    def beginJob(self):
        # pretrigger rates
        self.hists["dem"] = ROOT.TH1D("dem","dem",len(self.jetPtThresholds),-0.5,len(self.jetPtThresholds)-0.5)
        for pretriggerThreshold in self.pretriggerThresholds:
            self.hists["num_%s"%pretriggerThreshold] = ROOT.TH1D("num_JetPt%s"%pretriggerThreshold,"num",len(self.jetPtThresholds),-0.5,len(self.jetPtThresholds)-0.5)
            nbins = self.hists["num_%s"%pretriggerThreshold].GetNbinsX()
            for ibin in range(1,nbins+1):
                self.hists["num_%s"%pretriggerThreshold].GetXaxis().SetBinLabel(ibin,str(self.jetPtThresholds[ibin-1]))
            self.hists["EtaPhi_%s"%pretriggerThreshold] = ROOT.TH2D("EtaPhi_%s"%pretriggerThreshold,"Eta vs Phi",20,-5.,5.,20,-3.14,3.14)
            self.hists["DeltaR_%s"%pretriggerThreshold] = ROOT.TH1D("DeltaR_%s"%pretriggerThreshold,"DeltaR",20,0.,5.)

    def analyze(self,event):
        indexBx0,jetEtBx0 = self.getLeadingJet(event.jetEt,event.jetBx,0)
        indexBxM1,jetEtBxM1 = self.getLeadingJet(event.jetEt,event.jetBx,-1)
        for ibin,jetPtThreshold in enumerate(self.jetPtThresholds):
            if jetEtBx0 >= jetPtThreshold:
                self.hists["dem"].Fill(ibin)
                for pretriggerThreshold in self.pretriggerThresholds:
                    if jetEtBxM1 >= pretriggerThreshold:
                        self.hists["num_%s"%pretriggerThreshold].Fill(ibin)
                        self.hists["EtaPhi_%s"%pretriggerThreshold].Fill(event.jetEta[indexBxM1],event.jetPhi[indexBxM1])
                        self.hists["DeltaR_%s"%pretriggerThreshold].Fill(deltaR(event.jetEta[indexBxM1],event.jetPhi[indexBxM1],event.jetEta[indexBx0],event.jetPhi[indexBx0]))
        return True

    def endJob(self):
        #super(PrefireAnalyzer,self).endJob()
        drawDict = {}
        tempList = []
        drawDict["EtaPhi.pdf"] = []
        drawDict["DeltaR.pdf"] = []
        for pretriggerThreshold in self.pretriggerThresholds:
            tempList.append(makeBinoHist(self.hists["num_%s"%pretriggerThreshold],self.hists["dem"]))
            drawDict["EtaPhi.pdf"].append(self.hists["EtaPhi_%s"%pretriggerThreshold])
            drawDict["DeltaR.pdf"].append(self.hists["DeltaR_%s"%pretriggerThreshold])
        drawDict["PrefireRate.pdf"] = [tempList]

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
