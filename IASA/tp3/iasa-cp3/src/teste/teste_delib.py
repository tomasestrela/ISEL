import sys
sys.path.append("../lib")
sys.path.append("../agente_prosp")

import psa
import pee
from agenteprospector import AgenteProspector
from controlo_delib.controlodelib import ControloDelib
from controlo_delib.plan.plan_pee.planpee import PlanPEE
from pee.melhorprim.procura_aa import ProcuraAA
from pee.melhorprim.procura_sofrega import ProcuraSofrega
from pee.melhorprim.procura_custo_unif import ProcuraCustoUnif


psa.iniciar("amb/amb2.das")

psa.executar(AgenteProspector(ControloDelib(PlanPEE(ProcuraAA()))))