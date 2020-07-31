
from astropy.table import Table
from astropy import stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def main():
    """
    """
    for i, file in enumerate(('NGC2516_19_filt', 'NGC2516_filt_GUMM',)):
        print(file)

        data = Table.read(file + '.dat', format='ascii')
        # Select members
        msk_memb = data['probs_final'] > .99
        # Estimate PMs+Plx region from estimated members
        pmRA_mean, pmRA_median, pmRA_std = stats.sigma_clipped_stats(
            data['pmRA'][msk_memb], sigma=3, maxiters=5)
        pmDE_mean, pmDE_median, pmDE_std = stats.sigma_clipped_stats(
            data['pmDE'][msk_memb], sigma=3, maxiters=5)
        plx_mean, plx_median, plx_std = stats.sigma_clipped_stats(
            data['Plx'][msk_memb], sigma=3, maxiters=5)

        def sigmaMsk(Nstd):
            msk = (data['pmRA'] > pmRA_mean - Nstd * pmRA_std) &\
                (data['pmRA'] < pmRA_mean + Nstd * pmRA_std) &\
                (data['pmDE'] > pmDE_mean - Nstd * pmDE_std) &\
                (data['pmDE'] < pmDE_mean + Nstd * pmDE_std) &\
                (data['Plx'] > plx_mean - Nstd * plx_std) &\
                (data['Plx'] < plx_mean + Nstd * plx_std)
            return msk

        # Masks for the 1 and 2 sigma stars
        msk_sigma1 = sigmaMsk(1)
        msk_sigma2 = sigmaMsk(2)
        msk_sigma2 = ~msk_sigma1 & msk_sigma2
        msk_sigma3 = sigmaMsk(3)
        msk_sigma3 = ~msk_sigma1 & ~msk_sigma2 & msk_sigma3

        # Plot members estimated by the algorithm
        fld_memb = ~msk_memb
        makePlot(
            data, file, pmRA_mean, pmRA_std, pmDE_mean, pmDE_std, plx_mean,
            plx_std, (msk_memb, ), fld_memb)

        # # Plot 1-2-3 sigma stars
        # file += "_Nstd"
        # msk_memb = (msk_sigma1, msk_sigma2, msk_sigma3)
        # fld_memb = ~msk_sigma1 & ~msk_sigma2 & ~msk_sigma3
        # makePlot(
        #     data, file, pmRA_mean, pmRA_std, pmDE_mean, pmDE_std, plx_mean,
        #     plx_std, msk_memb, fld_memb)


def makePlot(
    data, file, pmRA_mean, pmRA_std, pmDE_mean, pmDE_std, plx_mean, plx_std,
        msk_memb, fld_memb):
    """
    """
    fig = plt.figure(figsize=(15, 15))
    GS = gridspec.GridSpec(3, 3)

    cols, mrk = ('g', 'b', 'purple'), ('o', 's', '^')

    plt.subplot(GS[0])
    for i, msk in enumerate(msk_memb):
        plt.scatter(
            data['_x'][msk], data['_y'][msk], edgecolors=cols[i],
            alpha=.75 - i * .25, marker=mrk[i], s=7, facecolors='none',
            zorder=6 - i * 1)
    plt.scatter(
        data['_x'][fld_memb], data['_y'][fld_memb], c='grey',
        alpha=.1, marker='.', s=2, zorder=1)
    plt.gca().invert_xaxis()
    plt.ylabel("DE")
    plt.xlabel("RA")

    #
    plt.subplot(GS[3])
    plt.title("({:.2f}, {:.2f}) [mas/yr]".format(pmRA_mean, pmDE_mean))
    for i, msk in enumerate(msk_memb):
        plt.scatter(
            data['pmRA'][msk], data['pmDE'][msk], edgecolors=cols[i],
            alpha=.75 - i * .25, marker=mrk[i], facecolors='none',
            zorder=6 - i * 1)
    plt.scatter(
        data['pmRA'][fld_memb], data['pmDE'][fld_memb], c='grey', alpha=.2,
        marker='.', s=3, zorder=1)
    plt.xlim(pmRA_mean - 10. * pmRA_std, pmRA_mean + 10. * pmRA_std)
    plt.ylim(pmDE_mean - 10. * pmDE_std, pmDE_mean + 10. * pmDE_std)
    plt.gca().invert_yaxis()
    plt.ylabel("pmDE")
    plt.xlabel("pmRA")

    #
    plt.subplot(GS[6])
    plt.title("Plx: {:.3f} [mas]".format(plx_mean))
    msk_plx = (data['Plx'] < 5.) & (data['Plx'] > -1.)
    nb = 50
    if len(msk_memb) > 1:
        nb = 5
    for i, msk in enumerate(msk_memb):
        msk1 = msk & msk_plx
        plt.hist(
            data['Plx'][msk1], nb, color=cols[i], alpha=.5, density=True,
            zorder=6)
    msk2 = fld_memb & msk_plx
    plt.hist(data['Plx'][msk2], 50, color='grey', density=True, alpha=.5)
    plt.xlabel("Plx")

    #
    plt.subplot(GS[0:, 1:])
    plt.title("{}".format(file.replace('_filt', '').replace('_GUMM', '')))
    plt.grid(ls=':', lw=.7, zorder=-1)
    lab = ""
    if len(msk_memb) > 1:
        lab = "Nstd={}; "
    for i, msk in enumerate(msk_memb):
        lab2 = lab.format(i + 1) + "N=" + str(msk.sum())
        plt.scatter(
            data['BP-RP'][msk], data['Gmag'][msk], edgecolors=cols[i],
            alpha=.75 - i * .25, marker=mrk[i], facecolors='none',
            zorder=6 - i * 1, label=lab2)
    # Non-members
    plt.scatter(
        data['BP-RP'][fld_memb], data['Gmag'][fld_memb], c='grey', alpha=.25,
        marker='+', zorder=2)

    # This is a bright star identified as a member in the 3x3 deg frame,
    # but not in the 6x6 deg frame.
    if len(msk_memb) == 1:
        if file == "NGC2516_19_filt":
            # Identified as member in the 3x3 field
            st_add = data[data['DR2Name'] == 'Gaia DR2 5293995281966793216']
        else:
            # Identified as member in the 6x6 field
            st_add = data[data['DR2Name'] == 'Gaia DR2 5290847861214655616']
        plt.scatter(
            st_add['BP-RP'], st_add['Gmag'], edgecolors='r',
            alpha=.75, marker='o', facecolors='none', zorder=6)

    plt.legend()
    plt.ylim(3.5, 21.5)
    plt.xlim(-1., 4)
    plt.gca().invert_yaxis()
    plt.ylabel("G")
    plt.xlabel("BP-RP")

    file_out = file + ".png"
    fig.tight_layout()
    plt.savefig(file_out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
