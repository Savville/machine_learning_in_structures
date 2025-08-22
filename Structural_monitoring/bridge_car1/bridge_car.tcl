# Wipe previous model
wipe

# Model builder for 2D, 3 DOF per node
model BasicBuilder -ndm 2 -ndf 3

# Bridge parameters
set L 30.0; # Length (m)
set E 3.0e10; # Young's modulus (Pa)
set A 0.5; # Area (m2)
set I 0.1; # Moment of inertia (m4)
set rho 2500.0; # Density (kg/m3)
set numElem 30; # Number of elements
set elemL [expr $L / $numElem]; # Element length

# Nodes
for {set i 0} {$i <= $numElem} {incr i} {
    node [expr $i+1] [expr $i * $elemL] 0.0
}

# Boundary conditions (simply supported)
fix 1 1 1 0; # Fixed in x, y, free rotation
fix [expr $numElem + 1] 0 1 0; # Roller in x, fixed y, free rotation

# Material
section Elastic 1 $E $A $I

# Define coordinate transformation (Linear, tag 1)
geomTransf Linear 1

# Elements (dispBeamColumn for beam)
for {set i 1} {$i <= $numElem} {incr i} {
    element dispBeamColumn $i $i [expr $i+1] 3 1 1 -mass [expr $rho * $A]
}

# Add mass to nodes for dynamic analysis
for {set i 1} {$i <= [expr $numElem + 1]} {incr i} {
    mass $i [expr $rho * $A * $elemL / 2.0] [expr $rho * $A * $elemL / 2.0] 0.0
}

# --- Modal Analysis: Compute first 3 frequencies ---
set numModes 3
set lambda [eigen -fullGenLapack $numModes]
set freqs {}
foreach lam $lambda {
    lappend freqs [expr sqrt($lam)/(2*3.14159)]
}

# Write frequencies to file
set fp [open "frequencies.txt" w]
puts $fp "Mode,Freq(Hz)"
for {set i 0} {$i < $numModes} {incr i} {
    puts $fp "[expr $i+1],[lindex $freqs $i]"
}
close $fp

# --- Transient Analysis: Moving Load ---

# Damping (5% Rayleigh)
set freq1 3.0; # Approximate first frequency (Hz)
set zeta 0.05
set a0 [expr $zeta * 2 * 3.14159 * $freq1]
set a1 [expr $zeta * 2 / (3.14159 * $freq1)]
rayleigh $a0 0 $a1 0

# Vehicle parameters
set P -10000.0; # Load 10 kN downward
set v 20.0; # Speed 20 m/s
set dt 0.001; # Time step
set T [expr $L / $v]; # Crossing time
set nSteps [expr int($T / $dt)]

# Pattern for load
timeSeries Linear 1
pattern Plain 1 1 {}

# Recorder for midspan acceleration (node at mid, dof 2 for vertical)
set midNode [expr int($numElem / 2) + 1]
recorder Node -file accel.txt -time -node $midNode -dof 2 accel

# Analysis setup
system BandGeneral
constraints Plain
numberer RCM
test NormDispIncr 1.0e-6 6
algorithm Newton
integrator Newmark 0.5 0.25
analysis Transient

# Simulate moving load by updating position each step
for {set step 0} {$step < $nSteps} {incr step} {
    set pos [expr $v * $step * $dt]
    if {$pos > $L} {break}
    # Find element for load
    set elemId [expr int($pos / $elemL) + 1]
    if {$elemId > $numElem} {continue}
    # Apply load to nodes of element
    set node1 $elemId
    set node2 [expr $elemId + 1]
    set xi [expr ($pos - ($elemId-1)*$elemL) / $elemL]
    load $node1 0.0 [expr $P * (1 - $xi)] 0.0
    load $node2 0.0 [expr $P * $xi] 0.0
    analyze 1 $dt
    load $node1 0.0 0.0 0.0
    load $node2 0.0 0.0 0.0
}