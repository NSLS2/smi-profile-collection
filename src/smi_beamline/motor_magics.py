"""Standalone, interactive moves, scans, readouts, and snapshots.

Load with ``%load_ext smi_beamline.motor_magics``. No devices are imported or
constructed here. These commands are console actions, never Bluesky plans.
"""

import math
import os
import re
import sys
from functools import partial

from bluesky import plan_stubs as bps
from bluesky import plans as bp
from IPython.core.error import UsageError
from IPython.core.magic import no_var_expand
from smi_beamline.devices.status import compare_energy


# Use the public axis aliases (stage.th/ph/ch are pseudo-positioner axes).
MOTOR_MAGICS = {
    **{axis: ("piezo", axis, "um" if axis in ("x", "y", "z") else "deg")
       for axis in ("x", "y", "z", "th", "ph", "ch")},
    **{"s" + axis: ("stage", axis, "mm" if axis in ("x", "y", "z") else "deg")
       for axis in ("x", "y", "z", "th", "ph", "ch")},
}

SCAN_MAGICS = {
    command + suffix: (command, relative)
    for command in MOTOR_MAGICS
    for suffix, relative in (("scan", False), ("rscan", True))
}
# Also accept xsscan/ysscan/... and xsrscan/ysrscan/... for the stage.
SCAN_MAGICS.update({
    axis + "s" + suffix: ("s" + axis, relative)
    for axis in ("x", "y", "z", "th", "ph", "ch")
    for suffix, relative in (("scan", False), ("rscan", True))
})
SNAPSHOTS = {
    "snaps": ("pil2M",),
    "snapw": ("pil900KW",),
    "snapsw": ("pil2M", "pil900KW"),
}
SHUTTERS = {"so": "shopen", "sopen": "shopen", "sc": "shclose", "sclose": "shclose"}
COMMANDS = (*MOTOR_MAGICS, *SCAN_MAGICS, "wh", "status", "exp", "e", *SNAPSHOTS, *SHUTTERS, "stop", "help")
ARGUMENT_COLORS = ("94", "92", "95")  # blue, green, magenta
ENERGY_MATCH_TOLERANCE_EV = 100.0
_SYNTAX_TOKEN = re.compile(
    r"(?<![\w.])(?:%?[A-Za-z_]+|[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)(?![\w.])"
)


def _help(command):
    if command == "status":
        return (
            "%status: read-only upstream-to-downstream beamline overview (~36 lines).\n"
            "Shutters, DCM, mirrors, attenuators, CRLs, slits, vacuum, sample, detectors.\n"
            "No RE call or device writes. Missing/offline readings remain visible; "
            "150 ms read timeout, 3 s read budget. Detector energy mismatch >100 eV."
        )
    if command == "e":
        return (
            "%e: read beamline and detector energies in eV; highlight differences > 100 eV.\n"
            "%e VALUE: RE(bps.mv(energy, VALUE)), then set_energy(VALUE) after success.\n"
            "Absolute energy in eV; VALUE > 0. The existing set_energy helper also "
            "moves energy to that target before updating detector settings."
        )
    if command in SHUTTERS:
        return f"%{command}: RE({SHUTTERS[command]}()); uses the existing shutter/feedback plan."
    if command == "stop":
        return "%stop: RE.stop(); gracefully stop a paused run (not an emergency hardware stop)."
    if command == "help":
        return "%help: show the boxed Bluesky command guide; COMMAND ? gives detailed help."
    if command in MOTOR_MAGICS:
        device, axis, units = MOTOR_MAGICS[command]
        return (
            f"%{command}: read {device}.{axis} position ({units}).\n"
            f"%{command} VALUE: RE(bps.mvr({device}.{axis}, VALUE)), relative {units}.\n"
            f"%{command} a VALUE: RE(bps.mv({device}.{axis}, VALUE)), absolute {units}."
        )
    if command in SCAN_MAGICS:
        motor_command, relative = SCAN_MAGICS[command]
        device, axis, units = MOTOR_MAGICS[motor_command]
        if relative:
            return (
                f"%{command} SPAN POINTS: RE(bp.rel_scan([pil2M], "
                f"{device}.{axis}, -SPAN, SPAN, POINTS)).\n"
                f"Symmetric offsets in {units}; SPAN > 0; integer POINTS >= 2. "
                "Returns to the starting position on normal completion."
            )
        return (
            f"%{command} START STOP POINTS: RE(bp.scan([pil2M], "
            f"{device}.{axis}, START, STOP, POINTS)).\n"
            f"Absolute endpoints in {units}; integer POINTS >= 2. "
            "Leaves the motor at STOP on normal completion."
        )
    if command in SNAPSHOTS:
        detectors = ", ".join(SNAPSHOTS[command])
        return (
            f"%{command}: RE(bp.count([{detectors}], 1, "
            "md={'sample_name': 'snapshot'})). Uses current exposure settings."
        )
    if command == "wh":
        return "%wh: read piezo and stage positions in a 2-row × 6-axis table; no RE call."
    return (
        "%exp: read exposure time (s), period (s), and images per trigger for each detector.\n"
        "%exp N: RE(det_exposure_time(N, N)), one image of N seconds.\n"
        "%exp N M: RE(det_exposure_time(N, M)); M is total measurement time (s), "
        "NOT image count. Images = int(M / N); require N > 0 and M >= N.\n"
        "Settings are read back after a change."
    )


