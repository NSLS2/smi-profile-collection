"""smi_beamline -- the NSLS-II SMI beamline Bluesky package.

Phase 4 of the profile-collection restructure (see
smi-plans/docs/STARTUP_RESTRUCTURE_PLAN.md).  Holds the ophyd device classes
(``smi_beamline.devices``), and -- as the restructure proceeds -- the device
factory, plans, and config.  The thin IPython/QS bootstrap lives in
``startup/startup.py`` and imports from here.
"""
