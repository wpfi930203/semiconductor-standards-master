import math
from scipy.stats import chi2
# 零失效：n = ln(1-CL) / ln(R)   —— 注意 R 是"可靠度"，不是失效率！
def n_zero_fail(R, CL=0.90):
    """R: 目标可靠度(如 0.99999 对应 10ppm)。"""
    return math.ceil(math.log(1-CL)/math.log(R))
print("零失效样本量 (test-to-pass)：目标失效率 R0 → 可靠度 R=1-R0")
for R0 in (10e-6, 100e-6, 1000e-6):
    R = 1-R0
    row = {f"CL={int(c*100)}%": n_zero_fail(R,c) for c in (0.90,0.95,0.99)}
    print(f"  R0={R0:>8.0e} (={R0*1e6:>4.0f} ppm) R={R:.6f} -> {row}")
# 有失效：n = chi2_{CL}(2r+2) / (2*(-ln R))
def n_fail(R, r, CL=0.90):
    return int(math.ceil(chi2.ppf(CL, 2*r+2) / (2*(-math.log(R)))))
R=1-10e-6
print(f"\n有失效样本量 (R0=10ppm, R={R:.6f})：")
for r in (0,1,2,3,5):
    print(f"  r={r} 失效 -> n={n_fail(R,r)}")
# 校验：MIL-HDBK-217 / 常见表 R=0.90 CL=0.90 r=0 应为 22
print("\n校验 (业界常识值对照):")
print("  R=0.90 CL=90% r=0 ->", n_zero_fail(0.90,0.90), "(常见表: 22)")
print("  R=0.95 CL=90% r=0 ->", n_zero_fail(0.95,0.90), "(常见表: 29)")
print("  R=0.90 CL=95% r=0 ->", n_zero_fail(0.90,0.95), "(常见表: 45)")
print("  R=0.90 CL=90% r=1 ->", n_fail(0.90,1,0.90), "(常见表: 46)")
