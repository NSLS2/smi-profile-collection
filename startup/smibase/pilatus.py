print(f"Loading {__file__}")

from ..smiclasses.pilatus import PIL1MPositions, FakeDetector, Pilatus, WAXS
from .amptek import amptek
import bluesky.plans as bp
import bluesky.plan_stubs as bps
from ophyd import EpicsSignal


def det_exposure_time(exp_t, meas_t=1, period_delay=0.001):
    """
    Waits broke pilatus exposure set when setting burst mode
    and hitting ctrl+c
    """

    try:
        for j in range(2):
            waits = []
            waits.append(pil1M.cam.acquire_time.set(exp_t))
            waits.append(pil1M.cam.acquire_period.set(exp_t + period_delay))
            waits.append(pil1M.cam.num_images.set(int(meas_t / exp_t)))
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
        pil1M.cam.acquire_time.put(exp_t)
        pil1M.cam.acquire_period.put(exp_t + 0.001)
        pil1M.cam.num_images.put(int(meas_t / exp_t))
        pil900KW.cam.acquire_time.put(exp_t)
        pil900KW.cam.acquire_period.put(exp_t + 0.001)
        pil900KW.cam.num_images.put(int(meas_t / exp_t))


def det_exposure_time_old(exp_t, meas_t=1):
    """
    The above broke, using old version as weekend workaround
    """
    for j in range(2):
        pil1M.cam.acquire_time.put(exp_t)
        pil1M.cam.acquire_period.put(exp_t + 0.001)
        pil1M.cam.num_images.put(int(meas_t / exp_t))
        pil900KW.cam.acquire_time.put(exp_t)
        pil900KW.cam.acquire_period.put(exp_t + 0.001)
        pil900KW.cam.num_images.put(int(meas_t / exp_t))



def det_next_file(n):
    pil1M.cam.file_number.put(n)
    pil900KW.cam.file_number.put(n)
    if pil300KW is not None:
        pil300KW.cam.file_number.put(n)
    # rayonix.cam.file_number.put(n)



fd = FakeDetector(name="fd")


pil1m_pos = PIL1MPositions("XF:12IDC-ES:2{Det:1M-Ax:", name="detector_saxs_pos")

for detpos in [pil1m_pos]:
    detpos.configuration_attrs = detpos.read_attrs

pil300KW = None


#####################################################
# Pilatus 900KW definition

pil900KW = Pilatus("XF:12IDC-ES:2{Det:900KW}", name="pil900KW", asset_path="pilatus900kw-1")
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



#####################################################
# Pilatus 1M definition

pil1M = Pilatus("XF:12IDC-ES:2{Det:1M}", name="pil1M", asset_path="pilatus1m-1")  # , detector_id="SAXS")
pil1M.set_primary_roi(1)

pil1mroi1 = EpicsSignal("XF:12IDC-ES:2{Det:1M}Stats1:Total_RBV", name="pil1mroi1")
pil1mroi2 = EpicsSignal("XF:12IDC-ES:2{Det:1M}Stats2:Total_RBV", name="pil1mroi2")
pil1mroi3 = EpicsSignal("XF:12IDC-ES:2{Det:1M}Stats3:Total_RBV", name="pil1mroi3")
pil1mroi4 = EpicsSignal("XF:12IDC-ES:2{Det:1M}Stats4:Total_RBV", name="pil1mroi4")

pil1M.stats1.kind = "hinted"
pil1M.stats1.total.kind = "hinted"
pil1M.cam.num_images.kind = "config"
pil1M.cam.kind = 'normal'
pil1M.cam.file_number.kind = 'normal'
pil1M.cam.ensure_nonblocking()


waxs = WAXS("XF:12IDC-ES:2{", name="waxs")



def multi_count(detectors, *args, **kwargs):
    delay = detectors[0].cam.num_images.get() * detectors[0].cam.acquire_time.get() + 1
    yield from bp.count(detectors, *args, delay=delay, **kwargs)



from .base import sd

sd.baseline.extend([pil1m_pos])