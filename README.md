# niche-inheritance-trees
A simple coarse-grained statistical model of niche construction coupled to speciation.

## Usage
- The main tree data structure and helper functions are defined in "utils.py". Import this file for any simulation.

- "simulate_AC.py" is an example script that simulates trees and gathers C(A) data.

- Inside the "data" folder, each subfolder stores the data as well as the simulation script for that case.
For example, "EAD" folder stores the Edge-length Abundance Distribution data for several sets of parameters. To
use a set of parameters different from the paper, please edit the simulation script directly.

- The plotting codes for all figures are also included in the "plotting_for_publish" folder. Plots can be reproduced
from the data in the data folder. (The only exception is fig.S2, which needs additional simulation done to save the
niche values for all the nodes.)
