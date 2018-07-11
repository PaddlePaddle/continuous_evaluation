from .continuous_evaluation import *

for i in range(10):
    kpi0.add_record(0.1 * i)
    kpi1.add_record(0.1 * i)

for kpi in kpis:
    kpi.persist()
