print(f"Loading {__file__}")

import matplotlib.pyplot as plt
import bluesky.plan_stubs as bps
import bluesky.plans as bp
from smibase.manipulators import prs, piezo, stage
from .pilatus import pil2M
from .config import sample_id
from .pilatus import det_exposure_time
from .utils import ps
from IPython import get_ipython
from .beam import SMI as smi

# Get the bluesky callback
bec = get_ipython().user_ns['bec']


def align_gisaxs_height(rang=0.3, point=31, der=False):
    """
    Align GISAXS height using a relative scan.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], piezo.y, -rang, rang, point)
    ps(der=der, plot=False)
    yield from bps.mv(piezo.y, ps.cen)



def align_bdm_height(rang=0.3, point=31, der=False):
    """
    Align BDM height using a relative scan.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], bdm.y, -rang, rang, point)
    ps(der=der, plot=False)
    print(f'Moving to halfcut at {ps.peak}')
    yield from bps.mv(bdm.y, ps.cen)



def align_gisaxs_height_rb(rang=0.3, point=31, der=False):
    """
    Align GISAXS height on the reflected beam.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], piezo.y, -rang, rang, point)
    ps(der=der, plot=False)
    yield from bps.mv(piezo.y, ps.peak)



def align_bdm_height_rb(rang=0.3, point=31, der=False):
    """
    Align BDM height on the reflected beam.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], bdm.y, -rang, rang, point)
    ps(der=der, plot=False)
    print(f'Moving to peak position at {ps.peak}')
    yield from bps.mv(bdm.y, ps.peak)


def align_gisaxs_th(rang=0.3, point=31):
    """
    Align GISAXS theta using a relative scan.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
    """
    yield from bp.rel_scan([pil2M], piezo.th, -rang, rang, point)
    ps(plot=False)
    yield from bps.mv(piezo.th, ps.peak)



def align_bdm_th(rang=0.3, point=31):
    """
    Align BDM theta using a relative scan.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
    """
    yield from bp.rel_scan([pil2M], bdm.th, -rang, rang, point)
    ps(plot=False)
    print(f'Moving to peak position at {ps.peak}')
    yield from bps.mv(bdm.th, ps.peak)


def align_xrr_prs(rang=0.3, point=31):
    """
    Align XRR using the prs stage.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
    """
    yield from bp.rel_scan([pil2M], prs, -rang, rang, point)
    ps(plot=False)
    yield from bps.mv(prs, ps.peak)


def align_xrr_height(rang=0.3, point=31, der=False):
    """
    Align XRR height using a relative scan.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], piezo.z, -rang, rang, point)
    ps(der=der, plot=False)
    yield from bps.mv(piezo.z, ps.peak)


def align_xrr_height_motx(rang=0.3, point=31, der=False):
    """
    Align XRR height using the piezo.x motor.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], piezo.x, -rang, rang, point)
    ps(der=der, plot=False)
    yield from bps.mv(piezo.x, ps.peak)


def align_gisaxs_height_hex(rang=0.3, point=31, der=False):
    """
    Align GISAXS height using the hexapod stage.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
        der (bool): Whether to calculate the derivative.
    """
    yield from bp.rel_scan([pil2M], stage.y, -rang, rang, point)
    ps(der=der, plot=False)
    yield from bps.mv(stage.y, ps.cen)


def align_gisaxs_th_hex(rang=0.3, point=31):
    """
    Align GISAXS theta using the hexapod stage.

    Parameters:
        rang (float): Range for the scan.
        point (int): Number of points in the scan.
    """
    yield from bp.rel_scan([pil2M], stage.th, -rang, rang, point)
    ps(plot=False)
    yield from bps.mv(stage.th, ps.peak)


def alignment_gisaxs(angle=0.15):
    """
    Regular alignment routine for GISAXS and GIWAXS. First, scan the sample height and incident angle on the direct beam.
    Then scan the incident angle, height, and incident angle again on the reflected beam.

    Parameters:
        angle (float): Angle at which the alignment on the reflected beam will be done.
    """
    

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(800, 21, der=True)
    yield from align_gisaxs_th(1.5, 27)

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th(0.2, 21)
    yield from align_gisaxs_height_rb(150, 16)
    yield from align_gisaxs_th(0.1, 31)  # was .025, 21 changed to .1 31

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, piezo.th.position-angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False

