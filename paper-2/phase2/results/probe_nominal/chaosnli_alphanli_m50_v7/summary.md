# probe_nominal — chaosnli_alphanli, m=50 training positions, 50 reference positions

```
               kl_ref         acc_mode         ent_spearman         resid_spearman        modal_mass_spearman        
                 mean     sem     mean     sem         mean     sem           mean    sem                mean     sem
arm                                                                                                                  
hard           0.2684  0.0021   0.7618  0.0040       0.2685  0.0208            NaN    NaN              0.3590  0.0117
smooth         0.2475  0.0017   0.7780  0.0048       0.2995  0.0178            NaN    NaN              0.3721  0.0120
proto          0.2402  0.0041   0.7824  0.0067       0.3162  0.0138            NaN    NaN              0.3774  0.0074
zc             0.2435  0.0044   0.7746  0.0037       0.3270  0.0209            NaN    NaN              0.3915  0.0106
cond           0.2326  0.0019   0.7792  0.0044       0.3415  0.0112            NaN    NaN              0.4002  0.0060
shrunk         0.2362  0.0040   0.7831  0.0043       0.3376  0.0174            NaN    NaN              0.3995  0.0096
soft           0.2385  0.0042   0.7831  0.0041       0.3351  0.0182            NaN    NaN              0.3983  0.0119
soft_pmode     0.2404  0.0060   0.7812  0.0074       0.3218  0.0063            NaN    NaN              0.3882  0.0044
soft_pzc       0.2387  0.0024   0.7802  0.0036       0.3376  0.0157            NaN    NaN              0.3992  0.0101
fidelity_zc    0.0661  0.0028   0.9688  0.0025       0.8359  0.0026         0.2996  0.026              0.8369  0.0025
fidelity_soft  0.0455  0.0014   0.9688  0.0025       0.8360  0.0025            NaN    NaN              0.8369  0.0025
```
