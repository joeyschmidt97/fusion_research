This code is used to fetch simulation from GENE gyrokinetic simulations, only grabbing the necessary info needed for your use (hence speeding up the code if several simulations are needed for analysis). 

It functions by specifying a filepath (or list of paths) where it searches for GENE simulation data, specifying the quantities you desire (i.e. gamma, Q_ES, bpar, etc.), and the species you want this information for. This approach allows the search to be much faster as opposed to loading at the data and filtering. It also has functionality to only get relevant data based on specified parameter criteria (i.e. "kymin < 10", "1 < gamma < 4", "time==last", etc.) allowing a speed-up in getting relevant data.

The output simulation data can be given as a dictionary or pandas dataframe for use in other workflows. 

Example use code can be found in `tests/src_tests/simulation_data.ipynb` but an example is given below:




```python
from GENE_sim_reader.src.dict_simulation_data import filepath_to_simulation_dict_list


```


```python
from GENE_sim_reader.src.dict_simulation_data import sim_filepath_to_df


```


