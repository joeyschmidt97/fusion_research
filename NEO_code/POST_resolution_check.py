#!/usr/bin/env python3

from POST_out_neo_run_2_dict import out_neo_data_2_dict

info_dict = out_neo_data_2_dict()

sumZsGammas = info_dict['sum Z_s Gamma_s']
r_a = info_dict['r/a']
print('At r/a =', r_a, 'the value of "sum Z_s Gamma_s" is', sumZsGammas)

all_tests = True
limit = 0.1

for spec in info_dict['species']:
    spec_z = spec['z']
    spec_pflux = spec['pflux']
    ratio = abs(sumZsGammas/spec_pflux)
    ratio_test = (ratio < limit)

    all_tests *= ratio_test

    print('For species of charge', spec_z, 'pflux is', spec_pflux, 'and the ratio (sum Zs Gammas/pflux) < ', limit, 'is:', ratio_test)

print('')
print('All ratio tests passed as:', all_tests)