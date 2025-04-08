from ophyd import Signal, Component, Device

# devices to store metadata about detectors
class SMI_WAXS_detector(Device):
    prefix = "detector_waxs_"
    pixel_size = Component(Signal, value=0.172, name=prefix + "pixel_size", kind="hinted")
    x0_pix = Component(Signal, value=97, name=prefix + "x0_pix", kind="hinted")
    y0_pix = Component(Signal, value=1386, name=prefix + "y0_pix", kind="hinted")
    sdd = Component(Signal, value=274.9, name=prefix + "sdd", kind="hinted")


class SMI_SAXS_detector(Device):
    prefix = "detector_saxs_"
    pixel_size = Component(Signal, value=0.172, name=prefix + "pixel_size", kind="hinted")
    bs_kind = Component(Signal, value="rod", name=prefix + "bs_kind", kind="hinted")
    xbs_mask = Component(Signal, value=0, name=prefix + "xbs_mask", kind="hinted")
    ybs_mask = Component(Signal, value=0, name=prefix + "ybs_mask", kind="hinted")
    x0_pix = Component(Signal, value=0, name=prefix + "y0_pix", kind="hinted")
    y0_pix = Component(Signal, value=0, name=prefix + "y0_pix", kind="hinted")
    sdd = Component(Signal, value=8300, name=prefix + "sdd", kind="hinted")

