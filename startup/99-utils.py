#!/usr/bin/python

print(f"Loading {__file__}")

from bluesky.plan_stubs import one_1d_step
from collections import ChainMap
import bluesky.plans as bp
from epics import caget, caput

from lmfit import Model
from scipy.special import erf

import peakutils



# def ps_new(der=False, plot=True):
#     yield from bps.sleep(0.5)
#     uid = list(bec._peak_stats)[0]
#     stats = list(bec._peak_stats[uid])[0]
#     pss = bec._peak_stats[uid][stats]

#     if der:
#         ps.cen = pss.derivative_stats.cen
#         ps.fwhm = pss.derivative_stats.fwhm
#         ps.peak = pss.derivative_stats.max[0]
#         ps.com = pss.derivative_stats.com
#     else:
#         ps.cen = pss.stats.cen
#         ps.fwhm = pss.stats.fwhm
#         ps.peak = pss.stats.max[0]
#         ps.com = pss.stats.com

#     if plot:
#         if der:
#             x = pss.derivative_stats.x
#             y = pss.derivative_stats.y
#         else:
#             x = pss.x_data
#             y = pss.x_data
#         plt.figure()
#         plt.plot([ps.peak, ps.peak], [np.min(y), np.max(y)], "k--", label="PEAK")
#         plt.plot([ps.cen, ps.cen], [np.min(y), np.max(y)], "r-.", label="CEN")
#         plt.plot([ps.com, ps.com], [np.min(y), np.max(y)], "g.-.", label="COM")
#         plt.plot(x, y, "bo-")
#         plt.legend()
#         plt.title(
#             "uid: "
#             + str(uid)
#             + "\n PEAK: "
#             + str(ps.peak)[:8]
#             + str(ps.peak)[:8]
#             + " COM "
#             + str(ps.com)[:8]
#             + "\n FWHM: "
#             + str(ps.fwhm)[:8]
#             + " CEN: "
#             + str(ps.cen)[:8],
#             size=9,
#         )
#         plt.show()


# def ps_new_post(uid=-1, der=False, plot=True):
#     for name, doc in db[uid].documents():
#         bec(name, doc)

#     uid = list(bec._peak_stats)[0]
#     stats = list(bec._peak_stats[uid])[0]
#     pss = bec._peak_stats[uid][stats]

#     if der:
#         x = pss.derivative_stats.x
#         y = pss.derivative_stats.y
#         ps.cen = pss.derivative_stats.cen
#         ps.fwhm = pss.derivative_stats.fwhm
#         ps.peak = pss.derivative_stats.max[0]
#         ps.com = pss.derivative_stats.com
#     else:
#         x = pss.x_data
#         y = pss.x_data
#         ps.cen = pss.stats.cen
#         ps.fwhm = pss.stats.fwhm
#         ps.peak = pss.stats.max[0]
#         ps.com = pss.stats.com

#     if plot:
#         plt.figure()
#         plt.plot([ps.peak, ps.peak], [np.min(y), np.max(y)], "k--", label="PEAK")
#         plt.plot([ps.cen, ps.cen], [np.min(y), np.max(y)], "r-.", label="CEN")
#         plt.plot([ps.com, ps.com], [np.min(y), np.max(y)], "g.-.", label="COM")
#         plt.plot(x, y, "bo-")
#         plt.legend()
#         plt.title(
#             "uid: "
#             + str(uid)
#             + "\n PEAK: "
#             + str(ps.peak)[:8]
#             + str(ps.peak)[:8]
#             + " COM "
#             + str(ps.com)[:8]
#             + "\n FWHM: "
#             + str(ps.fwhm)[:8]
#             + " CEN: "
#             + str(ps.cen)[:8],
#             size=9,
#         )
#         plt.show()


