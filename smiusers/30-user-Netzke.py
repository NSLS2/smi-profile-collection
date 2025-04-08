# phi scan
def gisaxsnetzke(meas_t=1):
    waxs_arc = np.linspace(0, 45.5, 8)  # for 9.54 keV
    # waxs_arc = np.linspace(0, 26, 5) #(2th_min 2th_max steps) for 16.1 keV
    dets = [pil300KW]
    phi = [0, -20, -40, -60]
    phi_aioff = [0, -0.03, -0.025, 0.015]
    xlocs = [  # -41000,
        -33500,
        -26000,
        -19000,
        -11500,
        1000,
        8500,
        16000,
        23500,
        31000,
        38500,
    ]
    # xlocs = [25500]
    names = [  #'SAM16-HZO_2',
        "ALLS61",
        "ALLS56",
        "ALLS63",
        "ALLS65",
        "SAM16-HZO_1",
        "SAM16HfO2_2",
        "ALLS58",
        "ALLS62",
        "ALLS57B",
        "ALLS64",
    ]
    angle = [0.2, 0.29, 0.4, 0.45]  # for 9.54 keV
    # angle = [0.08, 0.12, 0.2] #for 16.1 keV
    energ = [9540, 9580]
    # energ = [6100]
    assert len(xlocs) == len(names), f"Sample name/position list is borked"

    for x, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, x)
        yield from bps.mv(GV7.open_cmd, 1)
        yield from alignement_gisaxs(0.2)  # for 9.54 keV
        # yield from alignement_gisaxs(0.08) #for 16.1 keV
        yield from bps.mv(GV7.close_cmd, 1)
        yield from bps.mv(att2_5.open_cmd, 1)
        det_exposure_time(meas_t, meas_t)
        name_fmt = "{sample}_E{ene}eV_ai{angle}deg_phi{phi}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            for an in angle:
                # yield from bps.mv(stage.th, an)
                for ph, aioff in zip(phi, phi_aioff):
                    yield from bps.mv(prs, ph)
                    yield from bps.mv(stage.th, an + aioff)
                    for en in energ:
                        yield from bps.mv(energy, en)
                        sample_name = name_fmt.format(
                            sample=name,
                            ene="%2.0f" % en,
                            angle="%3.2f" % an,
                            phi="%2.1f" % ph,
                            waxs="%2.1f" % wa,
                        )
                        sample_id(user_name="SN", sample_name=sample_name)
                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=1)
        yield from bps.mv(stage.th, 0)
        yield from bps.mv(piezo.th, 0)

        yield from bps.mv(prs, 0)


def netzkeall(meas_t=0.6):
    yield from gisaxsnetzke(meas_t=0.6)
    yield from gisaxsnetzke3(meas_t=0.6)


def gisaxsquick(meas_t=0.3):
    waxs_arc = np.linspace(0, 45.5, 8)  # (2th_min 2th_max steps)
    dets = [pil300KW, pil1M]
    phi = -20
    xlocs = [25500]
    names = ["RY26n"]
    # angle = [0.2, 0.29, 0.4, 0.45]
    angle = [0.2, 0.29, 0.4]
    energ = [9580]
    assert len(xlocs) == len(names), f"Sample name/position list is borked"

    for x, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, x)

        # yield from bps.mv(GV7.open_cmd, 1 )
        # yield from alignement_gisaxs(0.2)
        # yield from bps.mv(GV7.close_cmd, 1 )

        det_exposure_time(meas_t, meas_t)
        name_fmt = "{sample}_E{ene}eV_ai{angle}deg_phi{phi}deg_wa{waxs}"
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
            for en in energ:
                yield from bps.mv(energy, en)
                # and the fastest cycle is the angle change
                for an in angle:
                    yield from bps.mvr(piezo.th, an)
                    sample_name = name_fmt.format(
                        sample=name,
                        ene="%2.0f" % en,
                        angle="%3.2f" % an,
                        phi=phi,
                        waxs="%2.1f" % wa,
                    )
                    sample_id(user_name="SN", sample_name=sample_name)
                    print(f"\n\t=== Sample: {sample_name} ===\n")
                    yield from bp.count(dets, num=4)
                    yield from bps.mvr(piezo.th, -an)

    yield from bps.mv(prs, 0)


