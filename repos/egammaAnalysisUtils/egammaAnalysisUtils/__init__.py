from minty.utils import deferred_root_loader, make_deferred_instance

CaloIsoCorrection = deferred_root_loader("CaloIsoCorrection.cxx", "CaloIsoCorrection")

calo_iso_correction = make_deferred_instance(CaloIsoCorrection)
GetPtEDCorrectedIsolation = calo_iso_correction.GetPtEDCorrectedIsolation
