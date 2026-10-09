"""Hardware-independent, provisional thin-lens model for the SMI CRLs.

Energy arguments are keV; motor positions and image distances are mm. Radii
are per-surface radii for *two-sided* parabolic lenses. The refractive decrement
uses the free-electron approximation, not tabulated dispersion.
See docs/CRL_MICROFOCUSING.md for assumptions and calibration requirements.
"""

from dataclasses import dataclass, field
from itertools import combinations
from math import isfinite, pi, sqrt


ENERGY_RANGE_KEV = (2.1, 24.0)
MEASURED_SAMPLE_DISTANCE_AT_Z0_MM = 1600.0
SSA_DISTANCE_AT_Z0_M = 10.5  # Upstream of the CRL center at crl.z=0.
DEFAULT_INCIDENT_CURVATURE_PER_M = 1 / SSA_DISTANCE_AT_Z0_M
BERYLLIUM_DENSITY_G_CM3 = 1.848
DIAMOND_DENSITY_G_CM3 = 3.515
MATERIALS = {
    "Be": (BERYLLIUM_DENSITY_G_CM3, 9.0121831, 4),
    "diamond": (DIAMOND_DENSITY_G_CM3, 12.011, 6),
}


def _finite(value, name):
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _energy(energy_keV):
    energy = _finite(energy_keV, "energy_keV")
    if not ENERGY_RANGE_KEV[0] <= energy <= ENERGY_RANGE_KEV[1]:
        raise ValueError("energy_keV must be between 2.1 and 24.0")
    return energy


def _delta_from_composition(energy_keV, *, density_g_cm3, atomic_weight_g_mol,
                            electrons_per_atom):
    """Approximate delta = r_e lambda^2 n_e / (2 pi)."""
    energy = _energy(energy_keV)
    density = _finite(density_g_cm3, "density_g_cm3")
    atomic_weight = _finite(atomic_weight_g_mol, "atomic_weight_g_mol")
    electrons = _finite(electrons_per_atom, "electrons_per_atom")
    if density <= 0:
        raise ValueError("density_g_cm3 must be positive")
    if atomic_weight <= 0:
        raise ValueError("atomic_weight_g_mol must be positive")
    if electrons <= 0:
        raise ValueError("electrons_per_atom must be positive")
    electrons_per_m3 = density * 1e6 / atomic_weight * 6.02214076e23 * electrons
    wavelength_m = 1.2398419843320026e-9 / energy
    return 2.8179403205e-15 * wavelength_m**2 * electrons_per_m3 / (2 * pi)


def material_delta(energy_keV, material):
    """Free-electron refractive decrement for a supported lens material."""
    try:
        density, atomic_weight, electrons = MATERIALS[material]
    except KeyError as exc:
        raise ValueError(f"unknown lens material: {material!r}") from exc
    return _delta_from_composition(
        energy_keV, density_g_cm3=density, atomic_weight_g_mol=atomic_weight,
        electrons_per_atom=electrons,
    )


def beryllium_delta(energy_keV, *, density_g_cm3=BERYLLIUM_DENSITY_G_CM3):
    """Approximate delta for beryllium with neutral-atom f1 = 4.

    Constants: classical electron radius 2.8179403205e-15 m, hc =
    1.2398419843320026e-9 keV m, N_A = 6.02214076e23 mol^-1,
    beryllium atomic weight 9.0121831 g/mol. No absorption/dispersion correction.
    """
    return _delta_from_composition(
        energy_keV, density_g_cm3=density_g_cm3, atomic_weight_g_mol=9.0121831,
        electrons_per_atom=4,
    )


def diamond_delta(energy_keV, *, density_g_cm3=DIAMOND_DENSITY_G_CM3):
    """Approximate delta for diamond with carbon f1 = 6.

    Constants: classical electron radius 2.8179403205e-15 m, hc =
    1.2398419843320026e-9 keV m, N_A = 6.02214076e23 mol^-1,
    carbon atomic weight 12.011 g/mol. No absorption/dispersion correction.
    """
    return _delta_from_composition(
        energy_keV, density_g_cm3=density_g_cm3, atomic_weight_g_mol=12.011,
        electrons_per_atom=6,
    )


@dataclass(frozen=True)
class LensHolder:
    number: int
    count: int = 0
    radius_um: float | None = None
    aperture_mm: float | None = None
    material: str | None = None
    in_mm: float = 0.0

    @property
    def out_mm(self):
        return 10.0 if self.number <= 6 else -10.0

    @property
    def description(self):
        if self.count:
            material = f" {self.material}" if self.material else ""
            return f"{self.count} x {self.radius_um:g} um{material}"
        return (f"{self.aperture_mm:g} mm aperture" if self.aperture_mm
                else "blank / uncharacterized")


