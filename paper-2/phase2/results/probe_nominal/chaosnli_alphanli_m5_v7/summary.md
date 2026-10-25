# probe_nominal — chaosnli_alphanli, m=5 training positions, 50 reference positions

```
               kl_ref         acc_mode         ent_spearman         resid_spearman         modal_mass_spearman        
                 mean     sem     mean     sem         mean     sem           mean     sem                mean     sem
arm                                                                                                                   
hard           0.2687  0.0022   0.7606  0.0027       0.2441  0.0189            NaN     NaN              0.3383  0.0101
smooth         0.2393  0.0012   0.7816  0.0041       0.3158  0.0160            NaN     NaN              0.3850  0.0085
proto          0.2397  0.0033   0.7821  0.0061       0.2962  0.0161            NaN     NaN              0.3740  0.0080
zc             0.2416  0.0051   0.7768  0.0041       0.3215  0.0211            NaN     NaN              0.3900  0.0128
cond           0.2471  0.0044   0.7727  0.0043       0.3126  0.0232            NaN     NaN              0.3822  0.0151
shrunk         0.2400  0.0048   0.7732  0.0066       0.3197  0.0223            NaN     NaN              0.3905  0.0127
soft           0.2466  0.0030   0.7775  0.0031       0.3056  0.0241            NaN     NaN              0.3890  0.0131
soft_pmode     0.2515  0.0054   0.7821  0.0059       0.2528  0.0180            NaN     NaN              0.3389  0.0129
soft_pzc       0.2461  0.0048   0.7727  0.0036       0.3089  0.0180            NaN     NaN              0.3844  0.0110
fidelity_zc    0.7158  0.0127   0.9319  0.0016       0.5987  0.0042         0.2635  0.0032              0.6257  0.0047
fidelity_soft  0.4512  0.0078   0.9319  0.0016       0.5987  0.0042            NaN     NaN              0.6257  0.0047
```
