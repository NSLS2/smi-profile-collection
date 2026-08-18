from ophyd import EpicsSignal, Device, Component as Cpt, DeviceStatus
from ophyd import EpicsSignal, EpicsSignalRO
from ophyd import Component as Cpt
import bluesky.plan_stubs as bps

class output_lakeshore(Device):

    status = Cpt(EpicsSignal, "Val:Range-Sel")
    P = Cpt(EpicsSignal, "Gain:P-SP")
    I = Cpt(EpicsSignal, "Gain:I-SP")
    D = Cpt(EpicsSignal, "Gain:D-SP")
    temp_set_point = Cpt(EpicsSignal, "T-SP")

    def turn_on(self):
        yield from bps.mv(self.status, 1)

    def turn_off(self):
        yield from bps.mv(self.status, 0)

    def mv_temp(self, temp):
        yield from bps.mv(self.temp_set_point, temp)


class new_LakeShore(Device):
    """
    Lakeshore is the device reading the temperature from the heating stage for SAXS and GISAXS.
    This class define the PVs to read and write to control lakeshore
    :param Device: ophyd device
    """

    input_A = Cpt(EpicsSignal, "{Env:01-Chan:A}T-I")
    input_A_celsius = Cpt(EpicsSignal, "{Env:01-Chan:A}T:C-I")

    input_B = Cpt(EpicsSignal, "{Env:01-Chan:B}T-I")
    input_C = Cpt(EpicsSignal, "{Env:01-Chan:C}T-I")
    input_D = Cpt(EpicsSignal, "{Env:01-Chan:D}T-I")

    # The four control-loop outputs as PROPER Components (relative suffix composes with the parent
    # prefix, e.g. "XF:12ID-ES" + "{Env:01-Out:1}").  Previously these were eagerly-instantiated
    # plain output_lakeshore() instances with hard-coded ABSOLUTE prefixes: that made them invisible
    # to ophyd (absent from component_names / read() / describe()) and -- worse -- meant
    # make_fake_device(new_LakeShore) left them holding REAL EpicsSignals.  As Cpt they join the
    # device tree and fake correctly.
    output1 = Cpt(output_lakeshore, "{Env:01-Out:1}")
    output2 = Cpt(output_lakeshore, "{Env:01-Out:2}")
    output3 = Cpt(output_lakeshore, "{Env:01-Out:3}")
    output4 = Cpt(output_lakeshore, "{Env:01-Out:4}")

class XBPM(Device):
    """
    XBPM are diamond windows that generate current when the beam come through. It is used to know the position
    of the beam at the bpm postion as well as the amount of incoming photons. 3 bpms are available at SMI: bpm1
    is position upstream, bpm2 after the focusing mirrons and bpm3 downstream
    :param Device: ophyd device
    """

    ch1 = Cpt(EpicsSignal, "Current1:MeanValue_RBV")
    ch2 = Cpt(EpicsSignal, "Current2:MeanValue_RBV")
    ch3 = Cpt(EpicsSignal, "Current3:MeanValue_RBV")
    ch4 = Cpt(EpicsSignal, "Current4:MeanValue_RBV")
    sumX = Cpt(EpicsSignal, "SumX:MeanValue_RBV")
    sumY = Cpt(EpicsSignal, "SumY:MeanValue_RBV")
    posX = Cpt(EpicsSignal, "PosX:MeanValue_RBV")
    posY = Cpt(EpicsSignal, "PosY:MeanValue_RBV")


# this doesn't work, because the PV names do not end in .VAL ??
# full PV names are given in the above.