def alignement_gisaxs_doblestack(angle=0.15):
    """
    Modification of teh regular alignement routine for the doble-stack. Since top row is out of the center of rotation of of theta, the alignement on teh direc does not work.
    Therefore, only teh height is aligned on the direct beam but the incident angle is aligned on the reflected beam with a small incident angle.
    The alignement on the reflected beam is the same as for regular alignement.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """
    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan height on the DB only
    yield from align_gisaxs_height(800, 21, der=True)

    # alignement of incident angle at ai = 0.1 deg so the alignement use the reflected roi not sitting on the db position
    yield from smi.setReflectedBeamROI(total_angle=0.1, technique="gisaxs")
    yield from align_gisaxs_th(0.9, 60)  # was 1.5 27

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak -0.1 + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th(0.2, 21)
    yield from align_gisaxs_height_rb(150, 16)
    yield from align_gisaxs_th(0.1, 21)  # changed from .025 to .1)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False



def alignement_gisaxs_rough(angle=0.15):
    """
    Modification of teh regular alignement routine for the doble-stack. Since top row is out of the center of rotation of of theta, the alignement on teh direc does not work.
    Therefore, only teh height is aligned on the direct beam but the incident angle is aligned on the reflected beam with a small incident angle.
    The alignement on the reflected beam is the same as for regular alignement.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """
    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan height on the DB only
    yield from align_gisaxs_height(800, 21, der=True)
    yield from align_gisaxs_th(2.0, 40)  # was 1.5 27

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False



