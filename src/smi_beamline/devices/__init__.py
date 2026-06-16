"""smi_beamline.devices -- ophyd DEVICE CLASSES (pure, importable, hardware-free at import).

These were formerly ``startup/smiclasses/``.  They contain only class definitions (no
``get_ipython()``, no import-time instance construction); the live instances are built by the
factory and the values they need (RE.md / mdsave / energy) are reached through the
``smi_beamline.devices._context`` seam.
"""
