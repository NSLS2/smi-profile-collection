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
    yield from bps.mv(piezo.th, ps.peak + angle)

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

    yield from smi.setReflectedBeamROI(total_angle=0.06, technique="gisaxs")
    yield from align_gisaxs_th_hex(0.5, 31)

    # move to theta 0 + value
    yield from bps.mv(stage.th, ps.peak + angle)

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