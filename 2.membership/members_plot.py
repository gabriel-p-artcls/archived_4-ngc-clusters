
import numpy as np
from astropy.table import Table
from astropy import stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def main(min_prob_cut=.99, sigmaplot_flag=False, Nsigmas=1):
    """
    Process the files with the added 'probs_final' column, obtained using the
    'Voronoi' clustering algorithm and the 'rkfunc' rejection method, in
    pyUPMASK.
    """

    clust_lst = ('NGC2516_19_filt',)
    for i, file in enumerate(clust_lst):
        print(file)

        data = Table.read("pyUPMASK_out/" + file + '.dat', format='ascii')
        # Select members
        msk_memb = data['probs_final'] > min_prob_cut
        # Estimate PMs+Plx region from estimated members
        pmRA_mean, pmRA_median, pmRA_std = stats.sigma_clipped_stats(
            data['pmRA'][msk_memb], sigma=3, maxiters=5)
        pmDE_mean, pmDE_median, pmDE_std = stats.sigma_clipped_stats(
            data['pmDE'][msk_memb], sigma=3, maxiters=5)
        plx_mean, plx_median, plx_std = stats.sigma_clipped_stats(
            data['Plx'][msk_memb], sigma=3, maxiters=5)

        if not sigmaplot_flag:
            # Plot members estimated by the algorithm
            fld_memb = ~msk_memb
            makePlot(
                data, file, pmRA_mean, pmRA_std, pmDE_mean, pmDE_std, plx_mean,
                plx_std, (msk_memb, ), fld_memb)

        else:
            def sigmaMsk(Nstd):
                msk = (data['pmRA'] > pmRA_mean - Nstd * pmRA_std) &\
                    (data['pmRA'] < pmRA_mean + Nstd * pmRA_std) &\
                    (data['pmDE'] > pmDE_mean - Nstd * pmDE_std) &\
                    (data['pmDE'] < pmDE_mean + Nstd * pmDE_std) &\
                    (data['Plx'] > plx_mean - Nstd * plx_std) &\
                    (data['Plx'] < plx_mean + Nstd * plx_std)
                return msk

            # # Masks for the 1 and 2 sigma stars
            # msk_sigma1 = sigmaMsk(1)
            # msk_sigma2 = sigmaMsk(2)
            # msk_sigma3 = sigmaMsk(3)

            msk_memb = []
            for Ns in range(Nsigmas):
                msk_sigma = sigmaMsk(Ns + 1)
                if Ns == 1:
                    msk_sigma = ~msk_memb[0] & msk_sigma
                if Ns == 2:
                    msk_sigma = ~msk_memb[0] & ~msk_memb[1] & msk_sigma
                msk_memb.append(msk_sigma)

            # Plot 1-2-3 sigma stars
            file += "_Nstd"
            # msk_memb = (msk_sigma1, msk_sigma2, msk_sigma3)
            # fld_memb = ~msk_sigma1 & ~msk_sigma2 & ~msk_sigma3
            fld_memb = np.logical_and.reduce([~msk for msk in msk_memb])
            makePlot(
                data, file, pmRA_mean, pmRA_std, pmDE_mean, pmDE_std, plx_mean,
                plx_std, msk_memb, fld_memb)


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

    # VPD
    plt.subplot(GS[3])
    plt.title(r"PMs: ({:.2f}$\pm${:.2f}, {:.2f}$\pm${:.2f}) [mas/yr]".format(
        pmRA_mean, pmRA_std, pmDE_mean, pmDE_std))
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
    plt.ylabel(r"$\mu_{\delta}$")
    plt.xlabel(r"$\mu_{\alpha} \cos \delta$")

    #
    plt.subplot(GS[6])
    plt.title(r"Plx: {:.3f}$\pm${:.2f} [mas]".format(plx_mean, plx_std))
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
    plt.axvline(plx_mean, c="r", ls=":", lw=1.5, zorder=6)
    xmin, xmax = max(-1., plx_mean - 5. * plx_std),\
        min(5., plx_mean + 10. * plx_std)
    plt.xlim(xmin, xmax)
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
    xmin, xmax = data['BP-RP'][msk].min(), data['BP-RP'][msk].max()
    ymin, ymax = data['Gmag'][msk].min(), data['Gmag'][msk].max()
    plt.ylim(ymax + .25, ymin - 1.)
    plt.xlim(xmin - .5, xmax + .5)

    # # For NGC2516
    # # This is a bright star identified as a member in the 3x3 deg frame,
    # # but not in the 6x6 deg frame.
    # if len(msk_memb) == 1:
    #     if file == "NGC2516_19_filt":
    #         # Identified as member in the 3x3 field
    #         st_add = data[data['DR2Name'] == 'Gaia DR2 5293995281966793216']
    #     else:
    #         # Identified as member in the 6x6 field
    #         st_add = data[data['DR2Name'] == 'Gaia DR2 5290847861214655616']
    #     plt.scatter(
    #         st_add['BP-RP'], st_add['Gmag'], edgecolors='r',
    #         alpha=.75, marker='o', facecolors='none', zorder=6)
    # plt.ylim(3.5, 21.5)
    # plt.xlim(-1., 4)

    plt.legend()
    # plt.gca().invert_yaxis()
    plt.ylabel("G")
    plt.xlabel("BP-RP")

    file_out = file + ".png"
    fig.tight_layout()
    plt.savefig(file_out, dpi=150, bbox_inches='tight')


if __name__ == '__main__':
    main()
