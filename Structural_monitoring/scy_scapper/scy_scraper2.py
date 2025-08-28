import openseespy.opensees as ops
import numpy as np
import matplotlib.pyplot as plt

# Wipe previous model
ops.wipe()

# Model setup
ops.model('basic', '-ndm', 2, '-ndf', 3)

# Nodes: (1) fixed base, (2) mat foundation at 2.5 m depth, (3) column top
ops.node(1, 0.0, -2.5)   # base (foundation bottom)
ops.node(2, 0.0, 0.0)    # ground level (foundation top/column base)
ops.node(3, 0.0, 97.5)   # column top

# Fixities
ops.fix(1, 1, 1, 1)
ops.fix(2, 0, 1, 0)

# Soil springs (zero-length element)
ops.uniaxialMaterial('Elastic', 1, 947053750.0)  # Vertical
ops.uniaxialMaterial('Elastic', 2, 97518125.0)   # Horizontal
ops.uniaxialMaterial('Viscous', 3, 9733.0, 1.0)  # Damping
ops.element('zeroLength', 1, 1, 2, '-mat', 1, 2, 3, '-dir', 1, 2, 1)

# Column section (improve fiber section definition as needed)
ops.uniaxialMaterial('Concrete01', 4, -30.0, -0.002, -12.0, -0.005)
ops.uniaxialMaterial('Steel01', 5, 500.0, 200000.0, 0.01)
ops.section('Fiber', 1)
ops.patch('rect', 4, 20, 20, -0.5, -0.5, 0.5, 0.5)
ops.layer('straight', 5, 8, 0.0004909, -0.4, 0.4, -0.4, -0.4)  # bottom
ops.layer('straight', 5, 8, 0.0004909, 0.4, 0.4, 0.4, -0.4)    # top

# Column element
ops.geomTransf('Linear', 1)
ops.element('nonlinearBeamColumn', 2, 2, 3, 10, 1, 1)

# Mass at column top (10,000,000 kg)
ops.mass(3, 10000.0, 0.0, 0.0)

# Axial load (264,000 kN)
ops.timeSeries('Linear', 2)
ops.pattern('Plain', 2, 2)
ops.load(3, 0.0, -264000.0, 0.0)

# Ground motion (Nairobi-specific, 2006 Tanzania earthquake scaled to 0.15g)
ops.timeSeries('Path', 1, '-filePath', r'C:\Users\User\Desktop\machine_learning\Structural_monitoring\scy_scapper\nairobi_eq.dat', '-dt', 0.02, '-factor', 9.81)
ops.pattern('UniformExcitation', 1, 1, '-accel', 1)

# Damping (5% critical)
ops.rayleigh(0.05, 0.0, 0.0, 0.05)

# Analysis
ops.system('UmfPack')
ops.constraints('Plain')
ops.integrator('Newmark', 0.5, 0.25)
ops.analysis('Transient')

# Record outputs
ops.recorder('Node', '-file', 'disp.out', '-time', '-node', 3, '-dof', 1, 'disp')
ops.recorder('Element', '-file', 'shear.out', '-time', '-ele', 2, 'force')

# Run analysis
disp = []
time = []
dt = 0.02
for i in range(1500):
    ops.analyze(1, dt)
    disp.append(ops.nodeDisp(3, 1))
    time.append(i * dt)

# Plot results
plt.plot(time, disp)
plt.xlabel('Time (s)')
plt.ylabel('Top Displacement (m)')
plt.title('Displacement Time History - 30-Story Building')
plt.grid(True)
plt.show()