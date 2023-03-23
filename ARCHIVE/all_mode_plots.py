import os

# sys.path.insert(1, '/global/homes/j/joeschm/ifs_scripts')
# import plot_scan_info_efit

discharge = '129015'



if discharge == '129015':

    path1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/COMBINED_DATA/COMBINED_Impurities_OM_top/all_scans'
    os.chdir(path1)
    print('current directory:', os.getcwd())
    os.system("/global/homes/j/joeschm/ifs_scripts/plot_scan_info_efit.py 0000 '129015 (OM)'")

    path1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/COMBINED_DATA/COMBINED_OM_top_30NE_minus/all_scans'
    os.chdir(path1)
    print('current directory:', os.getcwd())
    os.system("/global/homes/j/joeschm/ifs_scripts/plot_scan_info_efit.py 0000 '129015 (OM density -30%)'")

    path1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129015/COMBINED_DATA/COMBINED_OM_top_30NE_plus/all_scans'
    os.chdir(path1)
    print('current directory:', os.getcwd())
    os.system("/global/homes/j/joeschm/ifs_scripts/plot_scan_info_efit.py 0000 '129015 (OM density +30%)'")



elif discharge == '129038':

    path1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/COMBINED_DATA/COMBINED_Impurities_OM_top/all_scans'
    os.chdir(path1)
    print('current directory:', os.getcwd())
    os.system("/global/homes/j/joeschm/ifs_scripts/plot_scan_info_efit.py 0000 '129038 (OM)'")

    path1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/COMBINED_DATA/COMBINED_OM_top_30NE_minus/all_scans'
    os.chdir(path1)
    print('current directory:', os.getcwd())
    os.system("/global/homes/j/joeschm/ifs_scripts/plot_scan_info_efit.py 0000 '129038 (OM density -30%)'")

    path1 = '/global/cscratch1/sd/joeschm/ST_research/NSTXU/129038/COMBINED_DATA/COMBINED_OM_top_30NE_plus/all_scans'
    os.chdir(path1)
    print('current directory:', os.getcwd())
    os.system("/global/homes/j/joeschm/ifs_scripts/plot_scan_info_efit.py 0000 '129038 (OM density +30%)'")


