print(f"Loading {__file__}")

from time import ctime
from smiclasses.pilatus import SAXSPositions, FakeDetector, SAXS_Detector, WAXS_Detector, set_energy_cam
from .amptek import amptek
from .energy import energy
from smiclasses.waxschamber import Sample_Chamber
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import EpicsSignal, Device, Component


def det_exposure_time(exp_t, meas_t=1, period_delay=0.001):
    """
    Waits broke pilatus exposure set when setting burst mode
    and hitting ctrl+c
    """

    try:
        for j in range(2):
            waits = []
            waits.append(pil2M.cam.acquire_time.set(exp_t))
            waits.append(pil2M.cam.acquire_period.set(exp_t + period_delay))
            waits.append(pil2M.cam.num_images.set(int(meas_t / exp_t)))
            if pil300KW is not None:
                waits.append(pil300KW.cam.acquire_time.set(exp_t))
                waits.append(pil300KW.cam.acquire_period.set(exp_t + period_delay))
                waits.append(pil300KW.cam.num_images.set(int(meas_t / exp_t)))
            waits.append(pil900KW.cam.acquire_time.set(exp_t))
            waits.append(pil900KW.cam.acquire_period.set(exp_t + period_delay))
            waits.append(pil900KW.cam.num_images.set(int(meas_t / exp_t)))
            waits.append(amptek.mca.preset_real_time.put(exp_t))

            for w in waits:
                w.wait()
    except:
        print('Problem with new exposure set, using old method')
        pil2M.cam.acquire_time.put(exp_t)
        pil2M.cam.acquire_period.put(exp_t + period_delay)
        pil2M.cam.num_images.put(int(meas_t / exp_t))
        pil900KW.cam.acquire_time.put(exp_t)
        pil900KW.cam.acquire_period.put(exp_t + period_delay)
        pil900KW.cam.num_images.put(int(meas_t / exp_t))


def det_exposure_time_old(exp_t, meas_t=1):
    """
    The above broke, using old version as weekend workaround
    """
    for j in range(2):
        pil2M.cam.acquire_time.put(exp_t)
        pil2M.cam.acquire_period.put(exp_t + 0.001)
        pil2M.cam.num_images.put(int(meas_t / exp_t))
        pil900KW.cam.acquire_time.put(exp_t)
        pil900KW.cam.acquire_period.put(exp_t + 0.001)
        pil900KW.cam.num_images.put(int(meas_t / exp_t))



def det_next_file(n):
    pil2M.cam.file_number.put(n)
    pil900KW.cam.file_number.put(n)
    if pil300KW is not None:
        pil300KW.cam.file_number.put(n)
    # rayonix.cam.file_number.put(n)



fd = FakeDetector(name="fd")




pil300KW = None


#####################################################
# Pilatus 900KW definition

pil900KW = WAXS_Detector("XF:12IDC-ES:2{Det:900KW}", name="pil900KW", asset_path="pilatus900kw-1")
pil900KW.set_primary_roi(1)

pil900kwroi1 = EpicsSignal(
    "XF:12IDC-ES:2{Det:900KW}Stats1:Total_RBV", name="pil900kwroi1"
)
pil900kwroi1 = EpicsSignal(
    "XF:12IDC-ES:2{Det:900KW}Stats2:Total_RBV", name="pil900kwroi2"
)
pil900kwroi1 = EpicsSignal(
    "XF:12IDC-ES:2{Det:900KW}Stats3:Total_RBV", name="pil900kwroi3"
)
pil900kwroi1 = EpicsSignal(
    "XF:12IDC-ES:2{Det:900KW}Stats4:Total_RBV", name="pil900kwroi4"
)

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

#####################################################
# Pilatus 1M definition  
#pil1M = Pilatus("XF:12IDC-ES:2{Det:1M}", name="pil1M", asset_path="pilatus1m-1")  # , detector_id="SAXS")
pil2M = SAXS_Detector("XF:12ID2-ES{Pilatus:Det-2M}", name="pil2M", asset_path="pilatus2m-1")  # , detector_id="SAXS")
pil2M.set_primary_roi(1)

pil2m_pos = pil2M.motor

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
waxs.kind='config'


def multi_count(detectors, *args, **kwargs):
    delay = detectors[0].cam.num_images.get() * detectors[0].cam.acquire_time.get() + 1
    yield from bp.count(detectors, *args, delay=delay, **kwargs)



from IPython import get_ipython
sd = get_ipython().user_ns['sd']

sd.baseline.extend([pil2m_pos,waxs,pil2M.active_beamstop,pil2M.beam_center_x_px,pil2M.beam_center_y_px])

def beamstop_save():
    """
    Save the current configuration
    """
    # TODO: ELIOT - change save to redis

    # SMI_CONFIG_FILENAME = os.path.join(
    #     get_ipython().profile_dir.location, "smi_config.csv"
    # )

    # Beamstop position in x and y
    bs_rod_x = pil2M.beamstop.x_rod.position
    bs_rod_y = pil2M.beamstop.y_rod.position

    bs_pin_x = pil2M.beamstop.x_pin.position
    bs_pin_y = pil2M.beamstop.y_pin.position

    # collect the current positions of motors
    current_config = {
        "bs_rod_x": bs_rod_x,
        "bs_rod_y": bs_rod_y,
        "bs_pin_x": bs_pin_x,
        "bs_pin_y": bs_pin_y,
        "time": ctime(),
    }

    if pil2M.active_beamstop.get() == 'rod':
        pil2M.rod_offset_x_mm.set(bs_rod_x)
        pil2M.rod_offset_y_mm.set(bs_rod_y)
        print(f"resetting the rod offsets to {bs_rod_x}, {bs_rod_y}")
    elif pil2M.active_beamstop.get() == 'pin':
        pil2M.pd_offset_x_mm.set(bs_pin_x)
        pil2M.pd_offset_y_mm.set(bs_pin_y)
        print(f"resetting the pin offsets to {bs_pin_x}, {bs_pin_y}")
    else:
        print("No active beamstop selected, not resetting offsets\n")
        print("Please run pil2M.insert_beamstop('rod' or 'pin')\n")

    # TODO - append config to redis


    print(current_config)

# Todo: No module paramiko
import telnetlib
import paramiko
import time

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
    det_exposure_time(0.5, 0.5)

    #set the energy and threshold
    pil900KW.cam.threshold_apply.put(1)

    # ToDo: Confirm if the default value saved in camserver are well loaded
    # to add - set energy of the camera to the current beamline energy
    #set_energy_cam(pil900KW.cam,energy.get())

def set_energy(en_ev, threshold=None, gain=1):
    energy.move(en_ev)
    set_energy_cam(pil900KW.cam, en_ev, thresh_ev=threshold, gain=gain)
    set_energy_cam(pil2M.cam, en_ev, thresh_ev=threshold, gain=gain)


# def check_condition():
#     #TODO: check if the pressure in the chamber is low enough or if the 900KW power is enabled

# def auto_pump():
#     print(f'starting chamber pumping')
#     # TODO: find all of the PVs in the auto pumping routine, and make objects
#     # perform the autopumping routine
#     print(f"Starting periodic check (every {2} seconds)... to wait for chamber to be pumped down")
#     while True:
#         if check_condition():
#             restartWAXS()
#             break  # Exit the loop once the condition is met and action is performed
#         else:
#             print(f"Condition not met. Sleeping for {2} second(s).")
#             time.sleep(2) # Pause the loop for the specified interval





