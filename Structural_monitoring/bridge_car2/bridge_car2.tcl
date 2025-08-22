wipe
model BasicBuilder -ndm 2 -ndf 3

set L 30.0; set E 3.0e10; set A 0.5; set I 0.1; set rho 2500.0
set numElem 100; set elemL [expr $L / $numElem]  
# Finer mesh for accuracy

# Nodes
for {set i 0} {$i <= $numElem} {incr i} {
    node [expr $i+1] [expr $i * $elemL] 0.0
}

# Boundaries
fix 1 1 1 0
fix [expr $numElem + 1] 0 1 0

# Section and integration
section Elastic 1 $E $A $I
beamIntegration Lobatto 1 1 3

# Define coordinate transformation (tag 1)
geomTransf Linear 1

# Elements
for {set i 1} {$i <= $numElem} {incr i} {
    element dispBeamColumn $i $i [expr $i+1] 1 1 -mass [expr $rho * $A]
}

# Damping (5%)
set omega1 [expr pow((3.14159/$L),2) * sqrt($E*$I/($rho*$A))]  
# Approx first freq
rayleigh [expr 0.05*2*$omega1] 0.0 [expr 0.05*2/$omega1] 0.0

# Vehicle
set P -15000.0; set v 25.0  
# Increased load/speed for visible response
set dt 0.0005; set T [expr $L / $v]; set nSteps [expr int($T / $dt) + 10]

timeSeries Constant 1 -factor 1.0
set midNode [expr int($numElem / 2) + 1]
recorder Node -file accello.txt -time -node $midNode -dof 2 accel

system BandGeneral
constraints Plain
numberer RCM
test NormDispIncr 1.0e-6 6
algorithm Newton
integrator Newmark 0.5 0.25
analysis Transient

for {set step 0} {$step < $nSteps} {incr step} {
    set pos [expr $v * $step * $dt]
    if {$pos > $L} {break}
    pattern Plain 1 1 {}
    set elemId [expr int($pos / $elemL) + 1]
    if {$elemId > $numElem} {set elemId $numElem}
    set relPos [expr ($pos - ($elemId-1)*$elemL) / $elemL]
    if {$relPos >= 1.0} { set relPos 0.999 }
    eleLoad -ele $elemId -type -beamPoint $P $relPos
    analyze 1 $dt
    remove loadPattern 1
}