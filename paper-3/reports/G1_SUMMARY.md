# G1 pool adaptation — summary (RPS; vs none = arm − none, negative is better; gap = none − oracle-B, positive = a pool shift the head trained on A did not capture)

```
        panel             var                                      poolB  nA  nB   none     gap  gap_sem  map-B(20)  map-B(50)  map-B(all)  dir-B(50)  dir-B(all)  recover_map50  recover_dir50  map_minus_dir_all
           bw           group                                      cs101  43  10 0.1716  0.0072   0.0014     0.0076    -0.0012     -0.0019    -0.0029     -0.0032         0.1650         0.4081             0.0013
           bw           group                        cs216-Prog_Data_Rep  43  22 0.1607 -0.0058   0.0013     0.0003     0.0057      0.0037    -0.0006     -0.0000            NaN            NaN             0.0037
           bw           group                                   cs414-OS  43  18 0.1621 -0.0013   0.0008     0.0022     0.0039      0.0035    -0.0005     -0.0008            NaN            NaN             0.0043
           bw           group                       cs445-Intro_Graphics  43  13 0.1627  0.0003   0.0010     0.0009     0.0024      0.0021    -0.0004     -0.0009        -7.0538         1.1209             0.0030
           bw          random                                     random  60  61 0.1656 -0.0013   0.0010     0.0013     0.0025      0.0012     0.0003     -0.0022            NaN            NaN             0.0034
        dices          random                                     random  52  52 0.2227  0.0021   0.0012    -0.0024     0.0012     -0.0035    -0.0001     -0.0038        -0.5929         0.0283             0.0003
        dices       rater_age                                     gen x+  49  27 0.2306 -0.0002   0.0013    -0.0035    -0.0012     -0.0035    -0.0037     -0.0042            NaN            NaN             0.0007
        dices       rater_age                                  millenial  49  28 0.2160 -0.0003   0.0010     0.0004     0.0073     -0.0006     0.0021     -0.0010            NaN            NaN             0.0004
        dices rater_education                       High school or below  64  33 0.2303 -0.0008   0.0018    -0.0008     0.0014     -0.0030    -0.0016     -0.0024            NaN            NaN            -0.0007
        dices    rater_gender                                        Man  57  47 0.2210  0.0000   0.0007    -0.0011     0.0013     -0.0027    -0.0013     -0.0030            NaN            NaN             0.0003
        dices      rater_race                   Asian/Asian subcontinent  25  21 0.2364  0.0045   0.0015    -0.0045    -0.0035     -0.0080    -0.0054     -0.0081         0.7631         1.1957             0.0000
        dices      rater_race                     Black/African American  25  23 0.2207  0.0018   0.0009    -0.0029     0.0005     -0.0040    -0.0007     -0.0039        -0.2727         0.3742            -0.0001
        dices      rater_race LatinX, Latino, Hispanic or Spanish Origin  25  22 0.2273  0.0079   0.0013    -0.0006     0.0007     -0.0052     0.0009     -0.0015        -0.0837        -0.1091            -0.0037
        dices      rater_race                                Multiracial  25  13 0.2622  0.0179   0.0009    -0.0120    -0.0191     -0.0234    -0.0161     -0.0185         1.0649         0.8995            -0.0049
     dices990          random                                     random  86  86 0.1933  0.0025   0.0007     0.0006     0.0032     -0.0021     0.0025     -0.0008        -1.2972        -1.0286            -0.0013
     dices990       rater_age                                     gen x+  98  43 0.1788  0.0005   0.0004     0.0007     0.0041      0.0013     0.0023      0.0006        -8.6270        -4.7616             0.0006
     dices990       rater_age                                      gen z  98  31 0.2083  0.0011   0.0004     0.0013     0.0019     -0.0024     0.0016      0.0000        -1.8321        -1.5437            -0.0024
     dices990 rater_education                       High school or below 152  20 0.1717  0.0029   0.0005     0.0010     0.0015     -0.0017    -0.0002     -0.0011        -0.5369         0.0856            -0.0006
     dices990    rater_gender                                        Man  88  82 0.1952  0.0004   0.0002     0.0009     0.0065     -0.0002     0.0029     -0.0006       -14.9626        -6.7391             0.0004
     dices990    rater_locale                                         US  92  80 0.1824  0.0160   0.0007    -0.0108    -0.0105     -0.0154    -0.0046     -0.0098         0.6527         0.2863            -0.0055
     dices990      rater_race                   Asian/Asian subcontinent  65  53 0.2030  0.0082   0.0003    -0.0046    -0.0043     -0.0079    -0.0037     -0.0060         0.5233         0.4513            -0.0019
     dices990      rater_race                     Black/African American  65  11 0.2210  0.0104   0.0003    -0.0056    -0.0054     -0.0119    -0.0060     -0.0093         0.5228         0.5766            -0.0026
     dices990      rater_race LatinX, Latino, Hispanic or Spanish Origin  65  16 0.1708  0.0446   0.0018    -0.0328    -0.0430     -0.0452    -0.0133     -0.0171         0.9637         0.2988            -0.0281
     dices990      rater_race                                      White  65  27 0.1752  0.0352   0.0006    -0.0253    -0.0306     -0.0352    -0.0110     -0.0150         0.8693         0.3119            -0.0202
popquorn_off8             age                                      18-24  36  31 0.1301  0.0081   0.0009     0.0015    -0.0014     -0.0040     0.0041      0.0041         0.1778        -0.5073            -0.0081
popquorn_off8             age                                      25-29  36  25 0.1205  0.0058   0.0010    -0.0021    -0.0060     -0.0062     0.0005     -0.0008         1.0288        -0.0876            -0.0054
popquorn_off8             age                                      30-34  36  30 0.1314  0.0035   0.0010    -0.0039    -0.0076     -0.0102    -0.0060     -0.0072         2.2050         1.7199            -0.0030
popquorn_off8             age                                      35-39  36  31 0.1267  0.0069   0.0013    -0.0049    -0.0092     -0.0109     0.0016     -0.0023         1.3416        -0.2334            -0.0086
popquorn_off8             age                                      40-44  36  23 0.1422 -0.0039   0.0008    -0.0007     0.0004     -0.0017    -0.0006     -0.0010            NaN            NaN            -0.0007
popquorn_off8             age                                      45-49  36  22 0.1278 -0.0070   0.0010    -0.0013    -0.0002     -0.0028     0.0017     -0.0009            NaN            NaN            -0.0019
popquorn_off8             age                                      50-54  36  20 0.1328 -0.0112   0.0022    -0.0002     0.0033      0.0027     0.0031      0.0034            NaN            NaN            -0.0007
popquorn_off8             age                                      60-64  36  15 0.1570 -0.0063   0.0018     0.0031    -0.0021     -0.0030     0.0006      0.0013            NaN            NaN            -0.0042
popquorn_off8             age                                        >65  36  29 0.1466 -0.0032   0.0013     0.0017     0.0007     -0.0011     0.0051      0.0039            NaN            NaN            -0.0050
popquorn_off8       education                            Graduate degree 121  50 0.1495 -0.0022   0.0008     0.0010     0.0004     -0.0010     0.0020      0.0009            NaN            NaN            -0.0019
popquorn_off8       education          High school diploma or equivalent 121  80 0.1253  0.0008   0.0005    -0.0002     0.0022     -0.0008     0.0021      0.0002        -2.7088        -2.6452            -0.0011
popquorn_off8          gender                                        Man 131 124 0.1307 -0.0011   0.0002     0.0011     0.0038      0.0002     0.0037      0.0007            NaN            NaN            -0.0005
popquorn_off8      occupation                                  Homemaker 127  12 0.1275 -0.0064   0.0012     0.0004     0.0049      0.0027     0.0036      0.0019            NaN            NaN             0.0008
popquorn_off8      occupation                                    Retired 127  29 0.1338 -0.0052   0.0008    -0.0005     0.0001     -0.0024     0.0045      0.0012            NaN            NaN            -0.0037
popquorn_off8      occupation                              Self-employed 127  34 0.1304 -0.0053   0.0007    -0.0004     0.0024     -0.0007     0.0008     -0.0003            NaN            NaN            -0.0004
popquorn_off8      occupation                                    Student 127  20 0.1252 -0.0090   0.0007     0.0012     0.0027      0.0013     0.0027      0.0011            NaN            NaN             0.0002
popquorn_off8      occupation                                 Unemployed 127  34 0.1190 -0.0048   0.0009    -0.0019     0.0031     -0.0001     0.0005      0.0009            NaN            NaN            -0.0010
popquorn_off8          random                                     random 131 131 0.1300  0.0005   0.0003     0.0012     0.0030      0.0001     0.0036      0.0007        -6.2932        -7.7473            -0.0006
popquorn_pol5       education                            Graduate degree 237  97 0.1378 -0.0041   0.0007     0.0001     0.0026      0.0001     0.0021      0.0011            NaN            NaN            -0.0011
popquorn_pol5       education          High school diploma or equivalent 237 151 0.1333 -0.0005   0.0004    -0.0010     0.0014     -0.0019     0.0018      0.0003            NaN            NaN            -0.0022
popquorn_pol5       education                                      Other 237  11 0.1083 -0.0310   0.0013     0.0009     0.0051      0.0029     0.0006     -0.0002            NaN            NaN             0.0031
popquorn_pol5          gender                                        Man 254 236 0.1355  0.0013   0.0003     0.0001     0.0005     -0.0021    -0.0000     -0.0013        -0.3519         0.0217            -0.0008
popquorn_pol5          gender                                 Non-binary 254  13 0.1282 -0.0200   0.0016    -0.0012    -0.0014     -0.0024     0.0008     -0.0002            NaN            NaN            -0.0022
popquorn_pol5          random                                     random 253 253 0.1321 -0.0000   0.0002    -0.0001     0.0024     -0.0006     0.0011      0.0001            NaN            NaN            -0.0006
```
