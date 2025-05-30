from ophyd import (
    Component as Cpt,
    ADComponent,
    Signal,
    Device,
    EpicsSignal,
    EpicsSignalRO,
    EpicsMotor,
    ROIPlugin,
    TransformPlugin,
    PilatusDetector,
    OverlayPlugin,
    TIFFPlugin,
    Staged,
    DeviceStatus,
)

from ophyd.areadetector.cam import PilatusDetectorCam
from ophyd.areadetector.detectors import PilatusDetector
from ophyd.areadetector.base import EpicsSignalWithRBV as SignalWithRBV
from ophyd.areadetector.filestore_mixins import FileStoreTIFFIterativeWrite

import bluesky.plans as bp
import time
from nslsii.ad33 import StatsPluginV33, SingleTriggerV33
import bluesky.plan_stubs as bps

from ophyd.utils.epics_pvs import AlarmStatus

import uuid
import numpy as np
import time as ttime


from smibase.energy import energy
from smibase.base import RE
from smibase.beamstop import SAXSBeamStops


class StatsWCentroid(StatsPluginV33):
    centroid_total = Cpt(EpicsSignalRO,'CentroidTotal_RBV')


class PilatusDetectorCamV33(PilatusDetectorCam):
    """This is used to update the Pilatus to AD33."""

    wait_for_plugins = Cpt(EpicsSignal, "WaitForPlugins", string=True, kind="config")
    file_path = Cpt(SignalWithRBV, "FilePath", string=True)
    file_name = Cpt(SignalWithRBV, "FileName", string=True)
    file_template = Cpt(SignalWithRBV, "FileTemplate", string=True)
    file_number = Cpt(SignalWithRBV, "FileNumber")
    auto_increment = Cpt(SignalWithRBV, "AutoIncrement")
    cam_energy = Cpt(SignalWithRBV, "Energy")
    energyset = Cpt(Signal, name="Beamline Energy", value=energy.energy.readback.get()) # remember the energy of the beamline


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs["wait_for_plugins"] = "Yes"
        self.stage_sigs["file_template"] = "%s%s_%6.6d_SAXS.tif"
        self.stage_sigs["auto_increment"] = 1
        self.stage_sigs["file_number"] = 0


    def ensure_nonblocking(self):
        self.stage_sigs["wait_for_plugins"] = "Yes"
        for c in self.parent.component_names:
            cpt = getattr(self.parent, c)
            if cpt is self:
                continue
            if hasattr(cpt, "ensure_nonblocking"):
                cpt.ensure_nonblocking()
    # file_path = Cpt(SignalWithRBV, "FilePath", string=True)
    # file_name = Cpt(SignalWithRBV, "FileName", string=True)
    # file_template = Cpt(SignalWithRBV, "FileName", string=True)
    # file_number = Cpt(SignalWithRBV, "FileNumber")

    def stage(self):
        self.file_name.set(str(uuid.uuid4()))
        super().stage()

class PilatusDetector(PilatusDetector):
    cam = Cpt(PilatusDetectorCamV33, "cam1:")


