from ophyd import (
    ProsilicaDetector,
    ImagePlugin,
    EpicsSignal,
    ROIPlugin,
    TIFFPlugin,
    TransformPlugin,
    ProcessPlugin,
    OverlayPlugin,
    ProsilicaDetectorCam,
    ColorConvPlugin,
    
)
from .pilatus import TIFFPluginWithFileStore
from ophyd import Component as Cpt
from nslsii.ad33 import SingleTriggerV33, StatsPluginV33
from smibase.base import RE

class ProsilicaDetectorCamV33(ProsilicaDetectorCam):
    """This is used to update the Standard Prosilica to AD33. It adds the
process
    """
    wait_for_plugins = Cpt(EpicsSignal, 'WaitForPlugins',
                           string=True, kind='config')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs['wait_for_plugins'] = 'Yes'

    def ensure_nonblocking(self):
        self.stage_sigs['wait_for_plugins'] = 'Yes'
        for c in self.parent.component_names:
            cpt = getattr(self.parent, c)
            if cpt is self:
                continue
            if hasattr(cpt, 'ensure_nonblocking'):
                cpt.ensure_nonblocking()

class TIFFPluginEnsuredOff(TIFFPlugin):
    """Add this as a component to detectors that do not write TIFFs."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs.update([('auto_save', 'No')])


class StandardProsilicaV33(SingleTriggerV33, ProsilicaDetector):
    cam = Cpt(ProsilicaDetectorCamV33, 'cam1:')
    image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPluginV33, 'Stats1:')
    stats2 = Cpt(StatsPluginV33, 'Stats2:')
    stats3 = Cpt(StatsPluginV33, 'Stats3:')
    stats4 = Cpt(StatsPluginV33, 'Stats4:')
    stats5 = Cpt(StatsPluginV33, 'Stats5:')
    trans1 = Cpt(TransformPlugin, 'Trans1:')
    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')
    proc1 = Cpt(ProcessPlugin, 'Proc1:')
    over1 = Cpt(OverlayPlugin, 'Over1:')
    cc1 = Cpt(ColorConvPlugin, 'CC1:')
    
    # This class does not save TIFFs. We make it aware of the TIFF plugin
    # only so that it can ensure that the plugin is not auto-saving.
    tiff = Cpt(TIFFPluginEnsuredOff, suffix='TIFF1:')

    @property
    def hints(self):
        return {'fields': [self.stats1.total.name]}

    def set_primary_roi(self, num):
        st = f"stats{num}"
        self.hints = {"fields": [getattr(self, st).total.name]}
        self.read_attrs = [st]


class StandardProsilicaWithTIFFV33(StandardProsilicaV33):
    tiff = Cpt(TIFFPluginWithFileStore,
               suffix='TIFF1:',
               md = RE.md,
               write_path_template='',
               root='/nsls2/data/smi/proposals')

    def __init__(self, *args, asset_path, **kwargs):
        self.asset_path = asset_path
        super().__init__(*args, **kwargs)
        self.tiff._asset_path = self.asset_path


