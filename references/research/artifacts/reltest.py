import warnings; warnings.filterwarnings('ignore')
import numpy as np, math
from lifelines import WeibullFitter
d=[1000,1400,1800,2200,2600,3000,3600,4000,4000]
ev=[1]*7+[0]*2
wf=WeibullFitter().fit(d,event_observed=ev)
print(f"lifelines: lambda_={wf.lambda_:.5f} rho_={wf.rho_:.3f} (2例右删失,用大值代替inf)")
print(f"  B10 = {wf.percentile(0.10):.0f} cycles")
from scipy.stats import weibull_min
from scipy.optimize import minimize
def nll(th):
    eta=math.exp(th[0]); ll=0.0
    for t,e in zip(d,ev):
        if e: ll += np.log(weibull_min.pdf(t,1.0,loc=0,scale=eta))
        else:  ll += np.log(1-weibull_min.cdf(t,1.0,loc=0,scale=eta))
    return -ll
r=minimize(nll,[math.log(2500.)],method='Nelder-Mead')
print(f"手写右删失MLE eta={math.exp(r.x[0]):.1f}  (应≈lifelines 1/lambda_={1/wf.lambda_:.1f})")
from scipy.stats import chi2
nz=lambda R0,C=0.90: math.ceil(math.log(1-C)/math.log(R0))
print("\n零失效样本量 (test-to-pass):")
for R0,C in [(10e-6,0.90),(10e-6,0.95),(10e-6,0.99),(100e-6,0.90)]:
    print(f"  R0={R0:.0e} C={C:.0%} -> n={nz(R0,C)}")
nf=lambda R0,r,CL=0.90: int(chi2.ppf(CL,2*r)/(-2*math.log(R0)))
print("有失效样本量 (R0=10ppm,CL=90%):", {f"r={r}":nf(10e-6,r) for r in (1,2,3,5)})
