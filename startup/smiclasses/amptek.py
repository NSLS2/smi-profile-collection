import time as ttime
import numpy as np
from ophyd.status import SubscriptionStatus
from ophyd.mca import EpicsMCA
from ophyd import (
    Component as Cpt,
    Device,
    EpicsSignal,
    EpicsSignalRO,
    EpicsSignalWithRBV,
    DeviceStatus,
    Signal,
    EpicsMotor,
)
from ophyd.device import BlueskyInterface, Staged

# Define energy channels
channels = np.linspace(0, 8191, 8192)
energy_channels = -120.34 + 2.925 * channels


class AmptekMCA(EpicsMCA):
    """
    Custom MCA class for Amptek detectors.
    """
    preset_real_time = Cpt(EpicsSignal, ".PRTM")
    preset_live_time = Cpt(EpicsSignal, ".PLTM")
    elapsed_real_time = Cpt(EpicsSignalRO, ".ERTM")
    elapsed_live_time = Cpt(EpicsSignalRO, ".ELTM")
    check_acquiring = Cpt(EpicsSignal, "CheckACQG")
    client_wait = Cpt(EpicsSignal, "ClientWait")
    collect_data = Cpt(EpicsSignal, "CollectData")
    enable_wait = Cpt(EpicsSignal, "EnableWait")
    erase = Cpt(EpicsSignal, "Erase")
    erase_start = Cpt(EpicsSignal, "EraseStart")
    read_signal = Cpt(EpicsSignal, "Read")
    read_callback = Cpt(EpicsSignal, "ReadCallback")
    read_data_once = Cpt(EpicsSignal, "ReadDataOnce")
    read_status_once = Cpt(EpicsSignal, "ReadStatusOnce")
    set_client_wait = Cpt(EpicsSignal, "SetClientWait")
    start = Cpt(EpicsSignal, "Start")
    status = Cpt(EpicsSignal, "Status")
    stop_signal = Cpt(EpicsSignal, "Stop")
    when_acq_stops = Cpt(EpicsSignal, "WhenAcqStops")
    why1 = Cpt(EpicsSignal, "Why1")
    why2 = Cpt(EpicsSignal, "Why2")
    why3 = Cpt(EpicsSignal, "Why3")
    why4 = Cpt(EpicsSignal, "Why4")


class Amptek(Device):
    """
    Amptek detector device.
    """
    mca = Cpt(AmptekMCA, "mca1")
    dwell = Cpt(EpicsSignal, "Dwell")
    energy_channels = Cpt(Signal, value=energy_channels)


class AmptekSoftTrigger(BlueskyInterface):
    """
    Soft trigger interface for Amptek detectors.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._status = None
        self._acquisition_signal = self.mca.erase_start
        self._count_signal = self.mca.preset_real_time
        self._count_time = None

        # Set kinds
        self.kind = "hinted"
        self.mca.kind = "hinted"
        self.mca.rois.kind = "hinted"
        self._starting = None

    def stage(self, *args, **kwargs):
        """
        Prepare the detector for acquisition.
        """
        for num in range(5):
            roi_n = getattr(self.mca.rois, f"roi{num}")
            roi_n.kind = "hinted"
            roi_n.count.kind = "hinted"
            label = roi_n.label.get()
            if label:
                roi_n.count.name = label
                for cpt in roi_n.component_names:
                    if cpt != "count":
                        getattr(roi_n, cpt).name = f"{label}_{cpt}"
            else:
                roi_n.kind = "normal"
                roi_n.count.kind = "normal"

        super().stage(*args, **kwargs)
        if self._count_time is not None:
            self.stage_sigs[self._count_signal] = self._count_time

    def trigger(self, *args, **kwargs):
        """
        Trigger one acquisition.
        """
        if self._staged != Staged.yes:
            raise RuntimeError(
                "This detector is not ready to trigger. "
                "Call the stage() method before triggering."
            )

        def callback(value, old_value, **kwargs):
            if int(round(old_value)) == 1 and int(round(value)) == 0:
                return True

        max_time = 1 + 2 * self.mca.preset_real_time.get()
        status = SubscriptionStatus(
            self.mca.when_acq_stops, callback, run=False, timeout=max_time
        )
        self._acquisition_signal.put(1)
        return status

    @property
    def count_time(self):
        """
        Exposure time, as set by bluesky.
        """
        return self._count_time

    @count_time.setter
    def count_time(self, count_time):
        self._count_time = count_time


class SMIAmptek(AmptekSoftTrigger, Amptek):
    """
    SMI-specific Amptek detector class.
    """
    def __init__(self, prefix, *, read_attrs=None, configuration_attrs=None, **kwargs):
        if read_attrs is None:
            read_attrs = ["mca.spectrum"]

        if configuration_attrs is None:
            configuration_attrs = [
                "mca.preset_real_time",
                "mca.preset_live_time",
            ]

        super().__init__(
            prefix,
            read_attrs=read_attrs,
            configuration_attrs=configuration_attrs,
            **kwargs,
        )


class AmptekPositions(Device):
    """
    Amptek motor positions.
    """
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    z = Cpt(EpicsMotor, "Z}Mtr")