"""
#incident angle scan
def gisaxsnetzke1(meas_t=0.3):
    waxs_arc = np.linspace(0, 45.5, 8)
    dets = [pil300KW]
    
    xlocs = [12000]
    names = ['RY5']
    phi = 0
        
    assert len(xlocs) == len(names), f'Sample name/position list is borked' 

    for x, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, x)
        #yield from alignement_gisaxs(angle = 0.15)
        #yield from bps.mvr(piezo.th, angle)
        
        det_exposure_time(meas_t, meas_t) 
        name_fmt = '{sample}_ai{angle}deg_{phi}deg_wa{waxs}'
        
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
        
            for th in np.linspace(0.2, 0.4, 2):
                yield from bps.mvr(stage.th, th)
            
                sample_name = name_fmt.format(sample=name, angle='%3.2f'%th, phi = phi, waxs='%2.1f'%wa)
                sample_id(user_name='SN', sample_name=sample_name)
            
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
                yield from bps.mvr(stage.th, -th)
 
   
#incident angle scan at different position of the sample
def gisaxsnetzke2(meas_t=1):
    waxs_arc = np.linspace(0, 32.5, 6)
    dets = [pil300KW]
    
    xlocs = [-2000, 1000, 0, 1000, 2000]
    names = ['190919-12_01_aiscan_pos1', '190919-12_01_aiscan_pos2', '190919-12_01_aiscan_pos3', '190919-12_01_aiscan_pos4', '190919-12_01_aiscan_pos5']
    phi = 7
        
    assert len(xlocs) == len(names), f'Sample name/position list is borked' 

    for x, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, x)
        #yield from alignement_gisaxs(angle = 0.15)
        #yield from bps.mvr(piezo.th, angle)
        
        det_exposure_time(meas_t, meas_t) 
        name_fmt = '{sample}_ai{angle}deg_{phi}deg_wa{waxs}'
        
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
        
            for th in np.linspace(0.05, 0.3, 6):
                yield from bps.mvr(piezo.th, th)
            
                sample_name = name_fmt.format(sample=name, angle='%3.2f'%th, phi = phi, waxs='%2.1f'%wa)
                sample_id(user_name='LC', sample_name=sample_name)
            
                print(f'\n\t=== Sample: {sample_name} ===\n')
                yield from bp.count(dets, num=1)
                yield from bps.mvr(piezo.th, -th)   
                
"""
# DONT USE!!!! realignement of tyhe sampl at each phi
def gisaxsnetzke3(meas_t=0.6):
    waxs_arc = np.linspace(0, 45.5, 8)  # (2th_min 2th_max steps)
    dets = [pil300KW, pil1M]
    xlocs = [-44500, -34800, -25700, -15500, -5000, 6900, 15200, 25500, 35500, 46800]
    names = [
        "RY13_phioffset",
        "RY15_phioffset",
        "RY16_phioffset",
        "RY17_phioffset",
        "RY18_phioffset",
        "RY19_phioffset",
        "RY21_phioffset",
        "RY26_phioffset",
        "TiN1_phioffset",
        "TiN2_phioffset",
    ]
    angle_off_from02 = [0, 0.09, 0.2]
    energ = [9540, 9580]
    phis = [-22.5, 22.5]
    assert len(xlocs) == len(names), f"Sample name/position list is borked"
    # num = 0
    for x, name in zip(xlocs, names):
        # if num > 0:
        #    yield from bps.mvr(piezo.th, ref_th_0)
        yield from bps.mv(piezo.x, x)
        # yield from alignement_gisaxs(0.15)
        # ref_th_0 = piezo.th.position

        det_exposure_time(meas_t, meas_t)
        name_fmt = "{sample}_E{ene}eV_ai{angle}deg_phi{phi}deg_wa{waxs}"
        # phi is the slowest cycle:s
        for phi in phis:  # (phi_min phi_max steps)
            yield from bps.mv(prs, phi)
            yield from alignement_gisaxs_hex_short(0.2)
            ref_th_0 = stage.th.position
            yield from bps.mvr(stage.th, ref_th_0 + 0.2)

            # waxs arc is scanned for a single phi
            for j, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                # then for a single waxs arc we change angle as relative move offset
                for a, an in enumerate(angle_off_from02):
                    yield from bps.mvr(stage.th, an)
                    # and the fastest cycle is the energy
                    for en in energ:
                        yield from bps.mv(energy, en)
                        real_an = an[a] + 0.2
                        sample_name = name_fmt.format(
                            sample=name,
                            ene="%2.0f" % en,
                            angle="%3.2f" % real_an,
                            phi=phi,
                            waxs="%2.1f" % wa,
                        )
                        sample_id(user_name="SN", sample_name=sample_name)

                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=4)
                yield from bps.mv(stage.th, ref_th_0 + 0.2)

        yield from bps.mv(prs, 0)
        # num +=1