def _number(token, usage):
    try:
        value = float(token)
    except ValueError:
        raise UsageError("Use finite numeric literals.\n" + usage) from None
    if not math.isfinite(value):
        raise UsageError("Use finite numeric literals.\n" + usage)
    return value


def _namespace(shell, name):
    value = shell.user_ns.get(name)
    if value is None:
        raise UsageError(f"No {name} in the IPython user namespace.")
    return value


def _motor(shell, command):
    device_name, axis, _ = MOTOR_MAGICS[command]
    device = _namespace(shell, device_name)
    try:
        return getattr(device, axis)
    except AttributeError:
        raise UsageError(
            f"%{command} unavailable: {device_name}.{axis} is not defined."
        ) from None


def _idle_re(shell, command):
    re = _namespace(shell, "RE")
    if re.state != "idle":
        raise UsageError(f"RE must be idle for %{command}; current state: {re.state}.")
    return re


def _color(shell, text, code):
    if str(shell.colors).lower() == "nocolor" or "NO_COLOR" in os.environ:
        return text
    return f"\033[{code}m{text}\033[0m"


def _syntax(shell, text):
    """Color commands and positional arguments without changing visible text."""
    argument = 0
    parts, end = [], 0
    for match in _SYNTAX_TOKEN.finditer(text):
        parts.append(text[end:match.start()])
        token = match.group()
        if token.lstrip("%") in COMMANDS:
            argument = 0
            token = _color(shell, token, "1;36")
        elif token in ("VALUE", "START", "STOP", "SPAN", "POINTS", "N", "M") or re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", token
        ):
            token = _color(shell, token, ARGUMENT_COLORS[argument % len(ARGUMENT_COLORS)])
            argument += 1
        elif token == "a":
            token = _color(shell, token, "93")
        parts.append(token)
        end = match.end()
    parts.append(text[end:])
    return "".join(parts)


def _echo(shell, command, tokens, description):
    print(f"{_syntax(shell, ' '.join([command, *tokens]))} → {description}")


def _description(shell, text, arguments):
    """Map each description number to its example argument, not display order.

    None marks a fixed/derived number rather than an input argument.
    """
    roles = iter(arguments)
    parts, end = [], 0
    for match in _SYNTAX_TOKEN.finditer(text):
        token = match.group()
        try:
            float(token)
        except ValueError:
            continue
        parts.append(text[end:match.start()])
        role = next(roles, None)
        parts.append(token if role is None else _color(shell, token, ARGUMENT_COLORS[role]))
        end = match.end()
    parts.append(text[end:])
    return "".join(parts)


def _table(shell, headers, rows, *, command_column=False, cell_colors=None, description_arguments=None):
    """Small dependency-free terminal table; pad before adding ANSI colors."""
    widths = [max(len(str(row[i])) for row in [headers, *rows]) for i in range(len(headers))]
    for row_index, row in enumerate([headers, *rows]):
        if row_index == 0:
            print("┌" + "┬".join("─" * (width + 2) for width in widths) + "┐")
        cells = [str(value).ljust(width) for value, width in zip(row, widths)]
        rendered = []
        for column, cell in enumerate(cells):
            if row_index == 0:
                rendered.append(_color(shell, cell, "1;36"))
            elif cell_colors and (row_index - 1, column) in cell_colors:
                rendered.append(_color(shell, cell, cell_colors[row_index - 1, column]))
            elif command_column:
                rendered.append(
                    _syntax(shell, cell) if column == 0 else
                    _description(shell, cell, (description_arguments or {}).get(row_index - 1, ()))
                )
            else:
                code = "36" if column == 0 else ARGUMENT_COLORS[(column - 1) % len(ARGUMENT_COLORS)]
                rendered.append(_color(shell, cell, code))
        print("│ " + " │ ".join(rendered) + " │")
        if row_index == 0:
            print("├" + "┼".join("─" * (width + 2) for width in widths) + "┤")
    print("└" + "┴".join("─" * (width + 2) for width in widths) + "┘")


