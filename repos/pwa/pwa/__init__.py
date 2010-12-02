from minty.main import make_main

from .purity.d3pd import PurityAnalysis

purity_main = make_main(PurityAnalysis)
