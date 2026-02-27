
from ophyd import Device, EpicsSignal, Component as Cpt
import bluesky.plan_stubs as bps
#from .shutter import TwoButtonShutter
from nslsii.devices import TwoButtonShutter

class Valve(TwoButtonShutter):
    def stop(self,*,success=False):
        ...

# Read the pressure from the waxs chamber
class Sample_Chamber(Device):
    waxs = Cpt(EpicsSignal, "XF:12IDC-VA:2{Det:300KW-TCG:7}P:Raw-I")  # Change PVs
    maxs = Cpt(EpicsSignal, "XF:12IDC-VA:2{B1:WAXS-TCG:9}P:Raw-I")  # Change PVs

    svent_valve = Cpt(Valve, 'XF:12IDC-VA:2{Det:300KW-VVSoft:WAXS}')
    fvent_valve = Cpt(Valve, 'XF:12IDC-VA:2{Det:300KW-VV:WAXS}')
    air_valve = Cpt(Valve, 'XF:12IDC-PU{Air-Vlv:Supply}')
    N2_valve = Cpt(Valve, 'XF:12IDC-PU{N2-Vlv:Supply}')
    turbo_valve = Cpt(Valve, 'XF:12IDC-PU{Air-Vlv:Supply}')
    turbo_cooling_valve = Cpt(Valve, 'XF:12IDC-PU{PCHW-Vlv:Supply}')
    turbo_enable = Cpt(EpicsSignal, 'XF:12IDC-VA:2{Det:300KW-TMP:1}OnOff',put_complete=False)
    det_power = Cpt(EpicsSignal, 'XF:12ID-EPS{PLC}DetOutlet-Cmd',put_complete=False)
    vent_safe = Cpt(EpicsSignal, 'XF:12ID2-ES{AutoBleed}Plus-Cmd',put_complete=False,string=True)
    

    def vent(self):
        yield from bps.mv(self.vent_safe,1,timeout=2)

    def pump(self):
        yield from bps.mv(
            self.svent_valve,'Close',
            self.fvent_valve,'Close',
            self.air_valve,'Close',
            self.N2_valve,'Close',timeout=2)
        yield from bps.sleep(1)
        yield from bps.mv(
            self.turbo_valve,'Open',timeout=2)
        yield from bps.sleep(.5)
        yield from bps.mv(
            self.turbo_cooling_valve,'Open',timeout=2)
        yield from bps.sleep(.5)
        yield from bps.mv(
            self.turbo_enable,1,
            self.det_power,1,timeout=2
        )



# evacuate procedure from css
# soft vent valve close         XF:12IDC-VA:2{Det:300KW-VVSoft:WAXS}Cmd:Cls-Cmd - 1     timeout 10
# full vent valve close         XF:12IDC-VA:2{Det:300KW-VV:WAXS}Cmd:Cls-Cmd     - 1     timeout 10
# air supply close              XF:12IDC-PU{Air-Vlv:Supply}Cmd:Cls-Cmd          - 1     timeout 10
# N2 supply close               XF:12IDC-PU{N2-Vlv:Supply}Cmd:Cls-Cmd           - 1     timeout 10
# pump port open                XF:12IDC-VA:2{Det:300KW-IV:1}Cmd:Opn-Cmd        - 1     timeout 10
# pump cooling water valve      XF:12IDC-PU{PCHW-Vlv:Supply}Cmd:Opn-Cmd         - 1     timeout 10
# turbo pump on                 XF:12IDC-VA:2{Det:300KW-TMP:1}OnOff             - 1     timeout 10
# detector power enable         XF:12ID-EPS{PLC}DetOutlet-Cmd                   - 1     timeout 10