def ps(
    uid=-1,
    det="default",
    suffix="default",
    shift=0.5,
    logplot="off",
    der=False,
    plot=True,
):
    """
    YG Copied from CHX beamline@March 18, 2018
    function to determine statistic on line profile (assumes either peak or erf-profile)
    calling sequence: uid='-1',det='default',suffix='default',shift=.5)
    det='default' -> get detector from metadata, otherwise: specify, e.g. det='eiger4m_single'
    suffix='default' -> _stats1_total / _sum_all, otherwise: specify, e.g. suffix='_stats2_total'
    shift: scale for peak presence (0.5 -> peak has to be taller factor 2 above background)
    """
    # import datetime
    # import time
    # import numpy as np
    # from PIL import Image
    # from databroker import db, get_fields, get_images, get_table
    # from matplotlib import pyplot as pltfrom
    # from lmfit import  Model
    # from lmfit import minimize, Parameters, Parameter, report_fit
    # from scipy.special import erf

    # get the scan information:
    h = db[uid]
    uid = h.start['scan_id']
    if uid == "-1":
        uid = db[-1].start['scan_id']
    if det == "default":
        if h.start['detectors'][0] == "elm" and suffix == "default":
            intensity_field = "elm_sum_all"
        elif h.start['detectors'][0] == "elm":
            intensity_field = "elm" + suffix
        elif suffix == "default":
            intensity_field = h.start['detectors'][0] + "_stats1_total"
        else:
            intensity_field = h.start['detectors'][0] + suffix
    else:
        if det == "elm" and suffix == "default":
            intensity_field = "elm_sum_all"
        elif det == "elm":
            intensity_field = "elm" + suffix
        elif suffix == "default":
            intensity_field = det + "_stats1_total"
        else:
            intensity_field = det + suffix

    field = h.start['motors'][0]
    taken_at = datetime.datetime.fromtimestamp(h.start['time']).strftime('%Y-%m-%d %H:%M:%S')
    #taken_at =  datetime.fromtimestamp(h.start['time']).strftime('%Y-%m-%d %H:%M:%S')
    
    tab = h.table()

    x = tab[field].values
    y = tab[intensity_field].values
    # print(t)
    if der:
        y = np.diff(y)
        x = x[1:]

    PEAK = x[np.argmax(y)]
    PEAK_y = np.max(y)
    COM = np.sum(x * y) / np.sum(y)

    ### from Maksim: assume this is a peak profile:
    def is_positive(num):
        return True if num > 0 else False

    # Normalize values first:
    ym = (y - np.min(y)) / (np.max(y) - np.min(y)) - shift  # roots are at Y=0

    positive = is_positive(ym[0])
    list_of_roots = []
    for i in range(len(y)):
        current_positive = is_positive(ym[i])
        if current_positive != positive:
            list_of_roots.append(
                x[i - 1]
                + (x[i] - x[i - 1]) / (abs(ym[i]) + abs(ym[i - 1])) * abs(ym[i - 1])
            )
            positive = not positive
    if len(list_of_roots) >= 2:
        FWHM = abs(list_of_roots[-1] - list_of_roots[0])
        CEN = list_of_roots[0] + 0.5 * (list_of_roots[1] - list_of_roots[0])
        ps.fwhm = FWHM
        ps.cen = CEN
        # return {
        #    'fwhm': abs(list_of_roots[-1] - list_of_roots[0]),
        #    'x_range': list_of_roots,
    # }
    else:  # ok, maybe it's a step function..
        print("no peak...trying step function...")
        ym = ym + shift

        def err_func(x, x0, k=2, A=1, base=0):  #### erf fit from Yugang
            return base - A * erf(k * (x - x0))

        mod = Model(err_func)
        ### estimate starting values:
        x0 = np.mean(x)
        # k=0.1*(np.max(x)-np.min(x))
        pars = mod.make_params(x0=x0, k=200, A=1.0, base=0.0)
        result = mod.fit(ym, pars, x=x)
        CEN = result.best_values["x0"]
        FWHM = result.best_values["k"]
        ps.cen = CEN
        ps.fwhm = FWHM

    ### re-plot results:
    if plot:
        if logplot == "on":
            plt.close(999)
            plt.figure(999, figsize=(6.4 * 2, 4.8 * 2))
            plt.semilogy([PEAK, PEAK], [np.min(y), np.max(y)], "k--", label="PEAK", lw=2)
            # plt.hold(True)
            plt.semilogy([CEN, CEN], [np.min(y), np.max(y)], "r-.", label="CEN", lw=2)
            plt.semilogy([COM, COM], [np.min(y), np.max(y)], "g.-.", label="COM", lw=2)
            plt.semilogy(x, y, "bo-")
            plt.xlabel(field, fontsize=20, labelpad=15)
            plt.ylabel(intensity_field, fontsize=20, labelpad=15)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.legend(fontsize=20)
            plt.title(
                "uid: "
                + str(uid)
                + " @ "
                + str(taken_at)
                + "\nPEAK: "
                + str(PEAK_y)[:8]
                + " @ "
                + str(PEAK)[:8]
                + "   COM @ "
                + str(COM)[:8]
                + "\n FWHM: "
                + str(FWHM)[:8]
                + " @ CEN: "
                + str(CEN)[:8],
                size=20,
            )
            plt.show()
        else:
            plt.close(999)
            plt.figure(999, figsize=(6.4 * 2, 4.8 * 2))
            plt.plot([PEAK, PEAK], [np.min(y), np.max(y)], "k--", label="PEAK", lw=2)
            # plt.hold(True)
            plt.plot([CEN, CEN], [np.min(y), np.max(y)], "r-.", label="CEN", lw=2)
            plt.plot([COM, COM], [np.min(y), np.max(y)], "g.-.", label="COM", lw=2)
            plt.plot(x, y, "bo-")
            plt.xlabel(field, fontsize=20, labelpad=15)
            plt.ylabel(intensity_field, fontsize=20, labelpad=15)
            plt.legend(fontsize=20)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.title(
                "uid: "
                + str(uid)
                + " @ "
                + str(taken_at)
                + "\nPEAK: "
                + str(PEAK_y)[:8]
                + " @ "
                + str(PEAK)[:8]
                + "   COM @ "
                + str(COM)[:8]
                + "\n FWHM: "
                + str(FWHM)[:8]
                + " @ CEN: "
                + str(CEN)[:8],
                size=20,
            )
            plt.show()

    ### assign values of interest as function attributes:
    ps.peak = PEAK
    ps.com = COM
    # return x, y


