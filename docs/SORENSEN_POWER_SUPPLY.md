# Sorensen Power Supply

The Sorensen power supply is available in the collection namespace as `sorensen_ps1`.

Device class: `smi_beamline.devices.power_supply.PowerSupply`

Live prefix: `XF:12ID2-ES{PS:1}`

## Readback

Reading the device records the output current and output voltage readback:

```python
sorensen_ps1.read()
```

Recorded fields:

- `sorensen_ps1_current`, in `A`, from `XF:12ID2-ES{PS:1}I-I`
- `sorensen_ps1_out_main_readback`, in `V`, from `XF:12ID2-ES{PS:1}E:OutMain-RB`

The current readback suffix was corrected from `I` to `I-I` to match the real
beamline PV. `XF:12ID2-ES{PS:1}I-I` has been verified during hardware operation.

## Set Voltage

Set the output voltage in volts:

```python
sorensen_ps1.output(12.0)
```

To set the current limit at the same time, pass `current_max` in amps:

```python
sorensen_ps1.output(12.0, current_max=1.5)
```

If `current_max` is omitted, the current limit PV is not written.

The helper returns an ophyd status from the voltage setpoint write, so it can be waited on:

```python
sorensen_ps1.output(12.0).wait(timeout=5)
```

## Output Enable

Turn the main output on:

```python
sorensen_ps1.on()
```

Turn the main output off:

```python
sorensen_ps1.off()
```

These helpers write `1` and `0`, respectively, to `XF:12ID2-ES{PS:1}Enbl:OutMain-Cmd`.

## PV Map

- `current`: `XF:12ID2-ES{PS:1}I-I`
- `max_current`: `XF:12ID2-ES{PS:1}I-Lim`
- `out_main_readback`: `XF:12ID2-ES{PS:1}E:OutMain-RB`
- `out_main_setpoint`: `XF:12ID2-ES{PS:1}E:OutMain-SP`
- `lock_command`: `XF:12ID2-ES{PS:1}Enbl:Lock-Cmd`
- `lock_status`: `XF:12ID2-ES{PS:1}Enbl:Lock-Sts`
- `out_main_command`: `XF:12ID2-ES{PS:1}Enbl:OutMain-Cmd`
- `out_main_status`: `XF:12ID2-ES{PS:1}Enbl:OutMain-Sts`
- `operating_status_bc`: `XF:12ID2-ES{PS:1}Sts:Opr-Sts.BC`
- `operating_status_bd`: `XF:12ID2-ES{PS:1}Sts:Opr-Sts.BD`