DEFAULT_HOLDERS = (
    LensHolder(1, 1, 50, material="Be"),
    LensHolder(2, 8, 50, material="Be"),
    LensHolder(3, 16, 50, material="Be"),
    LensHolder(4, 4, 50, material="Be"),
    LensHolder(5, 2, 50, material="Be"),
    LensHolder(6), LensHolder(7), LensHolder(8),
    LensHolder(9, 1, 200, material="Be"),
    LensHolder(10, 8, 500, material="Be"),
    LensHolder(11, 1, 500, material="Be"),
    LensHolder(12, aperture_mm=2.0),
)
HOLDERS_BY_NUMBER = {h.number: h for h in DEFAULT_HOLDERS}


@dataclass(frozen=True)
class LensCombination:
    holders: tuple[int, ...]
    element_count: int
    strength_per_m: float  # sum(N / R), with R in metres

    @property
    def rank(self):
        """Fewest holders, then elements, then holder numbers (stable tie-break)."""
        return len(self.holders), self.element_count, self.holders


def _combinations():
    populated = [h for h in DEFAULT_HOLDERS if h.count]
    return tuple(sorted((
        LensCombination(
            tuple(h.number for h in group), sum(h.count for h in group),
            sum(h.count / (h.radius_um * 1e-6) for h in group),
        )
        for size in range(1, len(populated) + 1)
        for group in combinations(populated, size)
    ), key=lambda combo: combo.rank))


COMBINATIONS = _combinations()


@dataclass(frozen=True)
class CRLGeometry:
    """Common lens plane, sample fixed downstream from the Z=0 lens plane.

    Positive Z moves downstream. ``incident_curvature_per_m`` is ray slope /
    ray height at Z=0: zero = collimated, positive = diverging, negative =
    converging. At Z it propagates as C(Z) = C(0)/(1 + C(0)*Z[m]).
    This is geometrical wavefront curvature, not angular divergence/emittance.
    Default: SSA secondary source 10.5 m upstream of the CRL center at Z=0,
    so source distance p(Z) = 10.5 + Z[m]. Set curvature=0 for collimated input.
    """

    sample_distance_mm: float = MEASURED_SAMPLE_DISTANCE_AT_Z0_MM
    z_min_mm: float = -300.0
    z_max_mm: float = 300.0
    incident_curvature_per_m: float = DEFAULT_INCIDENT_CURVATURE_PER_M

    def __post_init__(self):
        for name in ("sample_distance_mm", "z_min_mm", "z_max_mm",
                     "incident_curvature_per_m"):
            object.__setattr__(self, name, _finite(getattr(self, name), name))
        if self.z_min_mm >= self.z_max_mm:
            raise ValueError("z_min_mm must be less than z_max_mm")
        if self.sample_distance_mm <= self.z_max_mm:
            raise ValueError("sample must be downstream of the entire Z range")
        c = self.incident_curvature_per_m
        if min(1 + c * z / 1000 for z in (self.z_min_mm, self.z_max_mm)) <= 0:
            raise ValueError("incident beam crosses its focus within/before the Z range")

    def required_power_per_m(self, z_mm):
        z = z_mm / 1000
        c = self.incident_curvature_per_m
        return 1 / (self.sample_distance_mm / 1000 - z) + c / (1 + c * z)

    def power_range_per_m(self):
        positions = [self.z_min_mm, self.z_max_mm]
        c = self.incident_curvature_per_m
        if c:
            stationary = (c * self.sample_distance_mm / 1000 - 1) / (2 * c) * 1000
            if self.z_min_mm < stationary < self.z_max_mm:
                positions.append(stationary)
        powers = [self.required_power_per_m(z) for z in positions]
        return min(powers), max(powers)

    def focus_positions_mm(self, power_per_m):
        """All real, in-travel conjugates; solve the propagated-curvature quadratic."""
        p = power_per_m
        c = self.incident_curvature_per_m
        d = self.sample_distance_mm / 1000
        if c == 0:
            distances = [1 / p]
        else:
            a = 1 + c * d
            discriminant = a * a - 4 * c * a / p
            if discriminant < 0 or a == 0:
                return ()
            root = sqrt(discriminant)
            # Stable small root, plus the second conjugate (usually far outside travel).
            denominator = a + root if a >= 0 else a - root
            distances = [2 * a / (p * denominator), denominator / (2 * c)]
        positions = []
        for q in distances:
            z = (d - q) * 1000
            if q > 0 and self.z_min_mm - 1e-8 <= z <= self.z_max_mm + 1e-8:
                z = min(self.z_max_mm, max(self.z_min_mm, z))
                if not any(abs(z - previous) < 1e-8 for previous in positions):
                    positions.append(z)
        return tuple(sorted(positions))


