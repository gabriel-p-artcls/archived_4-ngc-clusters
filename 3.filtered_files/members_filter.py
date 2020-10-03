
from astropy.io import ascii
from astropy.table import Table

# fname = "NGC2660_filt.dat"
fname = "NGC2516_19_filt.dat"
data = Table.read("../2.membership/pyUPMASK_out/" + fname, format='ascii')
# msk = data["Gmag"] < 18
msk = (data["probs_final"] > .99) & (data["Gmag"] < 18.5)
fout = fname.replace('.dat', '_cut.dat')
ascii.write(data[msk], fout, format='csv', overwrite=True)