def _position(shell, command):
    motor = _motor(shell, command)
    if not getattr(motor, "connected", True):
        raise UsageError("disconnected")
    value = float(motor.position)
    if not math.isfinite(value):
        raise UsageError("non-finite readback")
    return f"{value:.4f} {MOTOR_MAGICS[command][2]}"


def _where(shell):
    axes = ("x", "y", "z", "th", "ph", "ch")
    rows, errors = [], []
    for device, prefix in (("piezo", ""), ("stage", "s")):
        row = [device]
        for axis in axes:
            try:
                row.append(_position(shell, prefix + axis))
            except Exception as exc:
                row.append("N/A")
                errors.append(f"{device}.{axis}: {exc}")
        rows.append(row)
    _table(shell, ["Device", *axes], rows)
    for error in errors:
        print(_color(shell, error, "33"))


def _exposures(shell):
    rows, errors = [], []
    for name in ("pil2M", "pil900KW"):
        try:
            cam = _namespace(shell, name).cam
            exposure = float(cam.acquire_time.get(timeout=2))
            period = float(cam.acquire_period.get(timeout=2))
            images = int(cam.num_images.get(timeout=2))
            rows.append([name, f"{exposure:g}", f"{period:g}", str(images)])
        except Exception as exc:
            rows.append([name, "N/A", "N/A", "N/A"])
            errors.append(f"{name}: {exc}")
    # The exposure plan optionally also configures Amptek (no burst image count).
    if shell.user_ns.get("amptek_det") is not None:
        try:
            exposure = _namespace(shell, "amptek").mca.preset_real_time.get(timeout=2)
            rows.append(["amptek", f"{float(exposure):g}", "—", "—"])
        except Exception as exc:
            rows.append(["amptek", "N/A", "—", "—"])
            errors.append(f"amptek: {exc}")
    _table(shell, ["Detector", "Exposure (s)", "Period (s)", "Images/trigger"], rows)
    for error in errors:
        print(_color(shell, error, "33"))


def _energies(shell):
    energy = _namespace(shell, "energy")
    position = energy.position
    # Energy is a PseudoPositioner: .position is a namedtuple.
    value = float(getattr(position, "energy", position))
    if not math.isfinite(value):
        raise UsageError("Non-finite energy readback.")
    rows = [["beamline", f"{value:.2f} eV", "—", "reference"]]
    colors, errors = {}, []
    for name in ("pil2M", "pil900KW"):
        row = len(rows)
        try:
            # Read the camera's Energy_RBV, not the remembered energyset value.
            camera_energy = float(_namespace(shell, name).cam.cam_energy.get(timeout=2)) * 1000
            if not math.isfinite(camera_energy):
                raise ValueError("non-finite detector energy readback")
            comparison = compare_energy(camera_energy, value, ENERGY_MATCH_TOLERANCE_EV)
            difference = comparison["difference_eV"]
            mismatch = not comparison["matches"]
            display_difference = 0.0 if round(difference, 2) == 0 else difference
            rows.append([
                name, f"{camera_energy:.2f} eV", f"{display_difference:+.2f} eV",
                "MISMATCH (>100 eV)" if mismatch else "OK (within 100 eV)",
            ])
            colors[row, 3] = "1;91" if mismatch else "92"
            if mismatch:
                colors[row, 1] = colors[row, 2] = "1;91"
        except Exception as exc:
            rows.append([name, "N/A", "—", "UNKNOWN"])
            colors[row, 3] = "93"
            errors.append(f"{name}: {exc}")
    _table(shell, ["Source", "Energy", "Detector − beamline", "Status"], rows, cell_colors=colors)
    for error in errors:
        print(_color(shell, error, "33"))


