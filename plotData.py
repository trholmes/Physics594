# This is a deeply un-optimized but conceptually simple implementation
# Like any other program that loops over many events in simple python, it's very slow
# If you want to to more data, faster you can try any of these methods:
#   Look into RDataFrames in ROOT
#   Try writing the same code in C++
#   Try using uproot to load data and iterate with numpy

import ROOT

# Load in our data file
fname = '/lustre/isaac/proj/UTK0219/data/Run2012BC_DoubleMuParked_Muons.root'
myFile = ROOT.TFile(fname, "read")
myTree = myFile.Get("Events")

# Choose a maximum number of events to plot
max_events = 1000

# Create a histogram object to fill
h = ROOT.TH1F("invmass", "invmass", 30, 70, 100)

# Loop over events and fill histograms
for i, event in enumerate(myTree):

    # Stop if we hit max events
    if i > max_events: break

    # Only look at events with exactly two muons
    if event.nMuon == 2: 

        # Check if they have opposite sign
        if event.Muon_charge[0]*event.Muon_charge[1] == -1:

            # Create our 4-vectors
            m0 = ROOT.TLorentzVector()
            m1 = ROOT.TLorentzVector()
            m0.SetPtEtaPhiM(event.Muon_pt[0], event.Muon_eta[0], event.Muon_phi[0], event.Muon_mass[0])
            m1.SetPtEtaPhiM(event.Muon_pt[1], event.Muon_eta[1], event.Muon_phi[1], event.Muon_mass[1])
            
            # Calculate invariant mass
            inv_mass = (m0+m1).M()

            # Fill our histogram with invariant mass
            h.Fill(inv_mass)

# A bunch of style settings
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptFit(1)

# Now that our histogram is filled, display it
c = ROOT.TCanvas("c", "c", 500, 500)
h.GetXaxis().SetTitle("m_{#mu#mu} [GeV]")
h.GetYaxis().SetTitle("N_{events}")
h.Draw()

# Fit a function
myFit = ROOT.TF1("f", "gaus", 70, 100)
h.Fit(myFit)
c.Update()
input("...")

# Save the histogram as an image
c.SaveAs("dimuonInvariantMass.pdf")

myFile.Close()

