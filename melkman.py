__author__ = 'flipajs'
import numpy as np
import matplotlib.pyplot as plt

ARROW_DEBUG = False
# set this if you want to save figures from each step
out_dir = None
out_dir = '/Users/flipajs/Dropbox/SCHOOL/3rd_semester/VG/melkman_demo/ex4/'
im_i = 0

def left(v0, v1, v2, debug=True, chain=None, CH=None, i=-1):
    if debug:
        show_step(chain, CH, i, text='left test', wait=False)
        plt.hold(True)
        ax = plt.axes()
        ax.arrow(v0[0], v0[1], 2*(v1[0]-v0[0]), 2*(v1[1]-v0[1]), head_width=0.05, head_length=0.1, fc='r', ec='r', linewidth=3)

        plt.scatter(v2[0], v2[1], color='g', s=150)
        plt.scatter(v0[0], v0[1], color='r', s=100)
        plt.scatter(v1[0], v1[1], color='r', s=100)

        plt.hold(False)
        plt.show()
        draw_im()
        plt.waitforbuttonpress(0)

    # Shewchuk predicate:
    orientation = (v0[0] - v2[0])*(v1[1] - v2[1]) - (v0[1] - v2[1])*(v1[0] - v2[0])
    if orientation <= 0:
        return False
    else:
        return True

def show_step(pts, CH, i, text='', wait=True):
    text += " "+str(CH)
    plt.cla()
    pts = np.array(pts)
    CH = np.array(CH)

    plt.hold(True)

    plt.scatter(pts[:, 0], pts[:, 1], color='b')
    plt.plot(pts[:, 0], pts[:, 1], linewidth=2)

    if -1 < i < len(pts):
        plt.scatter(pts[i, 0], pts[i, 1], color='g', s=300)

    if len(CH):
        plt.scatter(CH[:, 0], CH[:, 1], color='r')
        plt.plot(CH[:, 0], CH[:, 1], color='r')

        plt.scatter(CH[-1, 0], CH[-1, 1], color='r', s=150)

        # ch_h_s = 100
        # # highligh CH points len(CH)-1, len(CH)-2, 0, 1
        # if CH[-1, 0] == CH[0, 0] and CH[-1, 1] == CH[0, 1]:
        #     plt.scatter(CH[0, 0], CH[0, 1], color='R', s=ch_h_s)
        # else:
        #     plt.scatter(CH[-1, 0], CH[-1, 1], color='C', s=ch_h_s)
        #     plt.scatter(CH[0, 0], CH[0, 1], color='M', s=ch_h_s)
        #
        # plt.scatter(CH[-2, 0], CH[-2, 1], color='C', s=50)
        # plt.scatter(CH[1, 0], CH[1, 1], color='M', s=50)

    plt.hold(False)
    plt.title(text)
    plt.grid(True)

    if wait:
        # plt.waitforbuttonpress(0)
        draw_im()

def draw_im():
    global out_dir
    global im_i

    if out_dir:
        im_name = str(im_i)
        while len(im_name) < 3:
            im_name = str(0)+im_name

        plt.savefig(out_dir+im_name+'.png')
        im_i += 1


def melkman(chain):
    """
    Computes convex hull on simple polygonal chain using Melkman's algorithm
    for further details see:
    :param chain: list of points
    :return: list of points - convex hull in CCW order
    """

    # TODO: check for input correctness

    # INIT:
    if left(chain[0], chain[1], chain[2], debug=ARROW_DEBUG, chain=chain, CH=[], i=2):
        CH = [chain[2], chain[0], chain[1], chain[2]]
    else:
        CH = [chain[2], chain[1], chain[0], chain[2]]

    i = 3
    show_step(chain, CH, 2, 'after init')

    while i < len(chain):
        while left(CH[len(CH)-2], CH[len(CH)-1], chain[i], debug=ARROW_DEBUG, chain=chain, CH=CH, i=i) \
                and left(CH[0], CH[1], chain[i], debug=ARROW_DEBUG, chain=chain, CH=CH, i=i):

            show_step(chain, CH, i, 'skipping')
            i += 1

        show_step(chain, CH, i, 'after "skip nodes inside"')
        # RESTORE CONVEXITY:
        while not left(CH[len(CH)-2], CH[len(CH)-1], chain[i], debug=ARROW_DEBUG, chain=chain, CH=CH, i=i):
            CH.pop()
            show_step(chain, CH, i, 'restoring convexity 1...')

        CH.append(chain[i])
        show_step(chain, CH, i, 'after restore convexity 1')

        while not left(chain[i], CH[0], CH[1], debug=ARROW_DEBUG, chain=chain, CH=CH, i=i):
            CH.remove(CH[0])
            show_step(chain, CH, i, 'restoring convexity 2...')

        CH.insert(0, chain[i])
        show_step(chain, CH, i, 'after restore convexity 2')

        i += 1

    return CH

if __name__ == '__main__':
    from examples import example1, example2, example3, example4

    pts = example4

    plt.figure(1)
    plt.ion()

    show_step(pts, [], -1, 'BEFORE INITIALIZATION')
    CH = melkman(pts)

    show_step(pts, CH, -1, 'RESULT')
