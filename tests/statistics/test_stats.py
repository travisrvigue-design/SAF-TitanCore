import numpy as np
from scipy import stats


def test_statistical_validation():
    # deterministic sample data
    a = np.array([1.0, 2.0, 3.0, 4.0])
    b = np.array([1.1, 1.9, 3.05, 3.95])
    mse = np.mean((a - b)**2)
    tstat, pval = stats.ttest_ind(a, b)
    cohens_d = (np.mean(a) - np.mean(b)) / (np.sqrt(((a.std(ddof=1) ** 2) + (b.std(ddof=1) ** 2)) / 2))
    assert mse < 0.02
    assert pval > 0.01  # not significantly different at alpha=0.01
    assert abs(cohens_d) < 0.2
