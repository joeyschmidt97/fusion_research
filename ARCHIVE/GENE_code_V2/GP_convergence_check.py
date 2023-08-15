import os

def convergence_check(simulation_dict):
    #returns simulation status as CONVERGED or NOT CONVERGED based on omega file
    simulation_files = simulation_dict['simulation files']
    filetype = 'omega' #filetype to check simulation status
    
    status = 'NOT CONVERGED'    #default to not converged unless proven otherwise

    for filepath in simulation_files:
        filename = os.path.basename(filepath)
        
        check_omega = filename.startswith(filetype) # check if file is omega file
        
        if check_omega:
            check_nonempty = (os.stat(filepath).st_size != 0)   # check if omega file is empty or has data            
            if check_nonempty:
                status = 'CONVERGED'

    return status