class PinDiodeTetrAMM(Device):
    """Experimental pin-diode electrometer view for the TetrAMM readout.

    This intentionally does not replace the existing ``QuadEMV33`` instance.  The
    default read set is limited to PVs already used in this profile; additional
    acquisition/averaging controls are exposed for manual testing from the CSS
    screen PV list without making routine reads depend on them.
    """

    adc_offset1 = Cpt(EpicsSignal, "ADCOffset1", kind="omitted")
    adc_offset2 = Cpt(EpicsSignal, "ADCOffset2", kind="omitted")
    adc_offset3 = Cpt(EpicsSignal, "ADCOffset3", kind="omitted")
    adc_offset4 = Cpt(EpicsSignal, "ADCOffset4", kind="omitted")

    acquire = Cpt(EpicsSignal, "Acquire")
    acquire_mode = Cpt(EpicsSignal, "AcquireMode")
    acquire_mode_readback = Cpt(EpicsSignal, "AcquireMode_RBV")
    averaging_time = Cpt(EpicsSignal, "AveragingTime")
    averaging_time_readback = Cpt(EpicsSignal, "AveragingTime_RBV")
    bias_interlock = Cpt(EpicsSignal, "BiasInterlock")
    bias_interlock_readback = Cpt(EpicsSignal, "BiasInterlock_RBV")
    bias_state = Cpt(EpicsSignal, "BiasState")
    bias_state_readback = Cpt(EpicsSignal, "BiasState_RBV")
    bias_voltage = Cpt(EpicsSignal, "BiasVoltage")
    bias_voltage_readback = Cpt(EpicsSignal, "BiasVoltage_RBV")
    calibration_mode = Cpt(EpicsSignal, "CalibrationMode", kind="omitted")
    calibration_mode_readback = Cpt(EpicsSignal, "CalibrationMode_RBV", kind="omitted")

    compute_current_offset1 = Cpt(EpicsSignal, "ComputeCurrentOffset1.PROC", kind="omitted")
    compute_current_offset2 = Cpt(EpicsSignal, "ComputeCurrentOffset2.PROC", kind="omitted")
    compute_current_offset3 = Cpt(EpicsSignal, "ComputeCurrentOffset3.PROC", kind="omitted")
    compute_current_offset4 = Cpt(EpicsSignal, "ComputeCurrentOffset4.PROC", kind="omitted")
    compute_pos_offset_x = Cpt(EpicsSignal, "ComputePosOffsetX.PROC", kind="omitted")
    compute_pos_offset_y = Cpt(EpicsSignal, "ComputePosOffsetY.PROC", kind="omitted")
    copy_adc_offsets = Cpt(EpicsSignal, "CopyADCOffsets.PROC", kind="omitted")

    current1_mean = Cpt(EpicsSignal, "Current1:MeanValue_RBV")
    current1_sigma = Cpt(EpicsSignal, "Current1:Sigma_RBV")
    current1_average = Cpt(EpicsSignal, "Current1Ave")
    current2_mean = Cpt(EpicsSignal, "Current2:MeanValue_RBV")
    current2_sigma = Cpt(EpicsSignal, "Current2:Sigma_RBV")
    current2_average = Cpt(EpicsSignal, "Current2Ave")
    current3_mean = Cpt(EpicsSignal, "Current3:MeanValue_RBV")
    current3_sigma = Cpt(EpicsSignal, "Current3:Sigma_RBV")
    current3_average = Cpt(EpicsSignal, "Current3Ave")
    current4_mean = Cpt(EpicsSignal, "Current4:MeanValue_RBV")
    current4_sigma = Cpt(EpicsSignal, "Current4:Sigma_RBV")
    current4_average = Cpt(EpicsSignal, "Current4Ave")

    current_name1 = Cpt(EpicsSignal, "CurrentName1")
    current_name2 = Cpt(EpicsSignal, "CurrentName2")
    current_name3 = Cpt(EpicsSignal, "CurrentName3")
    current_name4 = Cpt(EpicsSignal, "CurrentName4")
    current_offset1 = Cpt(EpicsSignal, "CurrentOffset1", kind="omitted")
    current_offset2 = Cpt(EpicsSignal, "CurrentOffset2", kind="omitted")
    current_offset3 = Cpt(EpicsSignal, "CurrentOffset3", kind="omitted")
    current_offset4 = Cpt(EpicsSignal, "CurrentOffset4", kind="omitted")
    current_precision1 = Cpt(EpicsSignal, "CurrentPrec1")
    current_precision2 = Cpt(EpicsSignal, "CurrentPrec2")
    current_precision3 = Cpt(EpicsSignal, "CurrentPrec3")
    current_precision4 = Cpt(EpicsSignal, "CurrentPrec4")
    current_scale1 = Cpt(EpicsSignal, "CurrentScale1", kind="omitted")
    current_scale2 = Cpt(EpicsSignal, "CurrentScale2", kind="omitted")
    current_scale3 = Cpt(EpicsSignal, "CurrentScale3", kind="omitted")
    current_scale4 = Cpt(EpicsSignal, "CurrentScale4", kind="omitted")

    dac0 = Cpt(EpicsSignal, "DAC0", kind="omitted")
    dac1 = Cpt(EpicsSignal, "DAC1", kind="omitted")
    dac2 = Cpt(EpicsSignal, "DAC2", kind="omitted")
    dac3 = Cpt(EpicsSignal, "DAC3", kind="omitted")

    diff_x_mean = Cpt(EpicsSignal, "DiffX:MeanValue_RBV")
    diff_x_sigma = Cpt(EpicsSignal, "DiffX:Sigma_RBV")
    diff_x_average = Cpt(EpicsSignal, "DiffXAve")
    diff_y_mean = Cpt(EpicsSignal, "DiffY:MeanValue_RBV")
    diff_y_sigma = Cpt(EpicsSignal, "DiffY:Sigma_RBV")
    diff_y_average = Cpt(EpicsSignal, "DiffYAve")

    fast_average_scan = Cpt(EpicsSignal, "FastAverageScan.SCAN")
    fast_averaging_time = Cpt(EpicsSignal, "FastAveragingTime")
    fast_averaging_time_readback = Cpt(EpicsSignal, "FastAveragingTime_RBV")
    firmware = Cpt(EpicsSignal, "Firmware")
    geometry = Cpt(EpicsSignal, "Geometry")
    geometry_readback = Cpt(EpicsSignal, "Geometry_RBV")
    hvi_readback = Cpt(EpicsSignal, "HVIReadback")
    hvs_readback = Cpt(EpicsSignal, "HVSReadback")
    hvv_readback = Cpt(EpicsSignal, "HVVReadback")
    integration_time = Cpt(EpicsSignal, "IntegrationTime")
    integration_time_readback = Cpt(EpicsSignal, "IntegrationTime_RBV")
    model = Cpt(EpicsSignal, "Model")
    nd_attributes_file = Cpt(EpicsSignal, "NDAttributesFile", kind="omitted")
    nd_attributes_macros = Cpt(EpicsSignal, "NDAttributesMacros", kind="omitted")
    nd_attributes_status = Cpt(EpicsSignal, "NDAttributesStatus", kind="omitted")
    num_acquire = Cpt(EpicsSignal, "NumAcquire")
    num_acquire_readback = Cpt(EpicsSignal, "NumAcquire_RBV")
    num_acquired = Cpt(EpicsSignal, "NumAcquired")
    num_average_readback = Cpt(EpicsSignal, "NumAverage_RBV")
    num_averaged_readback = Cpt(EpicsSignal, "NumAveraged_RBV")
    num_channels = Cpt(EpicsSignal, "NumChannels")
    num_channels_readback = Cpt(EpicsSignal, "NumChannels_RBV")
    num_fast_average = Cpt(EpicsSignal, "NumFastAverage")
    ping_pong = Cpt(EpicsSignal, "PingPong")
    ping_pong_readback = Cpt(EpicsSignal, "PingPong_RBV")

    pos_x_mean = Cpt(EpicsSignal, "PosX:MeanValue_RBV")
    pos_x_sigma = Cpt(EpicsSignal, "PosX:Sigma_RBV")
    pos_y_mean = Cpt(EpicsSignal, "PosY:MeanValue_RBV")
    pos_y_sigma = Cpt(EpicsSignal, "PosY:Sigma_RBV")
    position_offset_x = Cpt(EpicsSignal, "PositionOffsetX", kind="omitted")
    position_offset_y = Cpt(EpicsSignal, "PositionOffsetY", kind="omitted")
    position_precision_x = Cpt(EpicsSignal, "PositionPrecX")
    position_precision_y = Cpt(EpicsSignal, "PositionPrecY")
    position_scale_x = Cpt(EpicsSignal, "PositionScaleX", kind="omitted")
    position_scale_y = Cpt(EpicsSignal, "PositionScaleY", kind="omitted")
    position_x_average = Cpt(EpicsSignal, "PositionXAve")
    position_y_average = Cpt(EpicsSignal, "PositionYAve")

    range = Cpt(EpicsSignal, "Range")
    range_readback = Cpt(EpicsSignal, "Range_RBV")
    read_data = Cpt(EpicsSignal, "ReadData.PROC", kind="omitted")
    read_format = Cpt(EpicsSignal, "ReadFormat")
    read_format_readback = Cpt(EpicsSignal, "ReadFormat_RBV")
    read_status_scan = Cpt(EpicsSignal, "ReadStatus.SCAN")
    reset = Cpt(EpicsSignal, "Reset.PROC", kind="omitted")
    resolution = Cpt(EpicsSignal, "Resolution")
    resolution_readback = Cpt(EpicsSignal, "Resolution_RBV")
    ring_overflows = Cpt(EpicsSignal, "RingOverflows")
    sample_time_readback = Cpt(EpicsSignal, "SampleTime_RBV")

    sum_all_mean = Cpt(EpicsSignal, "SumAll:MeanValue_RBV")
    sum_all_sigma = Cpt(EpicsSignal, "SumAll:Sigma_RBV")
    sum_all_average = Cpt(EpicsSignal, "SumAllAve")
    sum_x_mean = Cpt(EpicsSignal, "SumX:MeanValue_RBV")
    sum_x_sigma = Cpt(EpicsSignal, "SumX:Sigma_RBV")
    sum_x_average = Cpt(EpicsSignal, "SumXAve")
    sum_y_mean = Cpt(EpicsSignal, "SumY:MeanValue_RBV")
    sum_y_sigma = Cpt(EpicsSignal, "SumY:Sigma_RBV")
    sum_y_average = Cpt(EpicsSignal, "SumYAve")

    ts_acquire = Cpt(EpicsSignal, "TS:TSAcquire")
    ts_acquiring = Cpt(EpicsSignal, "TS:TSAcquiring")
    temperature = Cpt(EpicsSignal, "Temperature")
    trigger_mode = Cpt(EpicsSignal, "TriggerMode")
    trigger_mode_readback = Cpt(EpicsSignal, "TriggerMode_RBV")
    trigger_polarity = Cpt(EpicsSignal, "TriggerPolarity")
    trigger_polarity_readback = Cpt(EpicsSignal, "TriggerPolarity_RBV")
    values_per_read = Cpt(EpicsSignal, "ValuesPerRead")
    values_per_read_readback = Cpt(EpicsSignal, "ValuesPerRead_RBV")

    _default_read_attrs = (
        "current2_mean",
        "current2_sigma",
        "current2_average",
        "sum_all_mean",
        "sum_all_sigma",
        "sum_all_average",
    )
    _default_configuration_attrs = (
        "acquire_mode_readback",
        "averaging_time_readback",
        "bias_state_readback",
        "bias_voltage_readback",
        "fast_averaging_time_readback",
        "integration_time_readback",
        "num_acquire_readback",
        "num_average_readback",
        "num_channels_readback",
        "range_readback",
        "resolution_readback",
        "sample_time_readback",
        "trigger_mode_readback",
        "values_per_read_readback",
    )


