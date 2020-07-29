
from astropy.io import ascii
from astropy.table import Table


cols = (
    'DR2Name', '_x', '_y', 'RA_ICRS', 'DE_ICRS', 'Plx', 'e_Plx', 'pmRA',
    'e_pmRA', 'pmDE', 'e_pmDE', 'Gmag', 'e_Gmag', 'BP-RP', 'e_BP-RP')
for file in ('NGC2516', 'NGC2516_19'):
    print(file)
    data = Table.read(file + '.dat', format='ascii')
    filt_data = data[cols]
    ascii.write(filt_data, file + '_filt.dat', format='csv', overwrite=True)
