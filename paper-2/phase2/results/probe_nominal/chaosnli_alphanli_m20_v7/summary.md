# probe_nominal — chaosnli_alphanli, m=20 training positions, 50 reference positions

```
               kl_ref         acc_mode         ent_spearman         resid_spearman        modal_mass_spearman        
                 mean     sem     mean     sem         mean     sem           mean    sem                mean     sem
arm                                                                                                                  
hard           0.2652  0.0022   0.7708  0.0030       0.2813  0.0209            NaN    NaN              0.3570  0.0138
smooth         0.2353  0.0028   0.7937  0.0069       0.3026  0.0142            NaN    NaN              0.3720  0.0102
proto          0.2339  0.0027   0.7874  0.0055       0.3162  0.0113            NaN    NaN              0.3762  0.0081
zc             0.2461  0.0047   0.7737  0.0028       0.3170  0.0208            NaN    NaN              0.3872  0.0135
cond           0.2379  0.0045   0.7766  0.0030       0.3299  0.0202            NaN    NaN              0.3929  0.0120
shrunk         0.2401  0.0042   0.7795  0.0037       0.3180  0.0178            NaN    NaN              0.3817  0.0148
soft           0.2407  0.0039   0.7746  0.0044       0.3396  0.0183            NaN    NaN              0.4010  0.0112
soft_pmode     0.2448  0.0034   0.7814  0.0064       0.2796  0.0159            NaN    NaN              0.3610  0.0124
soft_pzc       0.2427  0.0040   0.7729  0.0031       0.3324  0.0187            NaN    NaN              0.3981  0.0108
fidelity_zc    0.1921  0.0103   0.9616  0.0038       0.7737  0.0025          0.339  0.014              0.7761  0.0031
fidelity_soft  0.1228  0.0060   0.9616  0.0038       0.7737  0.0025            NaN    NaN              0.7761  0.0031
```