class Keithly2450(Device):
    run = Cpt(EpicsSignal, "run")
    busy = Cpt(EpicsSignalRO, "busy")
    reading = Cpt(EpicsSignalRO, "reading")

    send_done = Cpt(EpicsSignal, "send_done")

    send_pgm = Cpt(EpicsSignal, "send_pgm.AOUT")
    send_prt = Cpt(EpicsSignal, "send_prt.AOUT")
    send_stb = Cpt(EpicsSignal, "send_stb.SCAN", string=True)
    # calc_done = Cpt(EpicsSignalRO, 'calc_done')
    # fast_thold = Cpt(EpicsSignalRO, 'fast_thold')
    # parse_cmd = Cpt(EpicsSignalRO, 'parse_cmd')
    # fast_done = Cpt(EpicsSignalRO, 'fast_done')

    _default_read_attrs = ("reading",)
    _default_configuration_attrs = ("send_pgm", "send_prt", "send_stb")

    def trigger(self):
        st = DeviceStatus(self)

        def keithy_done_monitor(old_value, value, **kwargs):
            if old_value == 1 and value == 0:
                st._finished()
                self.busy.clear_sub(keithy_done_monitor)

        self.busy.subscribe(keithy_done_monitor, run=False)
        self.run.put(1)
        return st
