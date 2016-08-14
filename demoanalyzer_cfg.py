import FWCore.ParameterSet.Config as cms
from RecoMuon.TrackingTools.MuonServiceProxy_cff import *
import PhysicsTools.PythonAnalysis.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
process = cms.Process("Validation")


process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('Validation')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
        limit = cms.untracked.int32(-1)
        )
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
# **********************************************************************
# set the maximum number of events to be processed                     *
#    this number (argument of int32) is to be modified by the user     *
#    according to need and wish                                        *
#    default is preset to 10000 events                                 *
# **********************************************************************
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20000000) )

# set the number of events to be skipped (if any) at end of file below

# define JSON file
goodJSON = '/home/cms-opendata/CMSSW_4_2_8/src/Validation/Mu_Mumonitor_dimuon_2010/datasets/Cert_136033-149442_7TeV_Apr21ReReco_Collisions10_JSON_v2.txt'

myLumis = LumiList.LumiList(filename = goodJSON).getCMSSWString().split(',')

# ****************************************************************************
# define the input data set here by inserting the appropriate .txt file list *
# ****************************************************************************
import FWCore.Utilities.FileUtils as FileUtils
#
# ****************************************************************
# exactly one of the following 'files2010data =' statements      *
# should be uncommented.                                         *
# For MUO-10-004, the default is the Mu data set.                *
# To run over all sets, replace '0000' by '0001' etc.            *
# consecutively (make sure you save the output before rerunning) *
# and add up the histograms using root tools.                    *
# ****************************************************************
#
# *** Mu data set ***
files2010data = FileUtils.loadListFromFile ('/home/cms-opendata/CMSSW_4_2_8/src/Validation/Mu_Mumonitor_dimuon_2010/datasets/CMS_Run2010B_Mu_AOD_Apr21ReReco-v1_0000_file_index.txt')
process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring(*files2010data))

# apply JSON file
#   (needs to be placed *after* the process.source input file definition!)
process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
process.source.lumisToProcess.extend(myLumis)

# *************************************************
# number of events to be skipped (0 by default)   *
# *************************************************
process.source.skipEvents = cms.untracked.uint32(0)


process.demo = cms.EDAnalyzer('Mu_Mumonitor_dimuon_2010'
)
# ***********************************************************
# output file name                                          *
# change this according to input file, or according to wish *
# ***********************************************************
process.TFileService = cms.Service("TFileService",
# *********************************************************
# exactly only one of the following should be uncommented *
# *********************************************************
       fileName = cms.string('Mu00val.root')
                                   )
process.p = cms.Path(process.demo)
