
from ophyd import (
    Device,
    EpicsSignal,
    EpicsSignalRO,
    Signal,
    Component as Cpt,
    DeviceStatus,
)
import datetime, time

# Unify on the maintained upstream TwoButtonShutter from nslsii (robust set(): handles
# str/int enum read-backs, short-circuits when already in position, MAX_ATTEMPTS retry,
# enabled_status).  The local re-implementation that used to live here was a divergent,
# buggier copy (it crashed on already-string enum read-backs, had no "already in position"
# short-circuit, and spammed prints).  We keep a thin SMI subclass below that adds the one
# thing the beamline needs: explicit, PER-VALVE actuation polarity.
from nslsii.devices import TwoButtonShutter as _NSLSIITwoButtonShutter

_time_fmtstr = "%Y-%m-%d %H:%M:%S"


class TwoButtonShutter(_NSLSIITwoButtonShutter):
    """Two-button (open/close) shutter / gate valve with EXPLICIT, per-valve polarity.

    Why this subclass exists
    ------------------------
    SMI's valves do **not** share a single open/close convention -- per beamline staff:

    * the **command** value that actuates a valve can be ``1`` *or* ``0`` depending on the valve
      (but "open" and "close" are always opposite of each other); and
    * the **status** read-back's meaning of open/closed also varies per valve, but is consistent
      for any single valve.

    The upstream nslsii ``set()`` hard-codes ``cmd_sig.set(1)`` (always press with ``1``) and
    confirms against ``open_val``/``close_val``.  That is correct for valves actuated by ``1`` but
    cannot express a valve that must be actuated with ``0``.  This subclass makes **all** of those
    knobs per-instance overridable, so each valve can be configured to match what its CSS screen
    shows, **without** silently flattening the variability:

    * :attr:`cmd_actuate_val` -- the value written to the *pressed* command PV (default ``1`` == the
      historical behavior; set per instance to ``0`` for a valve wired the other way);
    * :attr:`open_val` / :attr:`close_val` -- the ``Pos-Sts`` strings that CONFIRM each state;
    * :attr:`open_str` / :attr:`close_str` -- the user-facing command words.

    .. important::
       The default is **identical to the previous production behavior** (actuate with ``1``,
       confirm 'Open'/'Not Open').  No valve's behavior changes until it is *explicitly* given a
       different polarity.  The per-valve polarity values still need to be confirmed against CSS
       before being trusted (see restructure-plan Q5).
    """

    # User-facing command words.  (Default to 'Open'/'Close'; the old local class used
    # 'Insert'/'Retract', which was flagged in-code as "correct for FOILS ONLY" -- foils now have
    # their own Attenuator class, so valves use the sensible Open/Close.)
    open_str = "Open"
    close_str = "Close"

    #: value written to the *pressed* command PV (Cmd:Opn-Cmd for open, Cmd:Cls-Cmd for close).
    #: Default 1 == historical behavior.  Override per instance for a valve actuated by 0.
    cmd_actuate_val = 1

    def set(self, val):
        """Open/close the valve, retrying actuation until ``status`` confirms.

        This mirrors nslsii's ``TwoButtonShutter.set`` exactly, except the actuation value is
        :attr:`cmd_actuate_val` (instead of a hard-coded ``1``) so per-valve polarity is honored,
        and the upstream per-call debug ``print`` is dropped.
        """
        if self._set_st is not None:
            raise RuntimeError(
                "trying to set {} while a set is in progress".format(self.name))

        cmd_map = {self.open_str: self.open_cmd, self.close_str: self.close_cmd}
        target_map = {self.open_str: self.open_val, self.close_str: self.close_val}

        cmd_sig = cmd_map[val]
        target_val = target_map[val]
        actuate = self.cmd_actuate_val

        st = DeviceStatus(self)
        if self.status.get() == target_val:
            st._finished()
            return st

        self._set_st = st
        enums = self.status.enum_strs

        def shutter_cb(value, timestamp, **kwargs):
            try:
                value = enums[int(value)]
            except (ValueError, TypeError):
                # value is already a str -- use as-is
                ...
            if value == target_val:
                self._set_st = None
                self.status.clear_sub(shutter_cb)
                st._finished()

        cmd_enums = cmd_sig.enum_strs
        count = 0

        def cmd_retry_cb(value, timestamp, **kwargs):
            nonlocal count
            try:
                value = cmd_enums[int(value)]
            except (ValueError, TypeError):
                ...
            count += 1
            if count > self.MAX_ATTEMPTS:
                cmd_sig.clear_sub(cmd_retry_cb)
                self._set_st = None
                self.status.clear_sub(shutter_cb)
                st._finished(success=False)
            if value == "None":
                if not st.done:
                    time.sleep(self.RETRY_PERIOD)
                    cmd_sig.set(actuate)
                    ts = datetime.datetime.fromtimestamp(timestamp).strftime(_time_fmtstr)
                    if count > 2:
                        print("** ({}) Had to reactuate {} while {}ing".format(
                            ts, self.name, val if val != "Close" else val[:-1]))
                else:
                    cmd_sig.clear_sub(cmd_retry_cb)

        cmd_sig.subscribe(cmd_retry_cb, run=False)
        self.status.subscribe(shutter_cb)
        cmd_sig.set(actuate)

        return st


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