"""        
#realignement of tyhe sampl at each phi
def gisaxsnetzke4(meas_t=1):
    waxs_arc = np.linspace(0, 32.5, 6) #(2th_min 2th_max steps)
    dets = [pil300KW]
    
    xlocs = [1010]
    names = ['190919-13_bkgnd3']
    angle = [0.2]
        
    assert len(xlocs) == len(names), f'Sample name/position list is borked' 
    num = 0
    for x, name in zip(xlocs, names):
        if num > 0:
            yield from bps.mvr(piezo.th, ref_th_0)
        yield from bps.mv(piezo.x, x)
        #yield from alignement_gisaxs(0.15)
        ref_th_0 = piezo.th.position
        
        det_exposure_time(meas_t, meas_t) 
        name_fmt = '{sample}_phiAlign2_ai{angle}deg_{phi}_wa{waxs}'
        
        for phi in np.linspace(65, 66, 2): #(phi_min phi_max steps)
            yield from bps.mv(prs, phi)
            yield from alignement_gisaxs_shorter(0.15)
            
            for j, wa in enumerate(waxs_arc):
                yield from bps.mv(waxs, wa)
                for an in angle:
                    yield from bps.mvr(piezo.th, an)
                    sample_name = name_fmt.format(sample=name, angle='%3.2f'%an, phi = phi, waxs='%2.1f'%wa)
                    sample_id(user_name='LC', sample_name=sample_name)
               
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    yield from bp.count(dets, num=1)
                    yield from bps.mvr(piezo.th, -an)
                
        yield from bps.mv(prs, 0)
        num +=1
        
        
#Silicon (100) scan
def gisaxsnetzkeSi(meas_t=1):
    waxs_arc = np.linspace(0, 32.5, 6) #(2th_min 2th_max steps)
    dets = [pil300KW]
    
    #xlocs = [-30600, -14100, 3800, 20400, 38900]
   # xlocs = [-27990, -13700, 800, 16300, 32700, 47400]
    xlocs = [1010]
    names = ['SiScGOOD2']
    angle = [0.2]
        
    assert len(xlocs) == len(names), f'Sample name/position list is borked' 
    
    for x, name in zip(xlocs, names):
        yield from bps.mv(piezo.x, x)
        
        yield from bps.mv(GV7.open_cmd, 1 )
        yield from alignement_gisaxs(0.15)
        yield from bps.mv(GV7.close_cmd, 1 )
        
        
        det_exposure_time(meas_t, meas_t) 
        name_fmt = '{sample}_ai{angle}deg_{phi}deg_wa{waxs}'
        
        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)
      #  NE
            for phi in np.linspace(-90, 90, 181): #(phi_min phi_max steps)
                yield from bps.mv(prs, phi)
                
                for an in angle:
                    yield from bps.mvr(piezo.th, an)
            
                    sample_name = name_fmt.format(sample=name, angle='%3.2f'%an, phi = phi, waxs='%2.1f'%wa)
                    sample_id(user_name='LC', sample_name=sample_name)
                    
                    print(f'\n\t=== Sample: {sample_name} ===\n')
                    #Change from 4 to 1 exposure
                    yield from bp.count(dets, num=2)
                 #   yield from bp.count(dets, num=1)
                    yield from bps.mvr(piezo.th, -an)                    
                
        yield from bps.mv(prs, 0)
"""


