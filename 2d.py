import math
import matplotlib.pyplot as plt
import numpy as np

# initialize 2D flux, P-31 number density, homogeneity
f2d = np.ones((20, 6)) * 1.0
np2_ = np.zeros((20, 6))
h_ = []


def t_up(n_up):
    """
    :param n_up: n-th number of time the sample goes up
    :return: list - the time interval needed for the sample to reach the top with dt=1[s], v=1[cm/s]
    """
    return [tup for tup in range(25+100*n_up, 75+100*n_up)]


def t_down(n_down):
    """
    :param n_down: n-th number of time the sample goes down
    :return: list - the time interval needed for the sample to reach the bottom with dt=1[s], v=1[cm/s]
    """
    return [tdd for tdd in range(75+100*n_down, 125+100*n_down)]


def t_start():
    """
    :return: list - the time interval needed for the sample to reach the bottom from initial t=0[s] with v=1[cm/s]
    """
    return [ts for ts in range(0, 25)]


def get_flux_1d():
    """
    :return: The reactor flux in 1D.
    """
    y = [i for i in range(-35, 36)]
    # hr = 70
    # Sigma (Si-30) = sigma(Si-30)(n,gamma)*N(Si-30)
    sigmaSi30 = 107.2 * 10 ** (-27)
    # nSi30_ = (roSi30*Na)/MSi30
    nSi30_ = (2.33 * 6.02214 * 10 ** 23) / 29.9737701
    sigmaSi30_ = sigmaSi30 * nSi30_
    print(f'sigmaSi30_ = {sigmaSi30_}, nSi30_= {nSi30_}')
    f0 = 10 ** 13
    f1 = []
    for el1 in y:
        f1.append(f0 * sigmaSi30_ * math.cos(math.radians((math.pi * el1) / 70)))
    # print(f'f 1d ] {f1}')
    return f1, sigmaSi30_


# get the flux in 1D and SigmaSi30
f1d, sSi30 = get_flux_1d()

# plt.plot(f)
# plt.show()


def going_down_first_time(ift, jft):
    """
    A function that calculates from initial time till the Si-30 sample reaches the bottom.
    :param ift: highest index of the Si-30 sample on the initial flux indexes scale
    :param jft: lowest index of the Si-30 sample on the initial flux indexes scale
    :return: highest and lowest index of the Si-30 sample on the initial flux indexes scale,
             P-31 number density, homogeneity
    """

    td = t_start()
    y = [i for i in range(1, 6)]
    for el1 in td:
        print(f't={el1} [s], i={ift}, j={jft}')
        for el2 in y:
            np2_[:, 0] = [el1 for i in range(20)]
            np2_[:, el2] = np2_[:, el2] + np.transpose(f1d[ift:jft]) * math.exp(-sSi30 * (el2 - 1))
            if el1 != 0:
                h_.append((max(np2_[:, el2]) - min(np2_[:, el2])) / np.average(np2_[:, el2]))
        ift += 1
        jft += 1
    return ift, jft, np2_, h_


if __name__ == '__main__':

    i1, j1, n, h1_ = going_down_first_time(25, 45)

    # plot Np at final t of the time interval defined above

    # fig = plt.figure(dpi=128, figsize=(10, 10))
    plt.imshow(n[:, 1:])
    plt.tick_params(axis='both', which='major', labelsize=11)
    plt.gca().invert_yaxis()
    plt.title(f'$N_{"{P-31}"}$ at t = {n[-1,0]} s')
    plt.xlabel('dv [cm]')
    plt.ylabel('h [cm]')
    plt.colorbar(pad=0.15)
    plt.xticks(ticks=range(5), labels=range(1, 6))
    plt.yticks(ticks=range(20), labels=range(1, 21))
    plt.show()

    # plt.plot(h_, '-')
    # plt.title(f'H = f (t)')
    # plt.xlabel('time [s]')
    # plt.ylabel('H [/]')
    # plt.grid(which='major', axis='both')
    # plt.show()
