
import ROOT
from Framework.Core.Process import Process
from Framework.Core.Sequence import Sequence
from Framework.Core.Parser import option
from Modules.PrefireAnalyzer import PrefireAnalyzer

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
