import numpy as np
t = np.arange(0, 30, 0.02)
a = 0.15 * np.sin(2 * np.pi * 2 * t) * np.exp(-0.05 * 2 * np.pi * 2 * t)
np.savetxt('nairobi_eq.dat', np.column_stack((t, a)), fmt='%.3f %.4f')