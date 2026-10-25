# probe_nominal — chaosnli_mnli, m=10 training positions, 50 reference positions

```
             kl_ref     acc_mode     ent_spearman     resid_spearman     modal_mass_spearman    
               mean sem     mean sem         mean sem           mean sem                mean sem
arm                                                                                             
hard         0.2244 NaN   0.6875 NaN       0.1799 NaN         0.1644 NaN              0.3657 NaN
smooth       0.2053 NaN   0.6979 NaN       0.2005 NaN         0.3605 NaN              0.3657 NaN
proto        0.1742 NaN   0.6771 NaN       0.2665 NaN         0.4863 NaN              0.3624 NaN
zc           0.1699 NaN   0.7042 NaN       0.2989 NaN         0.4879 NaN              0.4060 NaN
cond         0.1671 NaN   0.6833 NaN       0.3256 NaN         0.5084 NaN              0.4184 NaN
shrunk       0.1579 NaN   0.7125 NaN       0.3202 NaN         0.5282 NaN              0.4069 NaN
soft         0.1580 NaN   0.7208 NaN       0.3347 NaN         0.5238 NaN              0.4178 NaN
soft_pmode   0.1846 NaN   0.6750 NaN       0.2324 NaN         0.4742 NaN              0.3519 NaN
soft_pzc     0.1775 NaN   0.6833 NaN       0.2576 NaN         0.4996 NaN              0.3619 NaN
oracle_zc    0.2997 NaN   0.7917 NaN       0.5093 NaN         0.4255 NaN              0.6013 NaN
oracle_soft  0.4338 NaN   0.7979 NaN       0.5169 NaN         0.5953 NaN              0.6096 NaN
```