@dataclass(frozen=True)
class FocusSolution:
    energy_keV: float
    holders: tuple[int, ...]
    element_count: int
    focal_length_mm: float
    image_distance_mm: float
    z_mm: float
    z_margin_mm: float


class NoFocusSolution(ValueError):
    """No nonempty lens combination focuses at the sample inside the Z range."""


@dataclass(frozen=True)
class SelectionBand:
    energy_min_keV: float
    energy_max_keV: float
    holders: tuple[int, ...] | None  # None denotes an unreachable interval


@dataclass(frozen=True)
class CRLModel:
    geometry: CRLGeometry = field(default_factory=CRLGeometry)

    def __post_init__(self):
        for holder in DEFAULT_HOLDERS:
            if holder.count:
                material_delta(10, holder.material)

    def delta(self, energy_keV, material):
        return material_delta(energy_keV, material)

    def _combination_for_holders(self, holders):
        ids = tuple(sorted(holders))
        combo = next((c for c in COMBINATIONS if c.holders == ids), None)
        if combo is None:
            raise ValueError("select a nonempty, unique subset of lens holders 1-5, 9-11")
        return combo

    def _combination_power_per_m(self, energy_keV, combo):
        energy = _energy(energy_keV)
        return sum(
            2 * self.delta(energy, HOLDERS_BY_NUMBER[number].material)
            * HOLDERS_BY_NUMBER[number].count
            / (HOLDERS_BY_NUMBER[number].radius_um * 1e-6)
            for number in combo.holders
        )

    def power_per_m(self, energy_keV, holders):
        """Effective focusing power in 1/m for explicit holder numbers."""
        combo = self._combination_for_holders(holders)
        return self._combination_power_per_m(energy_keV, combo)

    def focal_length_mm(self, energy_keV, holders):
        """Effective focal length; reject empty holders/aperture/duplicate IDs."""
        return 1000 / self.power_per_m(energy_keV, holders)

    def candidates(self, energy_keV):
        """Feasible solutions ordered by holder count, elements, IDs, then Z margin."""
        energy = _energy(energy_keV)
        g = self.geometry
        solutions = []
        for combo in COMBINATIONS:
            power = self._combination_power_per_m(energy, combo)
            positions = sorted(g.focus_positions_mm(power), key=lambda z: (
                -min(z - g.z_min_mm, g.z_max_mm - z), z))
            for z in positions:
                solutions.append(FocusSolution(
                    energy, combo.holders, combo.element_count, 1000 / power,
                    g.sample_distance_mm - z, z,
                    min(z - g.z_min_mm, g.z_max_mm - z),
                ))
        return tuple(solutions)

    def recommend(self, energy_keV):
        """Calculate only: raise NoFocusSolution rather than clamp unreachable Z."""
        solutions = self.candidates(energy_keV)
        if not solutions:
            raise NoFocusSolution(
                f"No CRL combination focuses at {energy_keV:g} keV within "
                f"Z=[{self.geometry.z_min_mm:g}, {self.geometry.z_max_mm:g}] mm"
            )
        return solutions[0]

    def combination_energy_range(self, combo):
        """Analytic reachable interval, clipped to 2.1-24 keV; None if absent."""
        low_power, high_power = self.geometry.power_range_per_m()
        if high_power <= 0:
            return None
        coefficient = self._combination_power_per_m(10, combo) * 10**2
        low = max(ENERGY_RANGE_KEV[0], sqrt(coefficient / high_power))
        high = min(ENERGY_RANGE_KEV[1], sqrt(coefficient / low_power)
                   if low_power > 0 else float("inf"))
        return (low, high) if low <= high else None

    def selection_bands(self):
        """Exact switch/gap intervals for this E^-2 model, not sampled coverage.

        Values at a shared boundary should be obtained with recommend(), since
        both adjacent combinations may be feasible exactly at the boundary.
        """
        boundaries = set(ENERGY_RANGE_KEV)
        for combo in COMBINATIONS:
            interval = self.combination_energy_range(combo)
            if interval:
                boundaries.update(interval)
        boundaries = sorted(boundaries)
        bands = []
        for low, high in zip(boundaries, boundaries[1:]):
            solutions = self.candidates((low + high) / 2)
            holders = solutions[0].holders if solutions else None
            if bands and bands[-1].holders == holders:
                bands[-1] = SelectionBand(bands[-1].energy_min_keV, high, holders)
            else:
                bands.append(SelectionBand(low, high, holders))
        return tuple(bands)