def get_incident_angle(db_y, rb_y, Ldet=1599, pixel_size=172):
    """Calculate incident beam angle by putting  direct beam-y pixel, reflected beam-y pixel, and sample-to-detector distance in mm
    Input: db_y: in pixel, rb_y: in pixel, Ldet: in mm
      pixel_size: in  um, defauls 172 um for Pilatus
    """

    return np.degrees(np.arctan2((-rb_y + db_y) * pixel_size * 10 ** (-3), Ldet)) / 2


def plot_1d(scans, x="dsa_x", y="pil1M_stats1_total", grid=True, **kwargs):

    # plt.clf()
    # plt.cla()

    fig = plt.figure(figsize=(8, 5.5))
    ax = fig.add_subplot(111)

    for s in scans:
        h = db[s]
        x_data = h.table()[x]
        y_data = h.table()[y]
        ax.plot(x_data, y_data, label=f"scan_id={h.start['scan_id']}", **kwargs)

    ax.legend()
    if grid:
        ax.grid()
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))



def purge_cryo():
    """
    Copied from CHX
    automatically purge cryo-cooler according to Bruker manual
    pre-requisit: GN2 of 1.5<p<3.0 bar connected to V21
    AND cryo-control NOT disabled, e.g. by EPS
    calling sequence: purge_cryo()
    LW 05/27/2018
    """

    print('start purging cryo-cooler')
    print('Please make sure: \n 1) GN2 of 1.5<p<3.0 bar connected to V21 \n 2) cryo-control NOT disabled, e.g. by EPS')
    #print('going to check EPS status:')
    #if caget('XF:12ID-OP{Cryo:1}Enbl-Sts') == 1:
    #    print('cryo-cooler operations are enabled!')
    #else: raise cryo_Exception('error: cryo-cooler operations not enabled by EPS')
    print('going to close all valves....')
    caput('XF:12ID-UT{Cryo:1-IV:21}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:09}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:19}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:15}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:20}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:10}Pos-SP', 0)
    caput('XF:12ID-UT{Cryo:1-IV:11}Pos-SP', 0)
    caput('XF:12ID-UT{Cryo:1-IV:17_35}Cmd:Cls-Cmd', 1) #V17.2
    caput('XF:12ID-UT{Cryo:1-IV:17_100}Cmd:Cls-Cmd', 1)  #V17.1
    print('purging step 1/3, taking 30 min \n current time: '+str(datetime.datetime.now()))
    caput('XF:12ID-UT{Cryo:1-IV:20}Cmd:Opn-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:09}Cmd:Opn-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:10}Pos-SP', 100)
    caput('XF:12ID-UT{Cryo:1-IV:21}Cmd:Opn-Cmd', 1)
    for i in range(6):
        print('time left on purging step 1/3: '+str(30-i*5)+'min \n')
        yield from bps.sleep(300)
    print('purging step 1/3 complete....proceeding to 2/3!')
    caput('XF:12ID-UT{Cryo:1-IV:09}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:11}Pos-SP', 100)
    print('purging step 2/3, taking 15 min \n current time: '+str(datetime.datetime.now()))
    for i in range(3):
       print('time left on purging step 2/3: '+str(15-i*5)+'min \n')
       yield from bps.sleep(300)
    print('purging step 2/3 complete....proceeding to 3/3!')
    caput('XF:12ID-UT{Cryo:1-IV:11}Pos-SP', 0)
    caput('XF:12ID-UT{Cryo:1-IV:17_35}Cmd:Opn-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:17_100}Cmd:Opn-Cmd', 1)
    print('purging step 3/3, taking 15 min \n current time: '+str(datetime.datetime.now()))
    for i in range(3):
       print('time left on purging step 3/3: '+str(15-i*5)+'min \n')
       yield from bps.sleep(300)
    print('purging COMPLETE! Closing all valves...')
    caput('XF:12ID-UT{Cryo:1-IV:21}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:17_35}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:17_100}Cmd:Cls-Cmd', 1)
    caput('XF:12ID-UT{Cryo:1-IV:10}Pos-SP', 0)
    caput('XF:12ID-UT{Cryo:1-IV:20}Cmd:Cls-Cmd', 1)

def get_scan_md(tender=False):
    """
    Create a string with scan metadata
    """
    # Metadata
    e = energy.position.energy / 1000
    #temp = str(np.round(float(temp_degC), 1)).zfill(5)
    wa = waxs.arc.position + 0.001
    wa = str(np.round(float(wa), 1)).zfill(4)
    sdd = pil1m_pos.z.position / 1000

    md_fmt = ("_{energy}keV_wa{wa}_sdd{sdd}m")

    if tender:
        scan_md = md_fmt.format(
            energy = "%.5f" % e ,
            wa = wa,
            sdd = "%.1f" % sdd,
        )
    else:
        scan_md = md_fmt.format(
            energy = "%.2f" % e ,
            wa = wa,
            sdd = "%.1f" % sdd,
        )
    return scan_md

def get_more_md(tender=True, bpm=True):
    """
    Add XBPM2 readings into the scan metadata
    """

    more_md = f'{get_scan_md(tender=tender)}'

    if bpm:
        xbpm = xbpm2.sumX.get()
        xbpm = str(np.round(float(xbpm), 3)).zfill(5)
        more_md = f'{more_md}_xbpm{xbpm}'

    return more_md

