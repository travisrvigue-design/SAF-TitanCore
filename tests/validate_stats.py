"""
Verification harness and STAT-001 validation script.
- Reads a benchmark CSV with at least `throughput_units_per_sec` column across runs
- Performs bootstrapped 95% CI (n=30 resamples) and two-sample t-test and Cohen's d
"""
import argparse
import csv
import math
import statistics
import random
from typing import List

import numpy as np
from scipy import stats

SEED = 42
random.seed(SEED)
np.random.seed(SEED)


def load_throughputs(path: str) -> List[float]:
    vals = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if 'throughput_units_per_sec' in r and r['throughput_units_per_sec']:
                vals.append(float(r['throughput_units_per_sec']))
    return vals


def bootstrap_ci(data: List[float], n_bootstrap: int = 1000, alpha: float = 0.05):
    n = len(data)
    means = []
    for _ in range(n_bootstrap):
        sample = [random.choice(data) for _ in range(n)]
        means.append(statistics.mean(sample))
    lower = np.percentile(means, 100 * (alpha / 2))
    upper = np.percentile(means, 100 * (1 - alpha / 2))
    return lower, upper


def cohens_d(a: List[float], b: List[float]) -> float:
    na, nb = len(a), len(b)
    mean_a, mean_b = statistics.mean(a), statistics.mean(b)
    var_a = statistics.pvariance(a)
    var_b = statistics.pvariance(b)
    pooled = math.sqrt(((na - 1) * var_a + (nb - 1) * var_b) / (na + nb - 2))
    if pooled == 0:
        return 0.0
    return (mean_a - mean_b) / pooled


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--baseline', required=True, help='CSV baseline with throughput_units_per_sec')
    p.add_argument('--candidate', required=True, help='CSV candidate with throughput_units_per_sec')
    p.add_argument('--alpha', type=float, default=0.01)
    args = p.parse_args()

    base = load_throughputs(args.baseline)
    cand = load_throughputs(args.candidate)
    if len(base) < 2 or len(cand) < 2:
        print('Need at least 2 runs per group; recommended n>=30 for CLT')
        return
    # bootstrap CI
    lower_b, upper_b = bootstrap_ci(base, n_bootstrap=1000, alpha=0.05)
    lower_c, upper_c = bootstrap_ci(cand, n_bootstrap=1000, alpha=0.05)
    # t-test
    tstat, pval = stats.ttest_ind(cand, base, equal_var=False)
    d = cohens_d(cand, base)
    print('Baseline mean:', statistics.mean(base), 'Candidate mean:', statistics.mean(cand))
    print('Baseline 95% CI (boot):', lower_b, upper_b)
    print('Candidate 95% CI (boot):', lower_c, upper_c)
    print('t-test p-value:', pval, 'alpha:', args.alpha)
    print("Cohen's d:", d)

if __name__ == '__main__':
    main()
