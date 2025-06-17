from ophyd import Component as Cpt
from ophyd import Device, Signal
from ophyd.sim import SynAxis
from bluesky_nexus.common.decorator_utils import NxSchemaLoader
from ophyd.sim import motor
import dataclasses


# Class simulating metadata of SimMotor
@dataclasses.dataclass
class MetadataSimMotor:
    worldPosition: dict = dataclasses.field(default_factory= lambda: {
        "x": "1.2000000000000003",
        "y": "4.5000000000000006",
        "z": "7.8000000000000009",
    })
    description: str = "I am a simulated motor"
    baseline: bool = True

    def get_attributes(self):
        dataclasses.asdict(self)


class SimMotor(motor.__class__):  # or simply: class SimMotor(type(motor)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.md = MetadataSimMotor()


# Class simulating metadata of monochromator
@dataclasses.dataclass
class MetadataMono:
    grating_substrate_material: str = "lead"
    worldPosition: dict = dataclasses.field(default_factory= lambda: {
        "x": "1.2000000000000003",
        "y": "4.5000000000000006",
        "z": "7.8000000000000009",
    })
    description: str = "I am the best mono at the bessyii facility"
    calibration_on: bool = True
    baseline: str = "True"
    transformations_axisname: str = "x"

    def get_attributes(self):
        dataclasses.asdict(self)

# Class simulating metadata of monochromator with grating component
@dataclasses.dataclass
class MetadataMonoWithGratingCpt:
    grating_substrate_material: str = "leadless"
    worldPosition: dict = dataclasses.field(default_factory= lambda: {
        "x": "11.120000013",
        "y": "14.150000016",
        "z": "17.180000019",
    })
    description: str = "I am the best mono with grating cpt at the bessyii facility"
    baseline: str = "True"

    def get_attributes(self):
        dataclasses.asdict(self)


# Class simulating grating component of monochromator
class Grating(Device):
    diffraction_order: Signal = Cpt(Signal, name="diff_order")


# Class simulating monochromator with grating component
@NxSchemaLoader("./nexus/schemas/monochromator_with_grating.yaml")
class MonoWithGratingCpt(Device):
    grating: Grating = Cpt(Grating, name="grating")
    engry: SynAxis = Cpt(SynAxis, name="engry")
    slit: Signal = Cpt(Signal, name="slit")
    md = MetadataMonoWithGratingCpt()

# Class simulating monochromator
@NxSchemaLoader("./nexus/schemas/monochromator.yaml")
class Mono(Device):
    en: SynAxis = Cpt(SynAxis, name="en")
    grating: Signal = Cpt(Signal, name="grating")
    slit: Signal = Cpt(Signal, name="slit", kind="config")
    md = MetadataMono()