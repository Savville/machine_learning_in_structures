wipe;
model Basic -ndm 2 -ndf 2;
node 1 0.0 0.0;
node 2 6.0 0.0;
node 3 3.0 [expr 3*sqrt(3)];
fix 1 1 1;  # Pinned at Node 1
fix 2 0 1;  # Roller at Node 2
fix 3 0 0;  # Free at Node 3
uniaxialMaterial Elastic 1 [expr 200e9];  # E = 200 GPa
element truss 1 1 2 0.001 1;  # Member 1-2, A=0.001
element truss 2 1 3 0.001 1;  # Member 1-3
element truss 3 2 3 0.001 1;  # Member 2-3
timeSeries Constant 1;
pattern Plain 1 1 {
    load 3 0.0 -10000.0;  # Load at Node 3
}
system UmfPack;
constraints Plain;
numberer RCM;
test NormDispIncr 1.0e-8 6;
algorithm Linear;
integrator LoadControl 1;
analysis Static;
analyze 1;
# Output forces (in OpenSees, use print ele or recorder for results)
recorder Element -ele 1 2 3 -file forces.txt axialForce;
record;