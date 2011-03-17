from minty.utils import deferred_root_loader, make_deferred_instance

EnergyRescaler = deferred_root_loader("EnergyRescaler.cxx+", "EnergyRescaler")

def initialize_EnergyRescaler(EnergyRescaler):
    er = EnergyRescaler()
    er.useDefaultCalibConstants()
    return er

energy_rescaler = make_deferred_instance(EnergyRescaler, initialize_EnergyRescaler)

v16_E_correction = energy_rescaler.applyEnergyCorrection

