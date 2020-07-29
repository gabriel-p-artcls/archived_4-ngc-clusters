# 4-ngc-clusters

NGC2516, NGC2571, NGC6242, NGC2660

<!-- MarkdownTOC levels="1,2" autolink="true" style="ordered" -->

1. [NGC2516](#ngc2516)

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

For the 3x3 field I set the `GUMM_flag` to both `True,False`.
