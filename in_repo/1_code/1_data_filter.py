
from astropy.io import ascii
from astropy.table import Table

"""
Remove not used columns from a data file. Makes the file smaller and more
manageable.
"""


cols = (
    'EDR3Name', '_x', '_y', 'RA_ICRS', 'DE_ICRS', 'Plx', 'e_Plx', 'pmRA',
    'e_pmRA', 'pmDE', 'e_pmDE', 'Gmag', 'e_Gmag', 'BP-RP', 'e_BPmag-RPmag')

in_folder = '../0_data/'
out_folder = '../2_pipeline/1_data_filter/out/'
files = ("king11", "ngc2509", "ngc2571", "ngc2660", "ngc6242")
# '_r' for "reduced columns"
out_file = "_r"

for file in files:
    data = Table.read(in_folder + file + '.dat', format='ascii')

    data = data[cols]
    print("{}, total number of stars: {}".format(file, len(data)))
    data.rename_column('e_BPmag-RPmag', 'e_BP-RP')

    # # 2x2 deg square
    # msk = (data['_x'] < 2.) & (data['_x'] > -2.) & (data['_y'] < 2.) &\
    #     (data['_y'] > -2.)
    # data = data[msk]
    # print(len(data))

    # # Mag filter
    # msk = data['Gmag'] < 16
    # data = data[msk]
    # print(len(data))

    ascii.write(data, out_folder + file + out_file + '.dat', format='csv',
                overwrite=True)