def _guide(shell):
    _table(shell, ["Command / example", "What it does"], [
        ["x y z th ph ch", "Piezo axes: translations um; rotations deg"],
        ["sx sy sz sth sph sch", "Stage axes: translations mm; rotations deg"],
        ["x", "Read position (works for every axis)"],
        ["x 1000 / x a 1000", "Jog +1000 um / move to 1000 um"],
        ["wh", "All positions: piezo + stage, 2 × 6 axes"],
        ["xscan -1000 1000 21", "pil2M: -1000 to 1000 um, 21 points; ends at 1000"],
        ["xrscan 1000 21", "pil2M: ±1000 um, 21 points; returns to start"],
        ["sxscan / sxrscan", "Stage scans; xsscan / xsrscan also work"],
        ["yscan, thscan, etc.", "scan / rscan variants for every axis"],
        ["exp", "Read detector exposure, period, images/trigger"],
        ["exp 0.5 / exp 0.5 2", "0.5 s × 1 image / int(2 / 0.5) images"],
        ["e / e 16150", "Compare energies / move to 16150 eV + set_energy(16150)"],
        ["snaps / snapw / snapsw", "One trigger: SAXS / WAXS / both; snapshot name"],
        ["so / sopen", "RE(shopen()): open shutter + enable feedback"],
        ["sc / sclose", "RE(shclose()): disable feedback + close shutter"],
        ["stop", "RE.stop(): gracefully stop a paused run"],
        ["help / COMMAND ?", "This guide / detailed command help"],
        ["status", "Upstream → downstream device overview (~36 lines)"],
    ], command_column=True, description_arguments={
        3: (0, 0),
        5: (0, 1, 2, 1),
        6: (0, 1),
        10: (0, None, 1, 0),  # exp: 0.5 s; fixed 1 image; int(M / N)
        11: (0, 0),
    })
    print(_syntax(shell, "Colors: xscan START STOP POINTS (command; first, second, third numeric argument)."))
    print("Standalone console commands. Prefix with % if a Python name shadows a magic.")
    print("Scans: POINTS >= 2; relative SPAN > 0. exp N M: M is total seconds, not images.")
    print("piezo.ph is currently unavailable. stop is not an emergency hardware stop.")


def _bare_help(shell, lines):
    """Route only bare help to the guide, leaving Python help(object) intact."""
    if "help" in shell.user_ns or "help" in shell.user_global_ns:
        return lines
    return [
        "%" + line if line.rstrip() in ("help", "help ?", "help --help", "help -h") else line
        for line in lines
    ]


