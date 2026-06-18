
import warnings
from time import ctime
from smi_beamline.devices.pilatus import SAXSPositions, FakeDetector, SAXS_Detector, WAXS_Detector, set_energy_cam
from smibase.waxschamber import chamber_pressure
from smibase.shutter import shopen, shclose
from .amptek import amptek
from .energy import energy
from smi_beamline.devices.waxschamber import Sample_Chamber
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import EpicsSignal, Device, Component

# Packages needed to restart camserver
import telnetlib
import paramiko
import time

from smi_beamline.devices import _context

def det_exposure_time(exp_t, meas_t=1, period_delay=0.001):
    """
    Set the exposure time / image count on the Pilatus 2M and 900KW
    (and the Amptek, when present) as a Bluesky **plan**.

    exp_t: single-image exposure time (s)
    meas_t: total measurement time (s); ``num_images = int(meas_t / exp_t)``
    period_delay: added to ``exp_t`` to form the acquire period (s)

    This is a plan (Tenet 5: plans contain only messages). Use it as
    ``yield from det_exposure_time(...)`` inside another plan, or
    ``RE(det_exposure_time(...))`` at the prompt. The two-pass set is preserved
    from the original implementation: the Pilatus occasionally drops the first
    acquire-time write when switching burst mode, so we set everything twice.
    """
    num_images = int(meas_t / exp_t)
    for _ in range(2):
        args = [
            pil2M.cam.acquire_time, exp_t,
            pil2M.cam.acquire_period, exp_t + period_delay,
            pil2M.cam.num_images, num_images,
            pil900KW.cam.acquire_time, exp_t,
            pil900KW.cam.acquire_period, exp_t + period_delay,
            pil900KW.cam.num_images, num_images,
        ]
        if amptek_det is not None:
            args += [amptek.mca.preset_real_time, exp_t]
        yield from bps.mv(*args)


def det_exposure_time_sync(exp_t, meas_t=1, period_delay=0.001):
    """DEPRECATED blocking version of :func:`det_exposure_time`.

    ``det_exposure_time`` is now a Bluesky plan (Tenet 5); call it via
    ``RE(det_exposure_time(...))`` or ``yield from det_exposure_time(...)``.
    This thin shim preserves the old synchronous ``.set()`` behaviour for any
    out-of-tree caller that cannot run a plan. It will be removed.
    """
    warnings.warn(
        "det_exposure_time is now a Bluesky plan; use "
        "RE(det_exposure_time(...)) or `yield from det_exposure_time(...)`. "
        "det_exposure_time_sync is a deprecated blocking shim and will be removed.",
        DeprecationWarning,
        stacklevel=2,
    )
    num_images = int(meas_t / exp_t)
    for _ in range(2):
        waits = [
            pil2M.cam.acquire_time.set(exp_t),
            pil2M.cam.acquire_period.set(exp_t + period_delay),
            pil2M.cam.num_images.set(num_images),
            pil900KW.cam.acquire_time.set(exp_t),
            pil900KW.cam.acquire_period.set(exp_t + period_delay),
            pil900KW.cam.num_images.set(num_images),
        ]
        if amptek_det is not None:
            waits.append(amptek.mca.preset_real_time.set(exp_t))
        for w in waits:
            w.wait()

def det_next_file(n):
    pil2M.cam.file_number.put(n)
    pil900KW.cam.file_number.put(n)
    
    #Keep this commented for now but should be removed
    # pil300KW.cam.file_number.put(n)
    # rayonix.cam.file_number.put(n)


fd = FakeDetector(name="fd")


#Keep this commented for now but should be removed
# pil300KW = None
amptek_det = None


#####################################################
# Pilatus 900KW definition

pil900KW = WAXS_Detector("XF:12IDC-ES:2{Det:900KW}", name="pil900KW", asset_path="pilatus900kw-1")
pil900KW.set_primary_roi(1)

pil900kwroi1 = EpicsSignal("XF:12IDC-ES:2{Det:900KW}Stats1:Total_RBV", name="pil900kwroi1")
pil900kwroi2 = EpicsSignal("XF:12IDC-ES:2{Det:900KW}Stats2:Total_RBV", name="pil900kwroi2")
pil900kwroi3 = EpicsSignal("XF:12IDC-ES:2{Det:900KW}Stats3:Total_RBV", name="pil900kwroi3")
pil900kwroi4 = EpicsSignal("XF:12IDC-ES:2{Det:900KW}Stats4:Total_RBV", name="pil900kwroi4")

pil900KW.stats1.kind = "hinted"
pil900KW.stats1.total.kind = "hinted"
pil900KW.cam.num_images.kind = "config"
pil900KW.cam.kind = 'normal'
pil900KW.cam.file_number.kind = 'normal'
pil900KW.cam.ensure_nonblocking()
pil900KW.motors.kind='normal'
pil900KW.motors.arc.user_readback.name='waxs_arc'
pil900KW.motors.bs_x.user_readback.name='waxs_bsx'
pil900KW.motors.bs_y.user_readback.name='waxs_bsy'
pil900KW.pixel_size_mm.kind='config'
pil900KW.sdd_mm.kind='config' 
pil900KW.beam_center_x_px.kind='config'
pil900KW.beam_center_y_px.kind='config'
pil900KW.motors.arc.user_readback.kind = 'normal'
pil900KW.motors.bs_x.user_readback.kind = 'normal'
pil900KW.motors.bs_y.user_readback.kind = 'normal'



