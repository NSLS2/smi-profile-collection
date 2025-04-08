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


def set_energy_cam(cam,en_ev):
     
    en = en_ev / 1000 # change to kev

    if en<2 : # invalid energy
        en = 16.1
        gain = 1
    elif en<4:
        gain = 3
    elif en < 7:
        gain = 2
    elif en < 20:
        gain = 1
    else:
        gain = 0    

    if en < 3.2:
        thresh = 1.6
    elif 13 < en < 22 and 'waxs' in cam.name: ## avoid the fluoresence from the waxs beamstop
        thresh = 11.5
    else:
        thresh = en/2

    cam.cam_energy.put(en)
    cam.threshold_energy.put(thresh)
    cam.gain_menu.put(gain)
    cam.threshold_apply.put(1)

    cam.energyset.set(en) # store so it remembers on failure and resets


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
    def __init__(self, *args, md=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._md = md
        self.__stage_cache = {}
        self._asset_path = ''

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
        return f"{self.root}/{self._md['cycle']}/{self._md['data_session']}/assets/{self._asset_path}/"

    def stage(self):

        self._update_paths()
        return super().stage()



class Pilatus(SingleTriggerV33, PilatusDetector):
    tiff = Cpt(
        TIFFPluginWithFileStore,
        suffix="TIFF1:",
        md=RE.md,
        write_path_template="/ramdisk/PLACEHOLDER",
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
            yield from bps.mv(self.energy, energy)
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



class PIL1MPositions(Device):
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


class WAXS(Device):
    arc = Cpt(EpicsMotor, "WAXS:1-Ax:Arc}Mtr")
    bs_x = Cpt(EpicsMotor, "MCS:1-Ax:5}Mtr")
    bs_y = Cpt(EpicsMotor, "BS:WAXS-Ax:y}Mtr")

    def set(self, arc_value):
        st_arc = self.arc.set(arc_value)

        if self.arc.limits[0] <= arc_value <= 10.1:
            calc_value = self.calc_waxs_bsx(arc_value)

        elif 10.1 < arc_value <= 13:
            raise ValueError(
                "The waxs detector cannot be moved to {} deg until the new beamstop is mounted".format(
                    arc_value
                )
            )
        else:
            calc_value = -100

        st_x = self.bs_x.set(calc_value)
        return st_arc & st_x

    def calc_waxs_bsx(self, arc_value):
        bsx_pos = -37.56 -249.69871 * np.tan(np.deg2rad(arc_value))    # 2025 March 26

        return bsx_pos