def alignement_gisaxs_multisample(angle=0.15):
    """
    This is design to align several samples at the same time. The attenuators, bs motion, ... needs to be done outside of this maccro, so there is no back and forth in term
    of motor motion from sample to sample.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """
    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    # yield from smi.modeAlignment(technique='gisaxs')

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(700, 16, der=True)
    yield from align_gisaxs_th(1, 15)
    yield from align_gisaxs_height(300, 11, der=True)
    yield from align_gisaxs_th(0.5, 16)

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th(0.2, 31)
    yield from align_gisaxs_height_rb(150, 21)
    yield from align_gisaxs_th(0.025, 21)  # changed from .025 to .1 on 3-38-22

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    # yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def alignement_gisaxs_hex(angle=0.1, rough_y=0.5):
    """
    Regular alignement routine for gisaxs and giwaxs using the hexapod. First, scan of the sample height
    and incident angle on the direct beam.
    Then scan of teh incident angle, height and incident angle again on the reflected beam.

    Params:
            angle (float): angle at which the alignement on the reflected beam will be done,
            rough_y (float): range in hexapod stage y for rough alignment.

    """


    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height_hex(rough_y, 21, der=True)

    yield from smi.setReflectedBeamROI(total_angle=0.1, technique="gisaxs")
    yield from align_gisaxs_th_hex(0.5, 31)

    # move to theta 0 + value
    yield from bps.mv(stage.th, ps.peak -0.1 + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th_hex(0.3, 31)
    yield from align_gisaxs_height_hex(0.15, 26)
    yield from align_gisaxs_th_hex(0.05, 21)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(stage.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def alignement_gisaxs_hex_roughsample(angle=0.1):
    """
    Regular alignement routine for gisaalign_xrr_prsxs and giwaxs using the hexapod. First,
    scan of the sample height and incident angle on the direct beam. Then scan
    of teh incident angle, height and incident angle again on the reflected beam.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height_hex(0.5, 15, der=True)
    yield from align_gisaxs_th_hex(0.5, 21)
    yield from align_gisaxs_height_hex(0.2, 25, der=True)
    yield from align_gisaxs_th_hex(0.2, 21)
    # # move to theta 0 + value
    # yield from bps.mv(stage.th, ps.peak + angle)

    # # Set reflected ROI
    # yield from smi.setReflectedBeamROI(total_angle=angle, technique='gisaxs')

    # yield from bps.mv(att2_10.open_cmd, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(att2_10.open_cmd, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(att2_9.open_cmd, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(att2_9.open_cmd, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(att2_11.close_cmd, 1)
    # yield from bps.sleep(1)
    # yield from bps.mv(att2_11.close_cmd, 1)
    # # Scan theta and height
    # #yield from align_gisaxs_th_hex(0.3, 21)
    # yield from align_gisaxs_height_hex(0.08, 21)
    # #yield from align_gisaxs_th_hex(0.05, 21)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    #      yield from bps.mvr(stage.th, -angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def alignement_gisaxs_hex_short(angle=0.12):
    """
    Short alignement routine for gisaxs and giwaxs using the hexapod. First, scan of the sample height and incident angle on the direct beam.
    Then scan of teh incident angle, height and incident angle again on the reflected beam.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment()

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height_hex(0.500, 21, der=True)

    # move to theta 0 + value
    yield from bps.mvr(stage.th, angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle)

    # Scan theta and height
    yield from align_gisaxs_th_hex(0.7, 23)
    yield from align_gisaxs_height_hex(0.15, 31)
    yield from align_gisaxs_th_hex(0.06, 25)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(stage.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def quickalign_gisaxs(angle=0.15):
    """
    Short alignement with only alignement on the reflected beam.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True
    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment()

    # move to theta 0 + value
    yield from bps.mvr(piezo.th, angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle)

    # Scan theta and height
    yield from align_gisaxs_height_rb(200, 31)
    yield from align_gisaxs_th(0.1, 21)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, ps.cen - angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


def alignement_xrr(angle=0.15):
    """
    This routine is for samples mounted at 90 degrees, so the alignement is done using prs stage as incident angle and piezo.x as height

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    yield from smi.modeAlignment(technique="xrr")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI(technique="xrr")

    # Scan theta and height
    yield from align_xrr_height(800, 16, der=True)

    # For XRR alignment, a poor results was obtained at incident angle 0. To improve the alignment success
    # the prs alignment is done at an angle of 0.15 deg
    yield from smi.setReflectedBeamROI(total_angle=-0.15, technique="xrr")
    yield from align_xrr_prs(1, 20)
    yield from bps.mv(prs, ps.peak + 0.15)


    yield from smi.setDirectBeamROI()
    yield from align_xrr_height(500, 13, der=True)

    yield from smi.setReflectedBeamROI(total_angle=-0.15, technique="xrr")
    yield from align_xrr_prs(0.5, 21)
    yield from bps.mv(prs, ps.peak + 0.15)

    # move to theta 0 + value
    yield from bps.mv(prs, (ps.peak + 0.15) - angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="xrr")

    # Scan theta and height
    yield from align_xrr_prs(0.2, 31)
    yield from align_xrr_height(200, 21)
    yield from align_xrr_prs(0.05, 21)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(prs, ps.cen + angle)
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False




def alignement_xrr_xmotor(angle=0.15):
    """
    This routine is for samples mounted at 90 degrees, so the alignement is done using prs stage as incident angle and piezo.x as height

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.5, 0.5)

    yield from smi.modeAlignment(technique="xrr")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI(technique="xrr")

    # Scan theta and height
    yield from align_xrr_height_motx(1000, 31, der=True)

    # For XRR alignment, a poor results was obtained at incident angle 0. To improve the alignment success
    # the prs alignment is done at an angle of 0.15 deg
    yield from smi.setReflectedBeamROI(total_angle=-0.15, technique="xrr")
    yield from align_xrr_prs(3, 60)

    yield from smi.setDirectBeamROI()
    yield from align_xrr_height_motx(500, 13, der=True)

    yield from smi.setReflectedBeamROI(total_angle=-0.15, technique="xrr")
    yield from align_xrr_prs(0.5, 21)
    yield from bps.mv(prs, ps.peak + 0.15)

    # move to theta 0 = (ps.peak + 0.15) + value
    yield from bps.mv(prs, (ps.peak + 0.15) - angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=-angle, technique="xrr")

    # Scan theta and height
    yield from align_xrr_prs(0.2, 31)
    yield from align_xrr_height_motx(200, 21)
    yield from align_xrr_prs(0.05, 21)

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(prs, ps.cen + angle) # finish the alignment at 0
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False






def alignement_gisaxs_short(angle=0.15):
    """
    Regular alignement routine for gisaxs and giwaxs. First, scan of the sample height and incident angle on the direct beam.
    Then scan of teh incident angle, height and incident angle again on the reflected beam.

    param angle: np.float. Angle at which the alignement on the reflected beam will be done

    """

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(800, 21, der=True)
    yield from align_gisaxs_th(1.5, 27)

    yield from align_gisaxs_height(800, 21, der=True)
    yield from align_gisaxs_th(1.5, 27)
    
    # Close all the matplotlib windows
    plt.close("all")
    yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False


import time
import numpy as np
from bluesky.preprocessors import finalize_decorator

@finalize_decorator(smi.modeMeasurement)
def fast_align(angle=0.1):
    '''Align the sample with respect to the beam. GISAXS alignment involves
    vertical translation to the beam center, and rocking theta to get the
    sample plane parralel to the beam. Finally, the angle is re-optimized
    in reflection mode.
    
    The 'step' argument can optionally be given to jump to a particular
    step in the sequence.'''

    #Initialization
    start_time = time.time()

    # For now unused but maybe we should we go back to these positions after failure of fast_align?
    initial_y = piezo.y.position
    initial_th = piezo.th.position

    fast_align = yield from fast_align_procedure(angle=angle)
    

    if not fast_align:
        print('Fast alignment failed')
        print('Trying regular alignment')
        # Should we go back to position before fast_align?
        yield from alignement_gisaxs_doblestack(angle=angle)

    #Here would be a good place to check if the alignment was successful

    # Print the alignment time and the final positions
    align_time = time.time() - start_time
    print('Alignment took {:.1f} seconds'.format(align_time))
    print('y position is {:.3f} and theta position is {:.3f}'.format(piezo.y.position, piezo.th.position))


def fast_align_procedure(angle=0.1, detector=pil2M, intensity_threshold=1000):
    '''
    Fast alignment procedure for GISAXS. This involves first taking a direct beam data to know the db intensity.
    Then, the sample height and incident angle are scanned with the direct beam roi.
    Then, the sample is moved to 1deg and the count on a large ROI is done to see if any reflected beam is detected.
    If so, the incident angle is adjusted to match the reflected beam position.
    If not, the function returns False and a full alignment is needed.

    
    Parameters
    ----------
    angle : float
        The targetted incident angle for the alignement
    detector : detector object
        The beamline detector to trigger to measure intensity (usually pil2M)
    intensity_threshold : float
        The minimum intensity in the reflected beam roi to consider that the reflected beam is found.

    '''   

    #purposely putting a non realistic value for the incident angle 
    rel_th = 10
    #counter for the fast alignement loop. Stop if ct higher than 5
    ct = 0

    # Go into alignment mode
    yield from smi.modeAlignment(technique="gisaxs")

    #Set direct beam ROI1
    yield from smi.setDirectBeamROI()

    #Set reflected beam ROI2
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs", 
                                       size=[48, 8], roi=pil2M.roi2)

    #set ROI3 as a fixed larged area

    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs", 
                                       size=[40,10], roi=pil2M.roi3)

    # Define a big ROI3 to catch the reflected beam from the top of the detector to
    # 100 pixels above the direct beam (to avoid glitches)
    yield from bps.mv(detector.roi3.min_xyz.min_y, 0,
                      detector.roi3.size.y, detector.roi1.min_xyz.min_y.get() - 100)

    # Estimate full-beam intensity
    yield from bps.mvr(piezo.y, -500)
    yield from bp.count([detector])
    db_intensity = detector.stats1.total.get()
    yield from bps.mvr(piezo.y, 500)
        
    if db_intensity < 1000:
        print('WARNING: Direct beam intensity', db_intensity, 'Make sure beam is in the hutch!')
        # We should think to lower the sample further

        iteration_number = 0
        while abs(detector.stats3.total.get() - db_intensity)/db_intensity < 0.1 and iteration_number < 3: 
            iteration_number += 1
            
            # Find the step-edge
            yield from bisection_search_plan(motor=piezo.y, step_size=.1, min_step=0.01, target=0.5, 
                                             intensity=db_intensity, polarity=-1, detector=detector,
                                             detector_suffix='_stats1_total')                
            
            # Find the peak
            yield from bisection_search_plan(motor=piezo.th, step_size=.2, min_step=0.01, target='max',
                                             detector=detector, detector_suffix='_stats1_total')

        #last check for height
        yield from bisection_search_plan(motor=piezo.y, step_size=0.05, min_step=0.005, target=0.5, 
                                         intensity=db_intensity, polarity=-1, detector=detector,
                                         detector_suffix='_stats1_total')
                
    #check reflection beam
    yield from bps.mv(piezo.th, angle)
    yield from bp.count([pil2M])
    
    #check if there is the reflected beam in roi2, enough intensity and max and centroid match
    if abs(pil2M.stats3.max_xy.get().y - pil2M.stats3.centroid.get().y) < 20 and pil2M.stats3.max_value.get() > intensity_threshold:
        #continue the fast alignment 
        print('The reflective beam is found! Continue the fast alignment')
        
        while abs(angle-rel_th) > 0.005 and ct < 5:            
            #absolute reflected beam position in pixels
            refl_beam = detector.roi3.min_xyz.min_y.get() + detector.stats3.max_xy.y.get()

            #calculate the corresponding value incident angle for the current reflected beam
            y0 = smi.SAXS.direct_beam[1]
            distance = smi.SAXS.distance  # mm
            pixel_size = smi.SAXS.pixel_size  # mm
            rel_th = np.rad2deg(0.5*np.arctan(abs(refl_beam-y0)*pixel_size/distance))
            
            print('Th is at {} deg'.format(rel_th))
            yield from bps.mvr(piezo.th, angle-rel_th)
            
            ct += 1
            yield from bp.count([pil2M])

        # Check if the fast alignment was successful
        if detector.stats3.total.get()>50:
            print('The fast alignment works!')
            yield from bps.mvr(piezo.th, -angle)
            return True
        else:
            print('Alignment Error: Cannot Locate the reflection beam')
            yield from bps.mvr(piezo.th, -angle)
            return False

    elif abs(detector.stats2.max_xy.get().y - detector.stats2.centroid.get().y) > 5:
        print('Max and Centroid dont Match, Alignment Error: No reflection beam is found!')
        #perform the full alignment
        yield from bps.mvr(piezo.th, -angle)
        return False

    else:
        print('Intensiy < threshold!, : No reflection beam is found!')
        #perform the full alignment
        yield from bps.mvr(piezo.th, -angle)
        return False



def bisection_search_plan(motor=piezo.y, step_size=1.0, min_step=0.05, intensity=None, target=0.5, 
                detector=None, polarity=1, detector_suffix='_stats1_total'):
    '''
    Bissection search method with the idea to move a motor in one direction and searching for a target value. 
    If the target value is passed, the direction is reversed and the step size is decreased until reaching the minimum step size.
    The target can be a ratio of the full-beam intensity (0.0 to 1.0), or 'max'/'min' to find a minimum or a maximum.
    
    Parameters
    ----------
    motor : bluesky motor
        The motor to move
    step_size : float
        The initial step size when moving the motor
    min_step : float
        The final (minimum) step size to try
    intensity : float
        The expected full-beam intensity readout
    target : float (0.0 to 1.0) or string
        The target ratio of full-beam intensity; 0.5 searches for half-max.
        The target can also be 'max' or 'min' to find a local maximum or minimum.
    detector, detector_suffix
        The beamline detector (and suffix, such as '_stats4_total') to trigger to measure intensity
    polarity : +1 or -1
        Positive motion assumes, e.g. a step-height 'up' (as the axis goes more positive)
    '''   
    if detector is None:
        detector = pil2M
    
    if detector_suffix is None:
        detector_suffix = '_stats1_total'
    
    value_name = detector.name + detector_suffix 

    @bpp.stage_decorator([detector])
    @bpp.run_decorator(md={})
    def inner_search():
        nonlocal intensity, target, step_size

        if intensity is None:
            print('No intensity on the direct beam')
            #Should quit teh search plan       
            return

        # Check current value
        current_intensity = yield from bps.trigger_and_read([detector, motor])
        value = current_intensity[value_name]['value']

        max_value = value
        direction = polarity

        if target == 'max' or target == 'min': 
            while step_size >= min_step:
                yield from bps.mvr(motor, direction*step_size)

                prev_value = value
                yield from bps.trigger_and_read([detector, motor])
                
                value = detector.read()[value_name]['value']

                max_value = max(value, max_value)
                    
                if (target == 'max' and value > prev_value) or \
                (target == 'min' and value < prev_value):
                    # Keep going in this direction...
                    pass
                else:
                    # Switch directions!
                    direction *= -1
                    step_size *= 0.5                   
        
        else:
            target_rel = target
            target = target_rel*intensity            
            
            # Determine initial motion direction: if value > target, go negative
            direction = polarity * (-1 if value>target else 1)
                
            while step_size>=min_step:
                yield from bps.mvr(motor, direction*step_size)                
                yield from bps.trigger_and_read([detector, motor])
                value = detector.read()[value_name]['value']

                # Determine direction
                new_direction = polarity * (-1 if value>target else 1)

                if abs(direction-new_direction) == 0:
                    # Same direction as we've been going... keep moving this way
                    pass
                else:
                    # Switch directions!
                    direction *= -1
                    step_size *= 0.5
    
    yield from inner_search()


from .manipulators import bdm


def alignment_bdm(angle=0.1):
    """
    Regular alignment routine for the bounce down mirror. 
    First, scan the mirror height and incident angle on the direct beam.
    Then scan the incident angle, height, and incident angle again on the reflected beam.
    note the reflected beam will be in the oposite direction compared to gisaxs

    Parameters:
        angle (float): Angle at which the alignment on the reflected beam will be done.
    
    Note:
        1. the height and th of bdm are in opposite directions: 
        the positive direction of height is going down
        the positive direction of th is bending the beam down
    
    
    """
    

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_bdm_height(1, 21, der=True)
    yield from align_bdm_th(1.5, 27)

    # move to theta 0 + value
    yield from bps.mv(bdm.th, ps.peak + angle)

    # Set reflected ROI for beam bending down
    yield from smi.setReflectedBeamROI(total_angle=-angle, technique="gisaxs",sample_z_offset_mm=185)

    # Scan theta and height
    yield from align_bdm_th(0.15, 21)
    yield from align_bdm_height_rb(.15, 16)
    yield from align_bdm_th(0.08, 41)  # was .025, 21 changed to .1 31

    # Scan theta and height finer
    yield from align_bdm_height_rb(.1, 21)
    yield from align_bdm_th(0.05, 51)  # was .025, 21 changed to .1 31

    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(bdm.th, bdm.th.get() - angle)
    print(f'Aligned position of bdm.y {bdm.y.get(): .2f}')
    print(f'Aligned position of bdm.th {bdm.th.get(): .2f}')
    # yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False



def alignment_gisaxs_finer_for_bdm(angle=0.1):
    """
    Regular alignment routine for GISAXS and GIWAXS. First, scan the sample height and incident angle on the direct beam.
    Then scan the incident angle, height, and incident angle again on the reflected beam.

    Parameters:
        angle (float): Angle at which the alignment on the reflected beam will be done.
    """
    

    # Activate the automated derivative calculation
    bec._calc_derivative_and_stats = True

    sample_id(user_name="test", sample_name="test")
    det_exposure_time(0.3, 0.3)

    yield from smi.modeAlignment(technique="gisaxs")

    # Set direct beam ROI
    yield from smi.setDirectBeamROI()

    # Scan theta and height
    yield from align_gisaxs_height(800, 21, der=True)
    yield from align_gisaxs_th(1.5, 27)

    # move to theta 0 + value
    yield from bps.mv(piezo.th, ps.peak + angle)

    # Set reflected ROI
    yield from smi.setReflectedBeamROI(total_angle=angle, technique="gisaxs")

    # Scan theta and height
    yield from align_gisaxs_th(0.2, 21)
    yield from align_gisaxs_height_rb(150, 16)
    yield from align_gisaxs_th(0.1, 31)  # was .025, 21 changed to .1 31


    # Scan theta and height finer
    yield from align_gisaxs_height_rb(50, 41)
    yield from align_gisaxs_th(0.05, 31)  # was .025, 21 changed to .1 31


    # Close all the matplotlib windows
    plt.close("all")

    # Return angle
    yield from bps.mv(piezo.th, piezo.th.position-angle)
    # yield from smi.modeMeasurement()

    # Deactivate the automated derivative calculation
    bec._calc_derivative_and_stats = False

