# 4-ngc-clusters

NGC2516, NGC2571, NGC6242, NGC2660

<!-- MarkdownTOC levels="1,2" autolink="true" style="ordered" -->

1. [NGC2516](#ngc2516)
1. [5. IMF](#5-imf)

<!-- /MarkdownTOC -->


## NGC2516

### 1. GAIADR2

Downloaded two fields:

1. A 3x3 deg field with the `GaiaQuery` script.
2. A 6x6 deg field with the `GaiaQuery` script, with a maximum magnitude cut at G=19 mag.

Used the `data_filter.py` script to remove not used columns from the data files.


### 2. Membership

Used the pyUPMASK algorithm in the configuration:

* `Voronoi,rkfunc,Nmembs=25,KDEP_flag=True`

The output files are stored in the `pyUPMASK_out/` folder.


### 3. Filtered files

Used the `members_filter.py` script to isolate the true members. These files are then used for the ASteCA and IMF analysis.

#### NGC2516
Generated the `NGC2516_19_filt_cut.dat` file from the 6x6 deg field processed with pyUPMASK, with the filters:

    msk = (data["probs_final"] > .99) & (data["Gmag"] < 18.5)

This results in a "clean" cluster sequence of ~1800 stars.



### 4. ASteCA

#### NGC2516
The Bayesian parallax analysis (offset +0.029) fails (the chains get stuck) but the weighted average gives a distance modulus of ~8.089 mag (2.411 mas --> 414.8 pc).

Processed with ASteCA using three fundamental parameter ranges (sequentially):

* Large
```
RZ       0.0005  0.0295
RA       7.9     8.5
RE       .0      .3
RV       3.1
RD       7.9     8.2
RM       100     5000
RB         0     1.
```

* Med
```
RZ       0.0014  0.023
RA       8.1     8.5
RE       .0      .3
RV       3.1
RD       7.9      8.2
RM       100     5000
RB         0     1.
```

* Low
```
RZ       0.016   0.02
RA       8.1     8.5
RE       .0      .3
RV       3.1
RD       7.9      8.2
RM       100     5000
RB         0     1.
```

This results (for the "low range" run) in the following fundamental parameters:

* z_mean      z_MAP   z_median     z_mode     z_16th     z_84th      z_std
0.0177992  0.0177147  0.0178767  0.0178715  0.0175785  0.0181642 0.000658595
* a_mean      a_MAP   a_median     a_mode     a_16th     a_84th      a_std
8.22633    8.21135    8.21165    8.21161    8.20943    8.21853
* E_mean      E_MAP   E_median     E_mode     E_16th     E_84th      E_std
0.181366   0.170758   0.178919    0.17315   0.168544   0.196703   0.016049   
* d_mean      d_MAP   d_median     d_mode     d_16th     d_84th      d_std
8.16043    8.16834    8.16787    8.17062    8.13425    8.18853  0.0330314
* M_mean      M_MAP   M_median     M_mode     M_16th     M_84th      M_std
3386.27    3270.91    3361.97    3323.19     3264.0    3533.01    142.825  
* b_mean      b_MAP   b_median     b_mode     b_16th     b_84th      b_std
0.238886   0.235554   0.238032   0.237163   0.203091    0.28167  0.0409509

The binaries mass ratio range is fixed to [0.7, 1.], following [Rubele et al. (2011)](https://academic.oup.com/mnras/article/414/3/2204/1038836):

> The binary fraction is set to a value of 0.3 for binaries with mass ratios in the range between 0.7 and 1.0, which is consistent with the prescriptions for binaries commonly used in works devoted to recover the field SFH in the Magellanic Clouds (e.g. Holtzman et al. 1999; Harris & Zaritsky 2001; Javiel, Santiago & Kerber 2005; Noel et al. 2009). Notice that this assumption is also in agreement with the few determinations of binary fraction for stellar clusters in the LMC (Elson et al. 1998; Hu et al. 2010, both for NGC 1818, a stellar cluster younger than ∼100 Myr).

This might not be the optimal choice, and needs to be properly justified.

The final distance modulus is 8.16 +/- 0.033 mag, reasonably close to the parallax estimate of 8.089 mag.



# 5. IMF

The `IMF` package was used to analyze the clusters' masses and estimate the slope of its IMF. Three fits were performed:

1. Using the single systems (P_binar < 0.5)
2. Using the binary systems (P_binar > 0.5)
3. Using the combined systems (P_binar < 1.)

#### NGC2516
