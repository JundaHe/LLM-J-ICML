# probe_nominal — chaosnli_alphanli, m=10 training positions, 50 reference positions

```
               kl_ref         acc_mode         ent_spearman         resid_spearman         modal_mass_spearman        
                 mean     sem     mean     sem         mean     sem           mean     sem                mean     sem
arm                                                                                                                   
hard           0.2676  0.0014   0.7664  0.0031       0.2599  0.0245            NaN     NaN              0.3444  0.0134
smooth         0.2400  0.0041   0.7848  0.0047       0.2985  0.0209            NaN     NaN              0.3716  0.0085
proto          0.2368  0.0039   0.7833  0.0043       0.3047  0.0139            NaN     NaN              0.3739  0.0055
zc             0.2404  0.0047   0.7763  0.0039       0.3202  0.0223            NaN     NaN              0.3915  0.0125
cond           0.2374  0.0041   0.7783  0.0051       0.3303  0.0152            NaN     NaN              0.4022  0.0061
shrunk         0.2369  0.0044   0.7790  0.0050       0.3373  0.0128            NaN     NaN              0.4018  0.0079
soft           0.2429  0.0034   0.7756  0.0029       0.3278  0.0224            NaN     NaN              0.3904  0.0136
soft_pmode     0.2511  0.0040   0.7744  0.0045       0.2527  0.0162            NaN     NaN              0.3302  0.0069
soft_pzc       0.2391  0.0046   0.7768  0.0037       0.3268  0.0172            NaN     NaN              0.3919  0.0125
fidelity_zc    0.3711  0.0065   0.9493  0.0036       0.6948  0.0048         0.2894  0.0037              0.7071  0.0052
fidelity_soft  0.2351  0.0041   0.9493  0.0036       0.6976  0.0042            NaN     NaN              0.7071  0.0052
```
