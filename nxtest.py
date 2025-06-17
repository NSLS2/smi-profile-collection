# from utils import startup
# startup()

from nexus.device import SimMotor, Mono, MonoWithGratingCpt
from ophyd.sim import det
from bluesky import RunEngine
from bluesky.callbacks.json_writer import JSONWriter
import bluesky.plans as bp
import json
import os
import types
import h5py
import numpy as np
import ast
from ophyd.sim import motor

from bluesky_nexus.preprocessors.supplemental_metadata import SupplementalMetadata
from bluesky_nexus.callbacks.nexus_writer import NexusWriter
from bluesky.preprocessors import SupplementalData, baseline_wrapper
from bluesky_nexus.common.logging_utils import setup_nx_logger, logging


RE = RunEngine({})

# Add and subscribe JSON Writer
jw = JSONWriter("./nexus/runs", "test_run.json")
RE.subscribe(jw)

# Define the devices
mono = Mono(name="mono")
mono_with_grating_cpt = MonoWithGratingCpt(name="mono_with_grating_cpt")
sim_motor = SimMotor(name="sim_motor")

devices_dictionary = {
        "mono": mono,
        "mono_with_grating_cpt": mono_with_grating_cpt,
        "sim_motor": sim_motor,
    }
baseline = [devices_dictionary["mono"], devices_dictionary["mono_with_grating_cpt"]]


# Define preprocesor for the baseline
class SupplementalDataBaseline(SupplementalData):

    def __call__(self, plan):
        plan = baseline_wrapper(plan, self.baseline)
        return (yield from plan)

def execute_scan_plan(
    RE: RunEngine,
    md: dict,
    detectors: list[object],
    motor: object,
    nsteps: int,
):
    """
    Helper function to define and execute a plan on the RunEngine.
    - Scans detectors over a motor's range with given metadata.
    """

    def scan_plan():
        plan = bp.scan(
            detectors, motor, 1, 10, nsteps, md=md
        )  # Start, stop, steps
        assert isinstance(
            plan, types.GeneratorType
        ), "scan() is not returning a generator!"
        yield from plan

    RE(scan_plan())


# Attach preprocessors to the RunEngine

# Add metadata for baseline devices
sdd = SupplementalDataBaseline(baseline=baseline)
RE.preprocessors.append(sdd)

# Add Nexus metadata to the Start document
pproc_nx = SupplementalMetadata()
pproc_nx.devices_dictionary = devices_dictionary
pproc_nx.md_type = SupplementalMetadata.MetadataType.NEXUS_MD
RE.preprocessors.append(pproc_nx)

# # Add device metadata to the Start document
# pproc_dv = SupplementalMetadata()
# pproc_dv.devices_dictionary = devices_dictionary
# pproc_dv.md_type = SupplementalMetadata.MetadataType.DEVICE_MD
# RE.preprocessors.append(pproc_dv)

# Subscribe NexusWriter
nw = NexusWriter(nx_file_dir_path="./nexus")
RE.subscribe(nw)

# Generate metadata
nx_file_name: str = "test_file.nxs"
nx_file_path: str = f"./nexus/{nx_file_name}"
md = {
        "nx_file_name": nx_file_name,
        "title": "bluesky run test 1",
        "definition": "NX_abc",
        "test_dict": {"a": 1, "b": 2, "c": {"d": 3, "e": 4}},
    }
nsteps = 10  # Number of steps in the scan

# This is an optional setting of the NeXus logger. If the setting is not defined, logging to a log file is deactivated.
nx_log_file_dir_path = "./nexus/logs"
setup_nx_logger(
    level=logging.INFO,
    log_file_dir_path=nx_log_file_dir_path,
    max_file_size=2 * 1024 * 1024,
    backup_count=5,
)

execute_scan_plan(RE, md, [devices_dictionary["mono"].en], motor, nsteps)


f = h5py.File(nx_file_path, "r")
# Print the contents of the NeXus file
def print_nexus_file_contents(group, indent=0):
    for key in group.keys():
        item = group[key]
        print(" " * indent + str(key) + ": " + str(item))
        if isinstance(item, h5py.Group):
            print_nexus_file_contents(item, indent + 2)

print_nexus_file_contents(f)