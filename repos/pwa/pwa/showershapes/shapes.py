import ROOT as R

def get_objects(d, typename):
    keys = sorted(d.GetListOfKeys(), key=lambda k: k.GetName())
    return [k.ReadObj() for k in keys if k.GetClassName() == typename]

def draw_projected(bin, *hists):
    cols = [
        R.kRed, R.kGreen, R.kBlue, R.kViolet, R.kOrange
    ]
    def col(i):
        return cols[i % len(cols)]
        
    ret = []
    for i, h in enumerate(hists):
        ya = h.GetYaxis()
        ya.SetRange(bin, bin+1)
        print "Bin:", ya.GetBinLowEdge(bin), ya.GetBinUpEdge(bin)
        p = h.Project3D("x")
        if ret:
            p.Scale(ret[0].Integral() / p.Integral())
        p.SetName("h%i" % i)
        p.SetLineColor(col(i))
        p.SetFillColor(col(i))
        p.Draw("same" if i else "")
        ret.append(p)
    R.gPad.Update()
    return ret
    

def process():
    f_mc = R.TFile.Open("PythiaPhotonJet.root") #merged_mc/all.root")
    f_data = R.TFile.Open("periodE.root") #merged_data/all.root")
    
    f_mc.ls()
    f_data.ls()
    o1s = get_objects(f_mc.Get("g10_loose/photon/bkg/unconv/rtight"), "TH3F")
    o2s = get_objects(f_mc.Get("g10_loose/photon/sig/unconv/rtight"), "TH3F")
    
    #f_data.Get("g10_loose/photon").ls()
    
    o3s = get_objects(f_data.Get("g10_loose/photon/sig/unconv/rtight"), "TH3F")
    var = "reta"
    #o3s = []
    static = [
        f_mc.Get("g10_loose/photon/bkg/conv/rtight/%s" % var),
        #f_mc.Get("g10_loose/photon/sig/conv/rtight/%s" % var),
        f_mc.Get("g10_loose/photon/bkg/unconv/rtight/%s" % var),
        #f_mc.Get("g10_loose/photon/sig/unconv/rtight/%s" % var),
        f_mc.Get("g10_loose/electron/sig/rtight/reta"),
        #f_data.Get("g10_loose/photon/sig/conv/rtight/%s" % var),
        #f_data.Get("g10_loose/electron/bkg/rtight/%s" % var),
    ]
    try:
        for i in xrange(static[0].GetYaxis().GetNbins()):
            draw_projected(i+1, *static)
            raw_input()
        #raw_input()
    except (KeyboardInterrupt, EOFError):
        pass    
    print "!!!!!!!!!!!!!!!!!!!!!!!!!"
    print "!!!!!!!!! DONE !!!!!!!!!!"
    print "!!!!!!!!!!!!!!!!!!!!!!!!!"
    
    return
    
    def get_parameters(h, axis_obj, ax_str):
        result = []
        for i in xrange(1, axis_obj.GetNbins()+1):
            axis_obj.SetRange(i, i+1)
            #hp = h.Project3D(ax_str)
            result.append((axis_obj.GetBinCenter(i), (h.GetMean(2), h.GetRMS(2))))
        return result
    
    try:
        #for o1, o2, o3 in zip(o1s, o2s, o3s):
        for o1, o2, o3 in static:
            #for i in xrange(o1.Get
            #print get_parameters(o1, o1.GetYaxis(), "x")
            
            #break
            #o1.GetYaxis().GetNbins()
            #o1.GetYaxis().SetRange(
            """
            h1 = o1.Project3D("x")
            h1.SetName("mcbkg")
            h1.SetLineColor(R.kBlue)
            h1.Draw()
            print list(h1.GetListOfFunctions())
            R.gPad.Update()
            h1.GetListOfFunctions().FindObject("stats").SetName("statbkg")
            """
            
            h2 = o2.Project3D("x")
            h2.SetName("mcsig")
            h2.SetLineColor(R.kRed)
            #h2.Scale(h1.Integral() / h2.Integral())
            h2.Draw()
            print "Updated"
            R.gPad.Update()
            print list(h2.GetListOfFunctions()) #.FindObject("stats")
            
            h3 = o3.Project3D("x")
            h3.SetName("data")
            h3.SetLineColor(R.kGreen)
            h3.Scale(h2.Integral() / h3.Integral())
            h3.Draw("same")
            
            print "Updated"
            R.gPad.Update()
            
            for p in R.gPad.GetListOfPrimitives():
                if hasattr(p, "GetListOfFunctions"):
                    print list(p.GetListOfFunctions())
            
            raw_input()    
    except (KeyboardInterrupt, EOFError):
        pass
    #print f.exception_count.GetVal()

def main():
    from sys import argv
    from optparse import OptionParser
    
    o = OptionParser()
    opts, args = o.parse_args(argv)
    
    process()
    
    #for arg in args[1:]:
        #process(arg)
    
