# analysis.tcl
# Tcl script for OpenSees to perform modal analysis on a bridge for damage detection
# Corrected for eigenvalue errors and element redefinition

wipe; # Clear previous model data

# Define model
model BasicBuilder -ndm 2 -ndf 3; # 2D model with 3 DOFs per node (UX, UY, RZ)

# Define geometry (10-meter beam bridge with 5 elements)
set L 10.0; # Total length (m)
set nElem 5; # Number of elements
set elemLength [expr $L / $nElem]; # Length per element
set nNodes [expr $nElem + 1]; # Number of nodes (0 to 5)

# Material properties
set E 2.0e11; # Young's modulus (Pa, steel)
set A 0.01;   # Cross-sectional area (m^2)
set I 8.0e-5; # Moment of inertia (m^4)

# Define nodes
for {set i 0} {$i < $nNodes} {incr i} {
    set xCoord [expr $i * $elemLength];
    node $i $xCoord 0.0; # Nodes 0 to 5 along X-axis, Y=0
}

# Boundary conditions (fixed at left, roller at right)
fix 0 1 1 1; # Fix node 0 (UX, UY, RZ)
fix 5 0 1 0; # Roller at node 5 (UY fixed)

# Add mass to nodes for dynamic analysis
for {set i 0} {$i < $nNodes} {incr i} {
    mass $i 1000.0 1000.0 0.0; # Mass (kg) for UX, UY, RZ
}

# Define material
uniaxialMaterial Elastic 1 $E; # Elastic material with tag 1

# Define coordinate transformation
geomTransf Linear 1; # Linear transformation with tag 1

# Define elements
for {set i 0} {$i < $nElem} {incr i} {
    set node1 $i;
    set node2 [expr $i + 1];
    element elasticBeamColumn $i $node1 $node2 $A $E $I 1; # Beam elements
}

# Define recorders for baseline frequencies
recorder Node -file "baseline_frequencies.txt" -node 1 -dof 2 disp; # Vertical displacement at node 1

# Perform eigenvalue analysis for baseline
set numModes 3; # Number of modes to compute
set lambda [eigen -fullGenLapack $numModes]; # Eigenvalues
set freqs {};
foreach lam $lambda {
    lappend freqs [expr sqrt($lam)/(2*3.14159)]; # Convert to frequencies (Hz)
}
puts "Baseline Frequencies (Hz): $freqs"

# Simulate damage (reduce stiffness of element 2 by 20%)
set damageFactor 0.8; # 20% stiffness reduction
set E_damaged [expr $E * $damageFactor];
uniaxialMaterial Elastic 2 $E_damaged; # New material for damaged element
remove element 2; # Remove existing element 2
element elasticBeamColumn 2 2 3 $A $E_damaged $I 1; # Redefine element 2

# Recorder for damaged state
recorder Node -file "damaged_frequencies.txt" -node 1 -dof 2 disp;

# Eigenvalue analysis for damaged state
set lambda_damaged [eigen -fullGenLapack $numModes];
set freqs_damaged {};
foreach lam $lambda_damaged {
    lappend freqs_damaged [expr sqrt($lam)/(2*3.14159)];
}
puts "Damaged Frequencies (Hz): $freqs_damaged"

# Output results for AI processing
set fp [open "modal_data.csv" w];
puts $fp "State,Freq1,Freq2,Freq3";
puts $fp "Baseline,[lindex $freqs 0],[lindex $freqs 1],[lindex $freqs 2]";
puts $fp "Damaged,[lindex $freqs_damaged 0],[lindex $freqs_damaged 1],[lindex $freqs_damaged 2]";
close $fp;

wipe; # Clean up model
puts "Analysis complete. Modal data saved to modal_data.csv"