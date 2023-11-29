This code is used to fetch simulation from GENE gyrokinetic simulations, only grabbing the necessary info needed for your use (hence speeding up the code if several simulations are needed for analysis). 

It functions by specifying a filepath (or list of paths) where it searches for GENE simulation data, specifying the quantities you desire (i.e. gamma, Q_ES, bpar, etc.), and the species you want this information for. This approach allows the search to be much faster as opposed to loading at the data and filtering. It also has functionality to only get relevant data based on specified parameter criteria (i.e. "kymin < 10", "1 < gamma < 4", "time==last", etc.) allowing a speed-up in getting relevant data.

The output simulation data can be given as a dictionary or pandas dataframe for use in other workflows. 

Example use code can be found in `tests/src_tests/simulation_data.ipynb` but examples are given below:

# Fetching GENE simulation data as pandas dataframe

```python
from GENE_sim_reader.src.dict_simulation_data import sim_filepath_to_df

# load filepaths as either a list of filepaths or a filepath string
filepath = ['/pscratch/sd/u/username/folder1', '/pscratch/sd/u/username/folder2']

# specify criteria to fetch simulation data
# Note: if no criteria is set but the quantity is desired for further analysis it must be specified as a string (i.e. "Q_EM")
# (if no criteria is given then only basic simulation info (filepath, parameters, suffix, etc.) will be fetched)
criteria1 = ['time<0.05', 'gamma>0', 'Q_ES < 3e-2', 'Q_EM', 'Gamma_ES']

# specify species that you want to fetch data for (if nothing is specified all species will be loaded)
spec = ['e', 'i']

# plug in requirements and fetch simulation data
sim_df = sim_filepath_to_df(filepath_list = filepath, criteria_list = criteria1, load_spec = spec)
```

This outputs a pandas dataframe with the specified data fulfilling the criteria given in each column of the dataframe.

For example, this dataframe can be used in other workflows like plotting data or finding fingerprints for instabilities. A simply example is given below for plotting the growth rates across several simulations.
```python
import matplotlib.pyplot as plt

from GENE_sim_reader.src.dict_simulation_data import sim_filepath_to_df

filepath = '/pscratch/sd/u/username/folder1'
criteria = 'gamma' #fetches gamma from omega filetype, if 'gamma' is not specified then sim_df['gamma'] will throw an error

sim_df = sim_filepath_to_df(filepath_list=filepath, criteria_list=criteria)

plt.plot(sim_df['kymin'], sim_df['gamma'])

```


If quantities are specified in the 'criteria_list' the appropriate quantity will be loaded into the dataframe (specify 'gamma' and 'omega' to load them into the dataframe, otherwise, they will not be loaded)

The current quantities and their associated filetypes are listed below:

Data from omega filetype:
```
['gamma','omega']
```

Data from nrg filetype:
```
['time', 'n_mag' , 'u_par_mag', 'T_par_mag', 'T_perp_mag', 'Gamma_ES', 'Gamma_EM', 'Q_ES', 'Q_EM', 'Pi_ES', 'Pi_EM']
```

Data from field filetype:
```
['time', 'phi', 'apar', 'bpar']
```

## Warning messages
Note: Warning messages will output if the criteria is too strict(no simulations fulfill any criteria), simulation data is buried too deep in directories (default search depth is 3 directories deep), quantities are not typed correct (i.e. """QES" , "q_es", "Q_ESs", etc. when correct quantity string is "Q_ES"), no simulations are found (directory is empty or contains no GENE simulation data), and several other errors.

# Fetching GENE simulation data as dictionaries

By default, the simulation data is loaded as dictionary types. The pandas dataframe is the preferred method of accessing the simulation data but the dictionaries can be used as follows:

```python
from GENE_sim_reader.src.dict_simulation_data import filepath_to_simulation_dict_list

# load filepaths as either a list of filepaths or a filepath string
filepath_list = ['/pscratch/sd/u/username/folder1', '/pscratch/sd/u/username/folder2']

# specify criteria to fetch simulation data
# Note: if no criteria is set but the quantity is desired for further analysis it must be specified as a string (i.e. "Q_EM")
criteria1 = ['time==last', 'gamma>0', 'Q_ES < 3e-2', 'Q_EM', 'Gamma_ES']

# specify species that you want to fetch data for
spec = ['e', 'i']

# plug in requirements and fetch simulation data
simulation_dict_list, _ = filepath_to_simulation_dict_list(filepath_list = filepath, criteria_list = criteria, load_spec = spec)

```
This outputs a list of simulation dictionaries with the specified data fulfilling the criteria.

Simulation dicts have keys information for the simulations such as 'directory', 'suffix', 'status', 'parameters_dict', etc. that can be used to locate and characterize the simulation. Moreover if quantities are specified in the 'criteria_list' the appropriate dict will be loaded that has said quantity (specify 'gamma' and the 'omega_dict' is loaded into the simulation_dict)

The current dictionaries and their quantities are listed below:
```
omega_dict > ['gamma','omega']
nrg_dict   > ['time', 'n_mag' , 'u_par_mag', 'T_par_mag', 'T_perp_mag', 'Gamma_ES', 'Gamma_EM', 'Q_ES', 'Q_EM', 'Pi_ES', 'Pi_EM']
field_dict > ['time', 'phi', 'apar', 'bpar']
```

If criteria is required for other use (i.e. plotting boundaries) it can be called from the function as follows:
```python

simulation_list, criteria_list = filepath_to_simulation_dict_list(filepath_list=filepath, criteria_list=criteria1, load_spec=['e', 'i'])
```

