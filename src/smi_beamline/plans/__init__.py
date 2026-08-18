"""smi_beamline.plans -- beamline-infrastructure plans / logic (functions, not device instances).

These modules (formerly ``startup/smibase/{alignment,beam-mode,config,humidity_cell,utils}``)
define PLANS and helper functions; they build no device instances themselves.  They import the
live device instances they operate on from ``smibase`` (which still builds them), and are loaded
by the device factory after the instances exist.

(This is the Phase-4 "move just the plan modules" relocation; the instance-builder modules remain
in ``startup/smibase/`` for now.)
"""
