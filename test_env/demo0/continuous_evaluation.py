from ce.kpi import LessWorseKpi

kpi0 = LessWorseKpi(
    name='cost0',
    actived=True,
    threshold=0.02,
    unit_repr='qps',
    short_description='Some description',
    description='some long description')

kpi1 = LessWorseKpi(
    name='cost1',
    actived=True,
    threshold=0.02,
    unit_repr='qps',
    short_description='Some description',
    description='some long description')

tracking_kpis = [kpi0, kpi1]
