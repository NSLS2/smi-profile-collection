from ophyd import (EpicsMotor,
                   EpicsSignalRO,
                   EpicsSignal,
                   Device,
                   Component as Cpt,
                   PseudoPositioner)

from .crl_optics import CRLModel, DEFAULT_HOLDERS


class CRL(Device):
    """CRL motors plus hardware-independent inventory and focus calculations.

    Energies for the optics helpers are explicitly in keV. These helpers do
    not read motor positions, connect to EPICS, or issue motion commands.
    """

    lens1 = Cpt(EpicsMotor, "L1}Mtr")
    lens2 = Cpt(EpicsMotor, "L2}Mtr")
    lens3 = Cpt(EpicsMotor, "L3}Mtr")
    lens4 = Cpt(EpicsMotor, "L4}Mtr")
    lens5 = Cpt(EpicsMotor, "L5}Mtr")
    lens6 = Cpt(EpicsMotor, "L6}Mtr")
    lens7 = Cpt(EpicsMotor, "L7}Mtr")
    lens8 = Cpt(EpicsMotor, "L8}Mtr")
    lens9 = Cpt(EpicsMotor, "L9}Mtr")
    lens10 = Cpt(EpicsMotor, "L10}Mtr")
    lens11 = Cpt(EpicsMotor, "L11}Mtr")
    lens12 = Cpt(EpicsMotor, "L12}Mtr")
    x = Cpt(EpicsMotor, "X}Mtr")
    y = Cpt(EpicsMotor, "Y}Mtr")
    z = Cpt(EpicsMotor, "Z}Mtr")
    ph = Cpt(EpicsMotor, "Ph}Mtr")
    th = Cpt(EpicsMotor, "Th}Mtr")

    @property
    def lens_inventory(self):
        """Immutable holder records, including nominal IN/OUT positions (mm)."""
        return DEFAULT_HOLDERS

    def recommend_focus(self, energy_keV, *, geometry=None):
        """Return the fewest-holder solution; raise if focus is unreachable.

        ``geometry`` may be a CRLGeometry with calibrated sample distance,
        working travel limits, and incident curvature. Defaults are provisional:
        sample at 615 mm, Z=-50..250 mm, collimated input. Calculates only.
        """
        model = CRLModel() if geometry is None else CRLModel(geometry)
        return model.recommend(energy_keV)

    def focus_candidates(self, energy_keV, *, geometry=None):
        """Return all feasible solutions ranked by holder count, then elements."""
        model = CRLModel() if geometry is None else CRLModel(geometry)
        return model.candidates(energy_keV)

    def focal_length(self, energy_keV, holders):
        """Calculate effective focal length in mm for explicit holder numbers."""
        return CRLModel().focal_length_mm(energy_keV, holders)

# aperture motors, see 10-slits.py