#####################################################
# Pilatus 1M definition  
#pil1M = Pilatus("XF:12IDC-ES:2{Det:1M}", name="pil1M", asset_path="pilatus1m-1")  # , detector_id="SAXS")
pil2M = SAXS_Detector("XF:12ID2-ES{Pilatus:Det-2M}", name="pil2M", asset_path="pilatus2m-1")  # , detector_id="SAXS")
pil2M.set_primary_roi(1)

pil2m_pos = pil2M.motor
# Capitalized alias: smi_plans' _qserver DEVICE_REGISTRY / SDD specs reference this as ``pil2M_pos``
# (matching the ``pil2M`` detector casing).  Same object; keeps both spellings resolvable so the
# smi-plans spec wrappers (acquire_from_spec, commissioning AgBH, ...) find the SDD translation.
pil2M_pos = pil2m_pos

for detpos in [pil2m_pos]:
    detpos.configuration_attrs = detpos.read_attrs

pil2mroi1 = EpicsSignal("XF:12ID2-ES{Pilatus:Det-2M}Stats1:Total_RBV", name="pil2mroi1")
pil2mroi2 = EpicsSignal("XF:12ID2-ES{Pilatus:Det-2M}Stats2:Total_RBV", name="pil2mroi2")
pil2mroi3 = EpicsSignal("XF:12ID2-ES{Pilatus:Det-2M}Stats3:Total_RBV", name="pil2mroi3")
pil2mroi4 = EpicsSignal("XF:12ID2-ES{Pilatus:Det-2M}Stats4:Total_RBV", name="pil2mroi4")

pil2M.stats1.kind = "hinted"
pil2M.stats1.total.kind = "hinted"
pil2M.cam.num_images.kind = "config"
pil2M.cam.kind = 'config'
pil2M.cam.file_number.kind = 'config'
pil2M.cam.ensure_nonblocking()
pil2M.active_beamstop.kind='config'
pil2M.motor.kind='config'
pil2M.beamstop.kind='config'
pil2M.beam_center_x_px.kind='config'
pil2M.beam_center_y_px.kind='config'


waxs = pil900KW.motors # for backwards compatibility
waxs.kind='normal'

def multi_count(detectors, *args, **kwargs):
    delay = detectors[0].cam.num_images.get() * detectors[0].cam.acquire_time.get() + 1
    yield from bp.count(detectors, *args, delay=delay, **kwargs)

_context.baseline_register([pil2m_pos,waxs,pil2M.active_beamstop,pil2M.beam_center_x_px,pil2M.beam_center_y_px])


# This needs to be remove because not used
 # TODO: ELIOT - change save to redis
def beamstop_save():
    """
    Save the current configuration
    this is now in the mdsave dictionary not in a file anymore
    """
    pil2M.save_beamstop()


# SSH connection details
hostname = 'xf12id2-det3'
username = 'det'
password = 'Pilatus2'

# Create an SSH client
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
telnet_command = 'telnet localhost 20002'

#ToDo need to add the good threshold in the restart function> It currently run the default from the camserver
def restartWAXS():
    try:
        # Connect to the SSH server
        client.connect(hostname=hostname,username=username, password=password)

        command_to_run = './start_camserver'  # Replace this with your desired command
        stdin, stdout, stderr = client.exec_command(command_to_run)

        # Start an interactive shell session
        ssh_shell = client.invoke_shell()

        # Send the Telnet command to the shell
        ssh_shell.send(telnet_command + '\n')

        # Create a Telnet session on the SSH server
        tn = telnetlib.Telnet()

        # Attach the shell transport to the Telnet session
        tn.sock = ssh_shell

        ssh_shell.send('\x18\x18')
        # Read and monitor the output of the Telnet command

        start_time=time.time()
        completed = False
        while time.time()-start_time<120:
            output = tn.read_very_eager().decode()
            if output:
                # print(output)
                if 'Set detector gap-fill to: -1' in output:
                    yield from bps.sleep(3)
                    print('Detector up and running')
                    completed = True
                    break

            # Check if the Telnet connection is closed
            if tn.eof:
                print('Connection failed. Either Detector is not on or chamber not pumped')
                break
        
        if not completed:
            print('something went wrong, the detector is not ready to use')
        
        # Close the SSH connection
        client.close()

    finally:
        # Close the SSH connection
        client.close()



#restartWAXS after pumping the vacuum below 0.5mbar
def startWAXS():
    #telnet and restart camserver
    yield from restartWAXS()

    #Reset exposure time and acquire period qdter tyurning on the detector
    yield from det_exposure_time(0.5, 0.5)

    #set the energy and threshold
    pil900KW.cam.threshold_apply.put(1)

    # ToDo: Confirm if the default value saved in camserver are well loaded
    # to add - set energy of the camera to the current beamline energy
    #set_energy_cam(pil900KW.cam,energy.get())

def set_energy(en_ev, thresh_ev=None, gain=1):
    energy.move(en_ev)
    set_energy_cam(pil900KW.cam, en_ev, thresh_ev=thresh_ev, gain=gain)
    set_energy_cam(pil2M.cam, en_ev, thresh_ev=thresh_ev, gain=gain)


# def check_condition():
#     #TODO: check if the pressure in the chamber is low enough or if the 900KW power is enabled

def pump_waxs():
    print(f'starting chamber pumping - this can take ~10-15 minutes')
    # perform the autopumping routine
    yield from chamber_pressure.pump_and_wait(verbose=False)
    print('starting the WAXS detector - this can take a couple minutes')
    yield from startWAXS()

def vent_waxs():
    print(f'starting chamber venting - this can take 5-10 minutes')
    yield from chamber_pressure.vent()


