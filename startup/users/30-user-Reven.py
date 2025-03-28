

def temp_series(name='temp',temps = np.linspace(32,26,13),exp_time=1, hold_delay=120, dets=[pil1M]):   # function loop to bring linkam to temp, hold and measure
# Function will begin at start_temp and take a SAXS measurement at every temperature given 
    
    #temps = np.linspace(45, 30, 16)

    #dets = [pil1M] 
    LThermal.setTemperature(temps[0])
    # LThermal.setTemperatureRate(ramp)
    LThermal.on() # turn on 
    det_exposure_time(exp_time,exp_time)

    s = Signal(name='target_file_name', value='')
    RE.md["sample_name"] = '{target_file_name}'
    for i, temp in enumerate(temps):
        print(f'setting temperature {temp}')
        LThermal.setTemperature(temp)

        while abs(LThermal.temperature()-temp)>0.2:
            yield from bps.sleep(10)
            print(f'{LThermal.temperature()} is too far from {temp} setpoint, waiting 10s')

        print('Reached setpoint', temp)
        if i==0:
            print(f'Beginning equilibration of {2*hold_delay} seconds')
            yield from bps.sleep(2*hold_delay)
        else:
            print(f'Beginning equilibration of {hold_delay} seconds')
            yield from bps.sleep(hold_delay)


        # Metadata
        sdd = pil1m_pos.z.position / 1000

        # Sample name
        name_fmt = ("{sample}_{energy}eV_sdd{sdd}m_temp{temp}")
        sample_name = name_fmt.format(sample = name,energy = "%.2f" % energy.energy.position , sdd = "%.1f" % sdd, temp = "%.1f" %temp)
        sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})

        print(f"\n\n\n\t=== Sample: {sample_name} ===")
        s.put(sample_name)
        
        yield from bp.count(dets + [s])

    LThermal.off()
    RE.md["sample_name"] = 'test'



def temp_series_withpos(name='temp',temps = np.linspace(32,26,13),exp_time=1, hold_delay=120, dets=[pil1M], xs=[-12.5], ys=[-2.298]):   # function loop to bring linkam to temp, hold and measure
# Function will begin at start_temp and take a SAXS measurement at every temperature given 
    
    #temps = np.linspace(45, 30, 16)

    #dets = [pil1M] 
    LThermal.setTemperature(temps[0])
    # LThermal.setTemperatureRate(ramp)
    LThermal.on() # turn on 
    det_exposure_time(exp_time,exp_time)

    s = Signal(name='target_file_name', value='')
    RE.md["sample_name"] = '{target_file_name}'
    for j in range(len(xs)):
        yield from mv(stage.x,xs[j])
        yield from mv(stage.y,ys[j])

        for i, temp in enumerate(temps):
            LThermal.setTemperature(temp)

            while abs(LThermal.temperature()-temp)>0.2:
                yield from bps.sleep(10)
                print('waiting for 10s')

            print('Reached temp', temp)
            print('Waiting during equilibration')
            if i==0:
                yield from bps.sleep(2*hold_delay)
            else:
                yield from bps.sleep(hold_delay)



            # Metadata
            sdd = pil1m_pos.z.position / 1000

            # Sample name
            name_fmt = ("{sample}_{energy}eV_sdd{sdd}m_temp{temp}_pos{pos`}")
            sample_name = name_fmt.format(sample = name,energy = "%.2f" % energy.energy.position , sdd = "%.1f" % sdd, temp = "%.1f" %temp, pos=j)
            sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})

            print(f"\n\n\n\t=== Sample: {sample_name} ===")
            s.put(sample_name)
            
            yield from bp.count(dets + [s])

    LThermal.off()
    RE.md["sample_name"] = 'test'





def temp_series_grid(name='temp',
                     temps = np.linspace(32,26,13),
                     exp_time=1, 
                     hold_delay=120, 
                     dets=[pil1M], 
                     xs=np.linspace(-13,-12,11), 
                     ys=np.linspace(-2.3,-2.8,6)):
       # function loop to bring linkam to temp, hold and measure
# Function will begin at start_temp and take a SAXS measurement at every temperature given 
    

    LThermal.setTemperature(temps[0])
    # LThermal.setTemperatureRate(ramp)
    LThermal.on() # turn on 
    det_exposure_time(exp_time,exp_time)

    s = Signal(name='target_file_name', value='')
    RE.md["sample_name"] = '{target_file_name}'
    print(f'starting grid scan of {len(xs)*len(ys)} points')
    for xp in xs:

        yield from mv(stage.x,xp)
        for yp in ys:
            yield from mv(stage.y,yp)
            print(f'beginning measurement at x={xp}, y={yp}')
            for i, temp in enumerate(temps):
                print(f'setting temperature {temp}')
                LThermal.setTemperature(temp)

                while abs(LThermal.temperature()-temp)>0.2:
                    yield from bps.sleep(10)
                    print(f'{LThermal.temperature()} is too far from {temp} setpoint, waiting 10s')

                print('Reached setpoint', temp)
                if i==0:
                    print(f'Beginning equilibration of {2*hold_delay} seconds')
                    yield from bps.sleep(2*hold_delay)
                else:
                    print(f'Beginning equilibration of {hold_delay} seconds')
                    yield from bps.sleep(hold_delay)



                # Metadata
                sdd = pil1m_pos.z.position / 1000

                # Sample name
                name_fmt = ("{sample}_{energy}eV_sdd{sdd}m_temp{temp}_x{x}_y{y}")
                sample_name = name_fmt.format(sample = name,
                                              energy = "%.2f" % energy.energy.position , 
                                              sdd = "%.1f" % sdd, 
                                              temp = "%.1f" % temp, 
                                              x= "%.1f" % xp, 
                                              y= "%.1f" % yp)
                sample_name = sample_name.translate({ord(c): "_" for c in "!@#$%^&*{}:/<>?\|`~+ =, "})

                print(f"\n\n\n\t=== Sample: {sample_name} ===")
                s.put(sample_name)
                
                yield from bp.count(dets + [s])

    LThermal.off()
    RE.md["sample_name"] = 'test'