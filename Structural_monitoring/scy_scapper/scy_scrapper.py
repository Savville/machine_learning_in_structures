import numpy as np

# Model parameters
column_height = 100.0      # m
foundation_depth = 2.5     # m
mat_size = 25.0            # m (not directly used, for context)
mass_top = 1e7             # kg
axial_load = 264000.0      # kN
dt = 0.02                  # s
n_steps = 1500

# Soil spring properties
k_vert = 947053750.0       # kN/m
k_horiz = 97518125.0       # kN/m
c_damp = 9733.0            # kN·s/m

# Column material properties (Concrete01 and Steel01)
fc = -30.0                 # MPa
epsc0 = -0.002
fcu = -12.0                # MPa
epscu = -0.005
fy = 500.0                 # MPa
E_steel = 200000.0         # MPa
b_steel = 0.01

# Ground motion (load from file)
gm = np.loadtxt('nairobi_eq.dat')
gm_time = gm[:, 0]
gm_accel = gm[:, 1] * 9.81  # scale to m/s^2

# Preallocate arrays for results
disp = np.zeros(n_steps)
shear = np.zeros(n_steps)

# Placeholder for structural analysis (requires FE library, e.g., OpenSeesPy)
# Here, we only show the structure of the script and data handling

for i in range(n_steps):
    # At each step, apply ground motion and axial load
    # Perform dynamic analysis step (not implemented here)
    # Update disp[i] and shear[i] with results from analysis
    pass

# Save outputs (format similar to OpenSees recorders)
np.savetxt('disp.out', np.column_stack((np.arange(0, n_steps*dt, dt), disp)), fmt='%.4f %.6f')
np.savetxt('shear.out', np.column_stack((np.arange(0, n_steps*dt, dt), shear)), fmt='%.4f %.6f')

print("Analysis complete. Results saved to disp.out and shear.out.")

# Note:
# This script sets up the data and output structure.
# To perform the actual structural dynamic analysis, use OpenSeesPy or