# Collection IPython profile
beamline configuration of SMI

## Starting with beam down

For one `bsui` session, disable beam-dependent suspenders at startup with:

```sh
BEAM_DOWN=1 bsui
```

For persistent beam-down mode shared across restarts and with the QueueServer worker,
run these from this profile directory:

```sh
pixi run beam-down
bsui
```

`pixi run start-beamdown` sets that same persistent flag and launches the profile in IPython.
When beam returns, run `turn_on_suspenders()` in the current session and
`clear_beam_down()` (or `pixi run beam-up` in a shell) to clear the persistent flag for
future starts. The environment-variable setting above lasts only for the launched session.

## Commissioning Notes

- [Beam position snapshots](docs/BEAM_POSITION_SNAPSHOTS.md)
- [Sorensen power supply](docs/SORENSEN_POWER_SUPPLY.md)
- [Pilot Bluesky console magics](docs/MOTOR_MAGICS.md)

## Plan writing

- [Energy scans with a single harmonic](docs/ENERGY_SCAN_HARMONICS.md)