def gisaxs_netzke_2020_3(meas_t=0.6):
    waxs_arc = np.linspace(0, 45.5, 8)
    dets = [pil300KW]

    # xlocs = [-44500, -34800, -25700, -15500, -5000, 6900, 15200, 25500, 35500, 46800]
    # names = ['RY13_phioffset','RY15_phioffset','RY16_phioffset','RY17_phioffset','RY18_phioffset','RY19_phioffset','RY21_phioffset','RY26_phioffset','TiN1_phioffset','TiN2_phioffset']
    # assert len(xlocs) == len(names), f'Sample name/position list is borked'

    angle_off_from02 = [0.20, 0.29, 0.40]
    energ = [9540, 9580]
    phis = [-40, -20, 0]

    ref_th_0 = stage.th.position

    for name, xs, zs, aiss, ys in zip(
        names, x_piezo, z_piezo, incident_angles, y_piezo_aligned
    ):
        yield from bps.mv(piezo.x, xs)
        yield from bps.mv(piezo.y, ys)
        yield from bps.mv(piezo.z, zs)
        yield from bps.mv(piezo.th, aiss)

        det_exposure_time(meas_t, meas_t)
        name_fmt = "{sample}_E{ene}eV_ai{angle}deg_phi{phi}deg_wa{waxs}"

        # phi is the slowest cycle:s
        if waxs.arc.position > 20:
            waxs_arc = np.linspace(0, 45.5, 8)[::-1]
        else:
            waxs_arc = np.linspace(0, 45.5, 8)

        for j, wa in enumerate(waxs_arc):
            yield from bps.mv(waxs, wa)

            for phi in phis:  # (phi_min phi_max steps)
                yield from bps.mv(prs, phi)

                # check waxs value and adjust waxs range
                for a, an in enumerate(angle_off_from02):
                    yield from bps.mv(stage.th, ref_th_0 + an)

                    for en in energ:
                        yield from bps.mv(energy, en)
                        yield from bps.sleep(1)

                        sample_name = name_fmt.format(
                            sample=name,
                            ene="%2.0f" % en,
                            angle="%3.2f" % an,
                            phi=phi,
                            waxs="%2.1f" % wa,
                        )
                        sample_id(user_name="SN", sample_name=sample_name)

                        print(f"\n\t=== Sample: {sample_name} ===\n")
                        yield from bp.count(dets, num=2)

            yield from bps.mv(stage.th, ref_th_0)
        yield from bps.mv(prs, 0)


def alignement_netzke():
    global names, x_piezo, z_piezo, incident_angles, y_piezo_aligned

    # names = ['ALLS80', 'ALLS87', 'RK3', 'RK14', 'ALLS88', 'ALLS101', 'RK16', 'RK19_800C_1', 'RK19_800C_2', 'RK19_750C', 'S25', 'RK13', 'RK2']
    # x_piezo = [-50800, -42800, -35800, -29800, -22800, -14800, -7800, 200, 7200, 15200, 22200, 29200, 36200]
    # z_piezo = [  1660,   1660,   1460,    960,    560,    160,   160, 160, -240,  -240,  -440,  -740, -1040]

    names = [
        "ALLS82",
        "ALLS102",
        "ALLS112",
        "ALLS68",
        "ALLS77",
        "RK1",
        "ALLS76",
        "ALLS78",
        "ALLS84",
        "ALLS103",
        "ALLS91",
        "ALLS86",
        "RK20",
        "RA3",
        "ALLS81",
    ]
    x_piezo = [
        -50000,
        -44000,
        -37000,
        -30000,
        -23000,
        -16000,
        -9000,
        -2000,
        5000,
        13000,
        20000,
        28000,
        36000,
        43000,
        50000,
    ]
    z_piezo = [
        560,
        560,
        560,
        560,
        360,
        360,
        360,
        160,
        160,
        -40,
        -340,
        -340,
        -540,
        -740,
        -1540,
    ]

    incident_angles = []
    y_piezo_aligned = []

    smi = SMI_Beamline()
    yield from smi.modeAlignment(technique="gisaxs")

    for name, xs_piezo, zs_piezo in zip(names, x_piezo, z_piezo):
        yield from bps.mv(piezo.x, xs_piezo)
        # yield from bps.mv(piezo.y, ys_piezo)
        yield from bps.mv(piezo.z, zs_piezo)

        yield from alignement_gisaxs_multisample(angle=0.15)

        incident_angles = incident_angles + [piezo.th.position]
        y_piezo_aligned = y_piezo_aligned + [piezo.y.position]

        print(incident_angles)
        print(y_piezo_aligned)

    yield from smi.modeMeasurement()

    print(incident_angles)
    print(y_piezo_aligned)


# y_piezo_aligned = array([7271.133, 7235.479, 7214.69 , 7177.205, 7144.364, 7151.092, 7063.728, 7081.229, 7058.901, 7029.661, 6874.397, 6958.301, 6971.521])
# incident_angles = [ 0.341887,  0.978769,  0.193741,  0.478084,  0.728999,  0.429933, 0.929884,  0.660595,  0.459128,  0.078492,
#     0.262723,  0.100632, -0.328383]

# incident_angles = array([-1.226571, -0.552806,  0.28984 , -0.419068,  0.103962, -0.162368, 0.42735 , -0.451796,  0.124283, -1.463176, -0.168004,
# -0.62571, -0.23411 , -0.106975, -0.307471])
# y_piezo_aligned =array([7144.954, 7172.772, 7184.785, 7133.138, 7088.943, 7091.481, 7050.918, 7039.402, 7007.882, 6938.484, 6947.378, 6943.667,
# 6901.995, 6796.63 , 6892.514])