class TIFFPluginWithFileStore(TIFFPlugin, FileStoreTIFFIterativeWrite):
    # def __init__(self, *args, md=None, root_path="/nsls2/data/smi/proposals", **kwargs):
    def __init__(self, *args, root_str="/nsls2/data/smi/proposals", md=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._md = md
        self.__stage_cache = {}
        self._asset_path = ''
        self.root_str = root_str

    def describe(self):
        ret = super().describe()
        key = self.parent._image_name
        color_mode = self.parent.cam.color_mode.get(as_string=True)
        if color_mode == 'Mono':
            ret[key]['shape'] = [
                self.parent.cam.num_images.get(),
                self.array_size.height.get(),
                self.array_size.width.get()
                ]

        elif color_mode in ['RGB1', 'Bayer']:
            ret[key]['shape'] = [self.parent.cam.num_images.get(), *self.array_size.get()]
        else:
            raise RuntimeError("SHould never be here")

        cam_dtype = self.data_type.get(as_string=True)
        type_map = {'UInt8': '|u1', 'UInt16': '<u2', 'Float32':'<f4', "Float64":'<f8', 'Int32':'<i4'}
        if cam_dtype in type_map:
            ret[key].setdefault('dtype_str', type_map[cam_dtype])

        return ret

    def get_frames_per_point(self):
        ret = super().get_frames_per_point()
        print('get_frames_per_point returns', ret)
        return ret

    def _update_paths(self):
        self.write_path_template = self.root_path_str + "%Y/%m/%d/"
        self.read_path_template = self.root_path_str + "%Y/%m/%d/"
        self.reg_root = self.root_path_str

    @property
    def root_path_str(self):
        return f"{self.root_str}/{self._md['cycle']}/{self._md['data_session']}/assets/{self._asset_path}/"

    def stage(self):

        self._update_paths()
        return super().stage()



class Pilatus(SingleTriggerV33, PilatusDetector):
    tiff = Cpt(
        TIFFPluginWithFileStore,
        suffix="TIFF1:",
        md=RE.md,
        write_path_template="/ramdisk/PLACEHOLDER",
        root_str="/nsls2/data/smi/proposals",
        root="/nsls2/data/smi/proposals",
    )

    def __init__(self, *args, asset_path, **kwargs):
        self.asset_path = asset_path
        super().__init__(*args, **kwargs)
        self.tiff._asset_path = self.asset_path

    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")

    stats1 = Cpt(StatsWCentroid, "Stats1:", read_attrs=["total"])
    stats2 = Cpt(StatsWCentroid, "Stats2:", read_attrs=["total"])
    stats3 = Cpt(StatsWCentroid, "Stats3:", read_attrs=["total"])
    stats4 = Cpt(StatsWCentroid, "Stats4:", read_attrs=["total"])
    stats5 = Cpt(StatsWCentroid, "Stats5:", read_attrs=["total"])

    over1 = Cpt(OverlayPlugin, "Over1:")
    trans1 = Cpt(TransformPlugin, "Trans1:")

    threshold = Cpt(EpicsSignal, "cam1:ThresholdEnergy")
    cam_energy = Cpt(EpicsSignal, "cam1:Energy")
    gain = Cpt(EpicsSignal, "cam1:GainMenu")
    apply = Cpt(EpicsSignal, "cam1:ThresholdApply")

    threshold_read = Cpt(EpicsSignal, "cam1:ThresholdEnergy_RBV")
    energy_read = Cpt(EpicsSignal, "cam1:Energy_RBV")
    gain_read = Cpt(EpicsSignal, "cam1:GainMenu_RBV")
    apply_read = Cpt(EpicsSignal, "cam1:ThresholdApply_RBV")

    def set_primary_roi(self, num):
        st = f"stats{num}"
        self.read_attrs = [st, "tiff"]
        getattr(self, st).kind = "hinted"

    # This is breaking some of the scans trying to reset trshold and gain

    def apply_threshold(self, energy=16.1, threshold=11.5, gain="autog"):
        if 1.5 < energy < 24:
            yield from bps.mv(self.cam_energy, energy)
        else:
            raise ValueError(
                "The energy range for Pilatus is 1.5 to 24 keV. The entered value is {}".format(
                    energy
                )
            )

        if 1.5 < threshold < 24:
            yield from bps.mv(self.threshold, threshold)
        else:
            raise ValueError(
                "The threshold range for Pilatus is 1.5 to 24 keV. The entered value is {}".format(
                    threshold
                )
            )

        # That will need to be checked and tested
        if gain == "autog":
            yield from bps.mv(self.gain, 1)
        elif gain == "uhighg":
            yield from bps.mv(self.gain, 3)
        else:
            raise ValueError(
                "The gain used is unknown. It shoul be either autog or uhighg"
            )
        yield from bps.mv(self.apply, 1)

    def read_threshold(self):
        return self.energy_read, self.threshold_read, self.gain_read

    def trigger(self):
        "Trigger one acquisition."
        if self._staged != Staged.yes:
            raise RuntimeError("This detector is not ready to trigger."
                               "Call the stage() method before triggering.")

        self._status = self._status_type(self)
        fail_count = 0
        def _acq_done(*, data, pvname):
            nonlocal fail_count
            data.get()
            if data.alarm_status is not AlarmStatus.NO_ALARM:

 
                if fail_count < 4:
                    # chosen after testing and it failing 2x per cam server restart so
                    # so two extra tries seems reasonable
                    print('\n\n\n\nYOL0(or twice): retrying detector failure')
                    print('Reset detector camserver if this is the start of the macro\n\n\n\n\n')
                    self._acquisition_signal.put(1, use_complete=True, callback=_acq_done, 
                                     callback_data=self.cam.detector_state)
                
                    fail_count += 1
                    time.sleep(1)
                elif fail_count < 7:
                    # chosen after testing and it failing 2x per cam server restart so
                    # so two extra tries seems reasonable
                    print('\n\n\n\nYOL0(or twice): retrying detector failure')
                    print('Reset detector camserver if this is the start of the macro\n\n\n\n\n')
                    self._acquisition_signal.put(1, use_complete=True, callback=_acq_done, 
                                     callback_data=self.cam.detector_state)
                
                    fail_count += 1
                    time.sleep(60)
                    #reset the threshold 
                    set_energy_cam(self.cam,self.cam.energyset.get())
                    time.sleep(5)

                else:
                    self._status.set_exception(
                        RuntimeError(f"FAILED {pvname}: {data.alarm_status}: {data.alarm_severity}")
                    )
            else:
                self._status._finished()

        self._acquisition_signal.put(1, use_complete=True, callback=_acq_done, 
                                     callback_data=self.cam.detector_state)
        self.dispatch(self._image_name, ttime.time())
        return self._status



class FakeDetector(Device):
    acq_time = Cpt(Signal, value=10)

    _default_configuration_attrs = ("acq_time",)
    _default_read_attrs = ()

    def trigger(self):
        st = self.st = DeviceStatus(self)

        from threading import Timer

        self.t = Timer(self.acq_time.get(), st._finished)
        self.t.start()
        return st



class SAXSPositions(Device):
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    z = Cpt(EpicsMotor, "Z}Mtr")



#####################################################
# ------ NOT TESTED AFTER DATA SECURITY CHANGES -----
# Pilatus 300kw definition

# pil300KW = Pilatus("XF:12IDC-ES:2{Det:300KW}", name="pil300KW", asset_path="pilatus300kw-1")  # , detector_id="WAXS")
# pil300KW.set_primary_roi(1)

# pil300kwroi1 = EpicsSignal(
#     "XF:12IDC-ES:2{Det:300KW}Stats1:Total_RBV", name="pil300kwroi1"
# )
# pil300kwroi2 = EpicsSignal(
#     "XF:12IDC-ES:2{Det:300KW}Stats2:Total_RBV", name="pil300kwroi2"
# )
# pil300kwroi3 = EpicsSignal(
#     "XF:12IDC-ES:2{Det:300KW}Stats3:Total_RBV", name="pil300kwroi3"
# )
# pil300kwroi4 = EpicsSignal(
#     "XF:12IDC-ES:2{Det:300KW}Stats4:Total_RBV", name="pil300kwroi4"
# )

# pil300KW.stats1.kind = "hinted"
# pil300KW.stats1.total.kind = "hinted"
# pil300KW.cam.num_images.kind = "config"
# pil300KW.cam.ensure_nonblocking()



# "multi_count" plan is dedicated to the time resolved Pilatus runs when the number of images in area detector is more than 1


class WAXS_Motors(Device):
    arc = Cpt(EpicsMotor, "WAXS:1-Ax:Arc}Mtr")
    bs_x = Cpt(EpicsMotor, "MCS:1-Ax:5}Mtr")
    bs_y = Cpt(EpicsMotor, "BS:WAXS-Ax:y}Mtr")
    test = 5
    bsx_offset = -54.8600000 
                # offset from the beam center to the beamstop in mm
                # this value should be reset in the motor offset - not here
                # the procedure is to move the motor to the negative limit (outboard) and run home_forward.set(1) on the waxs beamstop x
                # waxs.bs_x.home_forward.set(1).  this should reset position correctly
                # if the beamstop mounting is changed or bent, this value may need to be tweaked
    bsz_offset = 249.69871 
                # distance from the center of arc rotation (sample position) to the beamstop
                # in mm   
                # if the beamstop mounting is changed or bent, this value may need to be tweaked
    bsx_safe_pos = -100 
                # x position of the beamstop when it IS NOT in the beam (out of the way direct beam and scattering)
    
    # when moving the waxs detector, the beamstop must be moved to a new position
    # the beamstop is moved to a new position based on the angle of the waxs detector
    def set(self, arc_value):
        st_arc = self.arc.set(arc_value)
        # start moving the arc stage and return the status

        if self.arc.limits[0] <= arc_value <= 10.1:
            calc_value = self.calc_waxs_bsx(arc_value)
            # calculate the position of the beamstop based on the angle of the waxs detector
        elif 10.1 < arc_value <= 13:
            # the beamstop cannot be moved to block the beam
            # this move is not safe
            raise ValueError(
                f"The waxs detector cannot be moved to {arc_value} deg \n"
                "Do NOT take data between 10.1 and 13 degrees WAXS arc"   
            )
        else:
            calc_value = self.bsx_safe_pos # out of the path of the beam and scattering

        st_x = self.bs_x.set(calc_value)
        # move the beamstop to the new position
        return st_arc & st_x # return both statuses
    def stop(self, *args, **kwargs):
        # stop the arc stage and the beamstop
        st_arc = self.arc.stop()
        st_x = self.bs_x.stop()
        return st_arc & st_x
    # calculate the position of the beamstop based on the angle of the waxs detector
    # the beamstop is on the arc stage, so as the angle of the waxs detector changes, the position of the beamstop must also change
    def calc_waxs_bsx(self, arc_value):
        bsx_pos = ( 
            self.bsx_offset # offset from the beam center to the beamstop in mm
            - (self.bsz_offset # distance from the center of arc rotation (sample position) to the beamstop
            * np.tan( # beamstop movement is a linear movement on the arc stage
                np.deg2rad(arc_value)))) # the angle of the waxs detector arc in degrees
        # 2025 March 26
        
        return bsx_pos


class WAXS_Detector(Pilatus):
## real positions of the SAXS detector and the beamstop
    ## WAXS det position and beamstop (mounted on the same stage)
    motors = Cpt(WAXS_Motors,"XF:12IDC-ES:2{",add_prefix= "", kind="config")
    
    
## the virtual positions of the beamcenter (in pixels) and the sample distance
    # values will be over written by the beam center calculation
    # based on the motor positions and the constant offsets
    col1_beam_center_x_px = Cpt(Signal,value =0, kind="normal")
    col1_beam_center_x_mm = Cpt(Signal,value =0, kind="config")
    col1_beam_center_y_px = Cpt(Signal,value =225, kind="normal")
    col1_beam_center_y_mm = Cpt(Signal,value =225*0.172, kind="config")
    col1_beam_center_angle_deg = Cpt(Signal,value = -7, kind="config")
    col1_sample_distance_mm = Cpt(Signal,value =284, kind="normal")
    col2_beam_center_x_px = Cpt(Signal,value =0, kind="normal")
    col2_beam_center_x_mm = Cpt(Signal,value =0, kind="config")
    col2_beam_center_y_px = Cpt(Signal,value =225, kind="normal")
    col2_beam_center_y_mm = Cpt(Signal,value =225*0.172, kind="config")
    col2_beam_center_angle_deg = Cpt(Signal,value =0, kind="config")
    col2_sample_distance_mm = Cpt(Signal,value =284, kind="normal")
    col3_beam_center_x_px = Cpt(Signal,value =0, kind="normal")
    col3_beam_center_x_mm = Cpt(Signal,value =0, kind="config")
    col3_beam_center_y_px = Cpt(Signal,value =225, kind="normal")
    col3_beam_center_y_mm = Cpt(Signal,value =225*0.172, kind="config")
    col3_beam_center_angle_deg = Cpt(Signal,value = 7, kind="config")
    col3_sample_distance_mm = Cpt(Signal,value =284, kind="normal")

## constants for the beam center calculation
    # offsets will be reset by the calc_offsets function
    # all other values should be set here from calibration / lookup table
    pixel_size_mm = Cpt(Signal,value =0.172, kind="config") # in mm
    # offset from 0th column pixel to the beam center at saxs position x = 0
    col1_beam_offset_x_mm = Cpt(Signal,value =127.968, kind="config") 
    col2_beam_offset_x_mm = Cpt(Signal,value =127.968, kind="config") 
    col3_beam_offset_x_mm = Cpt(Signal,value =127.968, kind="config") 
    # offset from 0th row pixel to the beam center at saxs position y = 0
    col1_beam_offset_y_mm = Cpt(Signal,value =190.404, kind="config")
    col2_beam_offset_y_mm = Cpt(Signal,value =190.404, kind="config")
    col3_beam_offset_y_mm = Cpt(Signal,value =190.404, kind="config")
    # difference between the position.z and the actual sample-detector distance
    col1_sample_offset_z_mm = Cpt(Signal,value =0.0, kind="config")
    col2_sample_offset_z_mm = Cpt(Signal,value =0.0, kind="config")
    col3_sample_offset_z_mm = Cpt(Signal,value =0.0, kind="config")
    # difference between the arc angle and the actual angle
    col1_angle_offset = Cpt(Signal,value =-7.0, kind="config")
    col2_angle_offset = Cpt(Signal,value =0.0, kind="config")
    col3_angle_offset = Cpt(Signal,value =7, kind="config")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motors.arc.subscribe(self.update_beam_center)
    
    def update_beam_center(self, *args, **kwargs):
        # based on the position, update the offsets from a calibration file
        self.calc_offsets(self.motors.arc.position)
        # use the angle offsets and the arc position to update the virtyal beam angles
        self.col1_beam_center_angle_deg.set(
            self.motors.arc.position + self.col1_angle_offset.get()
        )
        self.col2_beam_center_angle_deg.set(
            self.motors.arc.position + self.col2_angle_offset.get()
        )
        self.col3_beam_center_angle_deg.set(
            self.motors.arc.position + self.col3_angle_offset.get()
        )

    def calc_offsets(self, angle):
        # use a spline fit to calculate the offsets based on the angle
        # this is a placeholder, the actual calculation will depend on the calibration
        # the offsets are in mm
        # self.col1_beam_offset_x_mm.set(0.0)
        # self.col1_beam_offset_y_mm.set(0.0)
        # self.col2_beam_offset_x_mm.set(0.0)
        # self.col2_beam_offset_y_mm.set(0.0)
        # self.col3_beam_offset_x_mm.set(0.0)
        # self.col3_beam_offset_y_mm.set(0.0)
        # self.col1_sample_offset_z_mm.set(0.0)
        # self.col2_sample_offset_z_mm.set(0.0)
        # self.col3_sample_offset_z_mm.set(0.0)
        ...


class DetMotor(Device):
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    z = Cpt(EpicsMotor, "Z}Mtr")


class SAXS_Detector(Pilatus):
## real positions of the SAXS detector and the beamstop
    ## SAXS det position
    motor = Cpt(DetMotor,"XF:12IDC-ES:2{Det:1M-Ax:",add_prefix= "", kind="config")
    ## stages for SAXS beamstops (two beamstops, each with their own offset from the beam center)
    beamstop = Cpt(SAXSBeamStops,"XF:12IDC-ES:2{BS:SAXS-Ax:",add_prefix= "", kind="config")

## the virtual positions of the beamcenter (in pixels) and the sample distance
    # values will be over written by the beam center calculation
    # based on the motor positions and the constant offsets
    beam_center_x_px = Cpt(Signal,value =-744, kind="normal")
    beam_center_x_mm = Cpt(Signal,value =127.968, kind="config")
    beam_center_y_px = Cpt(Signal,value =-1107, kind="normal")
    beam_center_y_mm = Cpt(Signal,value =190.404, kind="config")
    sample_distance_mm = Cpt(Signal,value =0.0, kind="normal")

## constants for the beam center calculation
    # offsets will be reset by the calc_offsets function
    # all other values should be set here from calibration / lookup table
    pixel_size_mm = Cpt(Signal,value =0.172, kind="config") # in mm
    # offset from 0th column pixel to the beam center at saxs position x = 0
    beam_offset_x_mm = Cpt(Signal,value =127.968, kind="config") 
    # offset from 0th row pixel to the beam center at saxs position y = 0
    beam_offset_y_mm = Cpt(Signal,value =190.404, kind="config")
    # difference between the position.z and the actual sample-detector distance
    sample_offset_z_mm = Cpt(Signal,value =0.0, kind="config")
    
## constants for the beamstop position
    rod_offset_x_mm = Cpt(Signal,value =6.8, kind="config")
    # position of the beamstop when it IS in the beam x
    rod_offset_y_mm = Cpt(Signal,value =0.0, kind="config") 
    # position of the beamstop when it IS in the beam y
    rod_safe_pos = Cpt(Signal,value =-200, kind="config") 
    # x position of the beamstop when it IS NOT in the beam (out of the way for the pin diode)
    pd_offset_x_mm = Cpt(Signal,value =-226.5, kind="config") 
    # position of the beamstop when it IS in the beam x
    pd_offset_y_mm = Cpt(Signal,value =8, kind="config") 
    # position of the beamstop when it IS in the beam y
    pd_safe_pos = Cpt(Signal,value =0.0, kind="config") 
    # x position of the beamstop when it IS NOT in the beam (out of the way for the rod)


# subscribe the virtual signals to the motors, so they are updated when the motors move
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor.x.subscribe(self.update_beam_center)
        self.motor.y.subscribe(self.update_beam_center)
        self.motor.z.subscribe(self.update_beam_center) # if there is wobble in the track, the x an y center will vary
    
# callback function to update the beam center based on the motor positions will be called often
    def update_beam_center(self, *args, **kwargs):
        # based on the position, update the offsets from a calibration file
        self.calc_offsets(self.motor.z.position) # account for the wobble in the track
        # use the offsets and the motor positions to update the virtual beam center in mm, and then convert to pixels
        self.beam_center_x_mm.set(
            self.motor.x.position - self.beam_offset_x_mm.get()
        )
        self.beam_center_y_mm.set(
            self.motor.y.position - self.beam_offset_y_mm.get()
        )
        self.sample_distance_mm.set(
            self.motor.z.position + self.sample_offset_z_mm.get()
        )
        self.beam_center_x_px.set(
            (self.beam_center_x_mm.get()) / self.pixel_size_mm.get()
        )
        self.beam_center_y_px.set(
            (self.beam_center_y_mm.get()) / self.pixel_size_mm.get()
        )
    
    # move the beamstop to the calculated position of the beam center
    def insert_beamstop(self, beamstop='rod', offset=0.0):
        if beamstop == 'rod':
            #move pd to safe position
            yield from bps.mv(self.beamstop.x_pin, self.pd_safe_pos.get())
            #move rod to beam center
            yield from bps.mv(self.beamstop.x_rod, self.rod_offset_x_mm.get())
        elif beamstop == 'pd':
            #move rod to safe position
            yield from bps.mv(self.beamstop.x_rod, self.rod_safe_pos.get())
            #move pd to beam center
            yield from bps.mv(self.beamstop.x_pin, self.pd_offset_x_mm.get(),
                              self.beamstop.y_pin, self.pd_offset_y_mm.get())
        else:
            raise ValueError("beamstop must be either 'rod' or 'pd'")
    
    def calc_offsets(self, distance, verbose=False):
        # use a spline fit to calculate the offsets based on the distance
        # this is a placeholder, the actual calculation will depend on the calibration
        # the offsets are in mm
        #self.beam_offset_x_mm.set(0.0)
        #self.beam_offset_y_mm.set(0.0)
        #self.rod_offset_x_mm.set(0.0)
        #self.rod_offset_y_mm.set(0.0)
        #self.pd_offset_x_mm.set(0.0)
        #self.pd_offset_y_mm.set(0.0)
        #self.sample_offset_z_mm.set(0.0)
        if verbose:
            print("Offsets calculated based on distance: ", distance)
            print("Beam center x offset: ", self.beam_offset_x_mm.get())
            print("Beam center y offset: ", self.beam_offset_y_mm.get())
            print("Rod x offset: ", self.rod_offset_x_mm.get())
            print("Rod y offset: ", self.rod_offset_y_mm.get())
            print("Pin diode x offset: ", self.pd_offset_x_mm.get())
            print("Pin diode y offset: ", self.pd_offset_y_mm.get())
            print("Sample distance offset: ", self.sample_offset_z_mm.get())
