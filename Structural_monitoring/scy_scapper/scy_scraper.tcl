# Wipe previous model
wipe

# Model setup
model basic -ndm 2 -ndf 3

# Nodes: (1) fixed base, (2) mat foundation at 2.5 m depth, (3) column top
node 1 0.0 -2.5
node 2 0.0 -2.5
node 3 0.0 97.5  ; # 100 m - 2.5 m = 97.5 m above ground

# Fixities
fix 1 1 1 1
fix 2 0 1 0  ; # Allow horizontal movement at foundation

# Soil springs (zero-length elements for 25 m x 25 m mat at 2.5 m depth)
uniaxialMaterial Elastic 1 947053750.0  ; # Vertical spring (kN/m)
uniaxialMaterial Elastic 2 97518125.0   ; # Horizontal spring (kN/m)
uniaxialMaterial Viscous 3 9733.0 1.0       ; # Damping (kN·s/m)
element zeroLength 1 1 2 -mat 1 2 3 -dir 1 2 1

# Column materials
uniaxialMaterial Concrete01 4 -30.0 -0.002 -12.0 -0.005  ; # Concrete: f'c = 30 MPa
uniaxialMaterial Steel01 5 500.0 200000.0 0.01           ; # Steel: fy = 500 MPa
section Fiber 1 {
    patch rect 4 20 20 -0.5 -0.5 0.5 0.5                 ; # Concrete core
    layer straight 5 16 0.0004909 0.4 0.4 0.4 -0.4       ; # 16 bars of 25 mm
}

# Column element (equivalent for 100 m tall building)
geomTransf Linear 1
element nonlinearBeamColumn 2 2 3 10 1 1

# Mass at column top (10,000,000 kg)
mass 3 10000.0 0.0 0.0

# Axial load (264,000 kN)
pattern Plain 2 Linear {
    load 3 0.0 -264000.0 0.0
}

# Ground motion (Nairobi-specific, 2006 Tanzania earthquake scaled to 0.15g)
timeSeries Path 1 -filePath nairobi_eq.dat -dt 0.02 -factor 9.81
pattern UniformExcitation 1 1 -accel 1

# Damping (5% critical)
rayleigh 0.05 0.0 0.0 0.05

# Analysis
system UmfPack
constraints Plain
integrator Newmark 0.5 0.25
analysis Transient

# Record outputs
recorder Node -file disp.out -time -node 3 -dof 1 disp
recorder Element -file shear.out -time -ele 2 force

# Run analysis
for {set i 0} {$i < 1500} {incr i} {
    analyze 1 0.02
}