def _command(shell, command, line):
    usage = _help(command)
    tokens = line.split()
    # A help token anywhere (including the second argument) never executes.
    if any(token in ("?", "-h", "--help") for token in tokens):
        _guide(shell) if command == "help" else print(_syntax(shell, usage))
        return
    # IPython calls this partial directly from run_line_magic; its caller must
    # be the top-level user cell. Reject functions, generators/plans, scripts,
    # and callbacks even when the RE happens to be idle. This is a misuse guard,
    # not a security boundary against deliberately manufactured Python frames.
    caller = sys._getframe(2)
    try:
        top_level = (
            caller.f_code.co_name == "<module>"
            and caller.f_globals is shell.user_global_ns
            and caller.f_locals is shell.user_ns
        )
    finally:
        del caller
    if not top_level:
        raise UsageError(
            f"%{command} is a standalone IPython command; do not call it from "
            "a function or plan. Inside plans use yield from with Bluesky plans."
        )

    if command in MOTOR_MAGICS:
        device_name, axis, units = MOTOR_MAGICS[command]
        if not tokens:
            _table(shell, ["Motor", "Position"], [[f"{device_name}.{axis}", _position(shell, command)]])
            return
        absolute = len(tokens) == 2 and tokens[0] == "a"
        if not (len(tokens) == 1 or absolute):
            raise UsageError(usage)
        value = _number(tokens[-1], usage)
        re = _idle_re(shell, command)
        motor = _motor(shell, command)
        mode = "absolute" if absolute else "relative"
        _echo(shell, command, tokens, f"{device_name}.{axis}: {mode} {value:g} {units}")
        return re(bps.mv(motor, value) if absolute else bps.mvr(motor, value))

    if command in SCAN_MAGICS:
        motor_command, relative = SCAN_MAGICS[command]
        if not tokens:
            print(_syntax(shell, usage))
            return
        if len(tokens) != (2 if relative else 3):
            raise UsageError(usage)
        try:
            points = int(tokens[-1])
        except ValueError:
            raise UsageError(usage) from None
        if points < 2:
            raise UsageError(usage)
        if relative:
            span = _number(tokens[0], usage)
            if span <= 0:
                raise UsageError(usage)
            start, stop = -span, span
        else:
            start, stop = (_number(token, usage) for token in tokens[:2])
        re = _idle_re(shell, command)
        motor = _motor(shell, motor_command)
        detector = _namespace(shell, "pil2M")
        device, axis, units = MOTOR_MAGICS[motor_command]
        mode = "relative offsets" if relative else "absolute"
        _echo(shell, command, tokens, f"{device}.{axis}: {mode} {start:g} to {stop:g} {units}, {points} points; pil2M")
        plan = bp.rel_scan if relative else bp.scan
        return re(plan([detector], motor, start, stop, points))

    if command == "wh":
        if tokens:
            raise UsageError(usage)
        return _where(shell)

    if command == "status":
        if tokens:
            raise UsageError(usage)
        from smi_beamline.beamline_status import show_status

        return show_status(shell, _color)

    if command == "e":
        if not tokens:
            return _energies(shell)
        if len(tokens) != 1:
            raise UsageError(usage)
        value = _number(tokens[0], usage)
        if value <= 0:
            raise UsageError(usage)
        engine = _idle_re(shell, command)
        energy = _namespace(shell, "energy")
        set_energy = _namespace(shell, "set_energy")
        if not callable(set_energy):
            raise UsageError("set_energy must be callable.")
        _echo(shell, command, tokens, f"energy: absolute {value:g} eV; then set_energy({value:g})")
        result = engine(bps.mv(energy, value))
        set_energy(value)
        _energies(shell)
        return result

    if command == "exp":
        if not tokens:
            return _exposures(shell)
        if len(tokens) not in (1, 2):
            raise UsageError(usage)
        exposure = _number(tokens[0], usage)
        total = _number(tokens[1], usage) if len(tokens) == 2 else exposure
        if exposure <= 0 or total < exposure or not math.isfinite(total / exposure):
            raise UsageError(usage)
        re = _idle_re(shell, command)
        exposure_plan = _namespace(shell, "det_exposure_time")
        _echo(shell, command, tokens, f"det_exposure_time({exposure:g}, {total:g}): {int(total / exposure)} images/trigger")
        result = re(exposure_plan(exposure, total))
        _exposures(shell)
        return result

    if tokens:
        raise UsageError(usage)
    if command == "help":
        return _guide(shell)
    if command == "stop":
        # Deliberately bypass the idle guard: stop is used on a paused RE.
        # Let RE enforce its own state rules and propagate errors unchanged.
        engine = _namespace(shell, "RE")
        _echo(shell, command, tokens, "RE.stop()")
        return engine.stop()
    if command in SHUTTERS:
        re = _idle_re(shell, command)
        plan = _namespace(shell, SHUTTERS[command])
        _echo(shell, command, tokens, f"RE({SHUTTERS[command]}())")
        return re(plan())
    re = _idle_re(shell, command)
    detectors = [_namespace(shell, name) for name in SNAPSHOTS[command]]
    _echo(shell, command, tokens, f"Snapshot: {', '.join(SNAPSHOTS[command])}; sample_name='snapshot'")
    return re(bp.count(detectors, 1, md={"sample_name": "snapshot"}))


def load_ipython_extension(ipython):
    """Register the pilot commands without binding/deleting user variables."""
    if ipython.user_ns.get("IS_QS_WORKER", False):
        raise UsageError("Motor magics are for interactive sessions, not QueueServer workers.")
    from smi_beamline.instances.layout import configure_layout

    configure_layout(ipython.user_ns)
    commands = COMMANDS
    for command in commands:
        magic = partial(_command, ipython, command)
        # IPython normally expands $variables and {expressions} before calling
        # magics. Disable this so the numeric-only parser really is literal-only.
        no_var_expand(magic)
        magic.__doc__ = _help(command) + "\nStandalone console use only; no functions or plans."
        ipython.register_magic_function(magic, magic_kind="line", magic_name=command)
    ipython.automagic = True
    # A builtin shadows automagic too. Use a narrowly scoped input transform
    # instead of replacing/deleting Python's builtin help. Replace on reload.
    ipython.input_transformers_cleanup[:] = [
        transform for transform in ipython.input_transformers_cleanup
        if not getattr(transform, "_smi_bare_help", False)
    ]
    transform = partial(_bare_help, ipython)
    transform._smi_bare_help = True
    ipython.input_transformers_cleanup.append(transform)
