
from ophyd import (
    Device,
    EpicsSignal,
    EpicsSignalRO,
    Signal,
    Component as Cpt,
    DeviceStatus,
)


class TwoButtonShutter(Device):
    # TODO this needs to be fixed in EPICS as these names make no sense
    # the vlaue comingout of the PV do not match what is shown in CSS
    open_cmd = Cpt(EpicsSignal, "Cmd:Opn-Cmd", string=True)
    open_val = "Open"

    close_cmd = Cpt(EpicsSignal, "Cmd:Cls-Cmd", string=True)
    close_val = "Not Open"

    status = Cpt(EpicsSignalRO, "Pos-Sts", string=True)
    fail_to_close = Cpt(EpicsSignalRO, "Sts:FailCls-Sts", string=True)
    fail_to_open = Cpt(EpicsSignalRO, "Sts:FailOpn-Sts", string=True)
    # user facing commands
    open_str = "Insert"
    close_str = "Retract"
    #!!these commands are correct with open_str = 'Insert'  close_str = 'Retract'for FOILS ONLY, to trigger gatevalevs this has to be swapped!!!
    # to check with Bluesky guys!!!

    def set(self, val):
        if self._set_st is not None:
            raise RuntimeError("trying to set while a set is in progress")

        cmd_map = {self.open_str: self.open_cmd, self.close_str: self.close_cmd}
        target_map = {self.open_str: self.open_val, self.close_str: self.close_val}

        cmd_sig = cmd_map[val]
        target_val = target_map[val]

        st = self._set_st = DeviceStatus(self)
        enums = self.status.enum_strs

        def shutter_cb(value, timestamp, **kwargs):
            value = enums[int(value)]
            if value == target_val:
                self._set_st._finished()
                self._set_st = None
                self.status.clear_sub(shutter_cb)

        cmd_enums = cmd_sig.enum_strs
        count = 0

        def cmd_retry_cb(value, timestamp, **kwargs):
            nonlocal count
            value = cmd_enums[int(value)]
            # ts = datetime.datetime.fromtimestamp(timestamp).strftime(_time_fmtstr)
            # print('sh', ts, val, st)
            count += 1
            if count > 5:
                cmd_sig.clear_sub(cmd_retry_cb)
                st._finished(success=False)
            if value == "None":
                if not st.done:
                    yield from bps.sleep(0.5)
                    cmd_sig.set(1)
                    ts = datetime.datetime.fromtimestamp(timestamp).strftime(
                        _time_fmtstr
                    )
                    print(
                        "** ({}) Had to reactuate shutter while {}ing".format(ts, val)
                    )
                else:
                    cmd_sig.clear_sub(cmd_retry_cb)

        cmd_sig.subscribe(cmd_retry_cb, run=False)
        cmd_sig.set(1)
        self.status.subscribe(shutter_cb)
        return st

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ["status"]


class SMIFastShutter(Device):
    open_cpt = Cpt(EpicsSignal, "XF:12IDC-ES:2{PSh:ES}pz:sh:open")
    close_cpt = Cpt(EpicsSignal, "XF:12IDC-ES:2{PSh:ES}pz:sh:close")
    status_pv = Cpt(EpicsSignalRO, "XF:12IDA-BI:2{EM:BPM1}DAC3")
    status = Cpt(Signal, value="")

    def check_status(self):
        if int(self.status_pv.get()) == 7:
            self.status.put("Closed")
        elif int(self.status_pv.get()) == 0:
            self.status.put("Open")
        else:
            raise RuntimeError(f'Shutter "{self.name}" is in a weird state.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_status()

    def open(self):
        self.open_cpt.put(1)
        self.check_status()

    def close(self):
        self.close_cpt.put(1)
        self.check_status()

