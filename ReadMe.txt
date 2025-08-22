# Bridge Moving Load Simulation (`bridge_car2`)

## Overview

This project simulates the dynamic response of a simply supported bridge subjected to a moving vehicle load using OpenSees. The main script, `bridge_car2.tcl`, builds a finite element model of the bridge, applies a moving point load, and records the vertical acceleration at the bridge's midspan.

---

## Model Description

- **Bridge Type:** Simply supported beam
- **Length:** 30 meters
- **Material Properties:**
  - Young's Modulus (E): 3.0e10 Pa
  - Cross-sectional Area (A): 0.5 m²
  - Moment of Inertia (I): 0.1 m⁴
  - Density (ρ): 2500 kg/m³
- **Mesh:** 100 beam elements (fine mesh for accuracy)
- **Boundary Conditions:**
  - Node 1: Fixed in X and Y, free rotation
  - Node 101: Roller (fixed in Y, free in X and rotation)

---

## Dynamic Analysis

- **Damping:** 5% Rayleigh damping, estimated from the first mode
- **Vehicle Load:**
  - Magnitude: 15,000 N (downward)
  - Speed: 25 m/s
- **Load Application:** The moving load is applied as a point load at the correct position on the relevant element using `eleLoad -beamPoint`.
- **Time Step:** 0.0005 s
- **Total Steps:** Calculated to cover the full crossing time plus a few extra steps

---

## Output

- **accello.txt:**  
  Contains two columns:  
  - Time (s)  
  - Vertical acceleration at the midspan node (m/s²)  
  This file records the bridge's dynamic response as the vehicle crosses.

---

## What Happens in the Simulation

1. **Model Setup:**  
   The bridge is discretized into 100 elements, and all material, geometric, and boundary conditions are defined.

2. **Moving Load Simulation:**  
   At each time step, the vehicle's position is updated, and the load is applied to the appropriate element at the correct relative position. The structure is analyzed for that time step, and the load pattern is removed for the next step.

3. **Response Recording:**  
   The vertical acceleration at the bridge's midspan is recorded at every time step, capturing the dynamic effects of the moving load.

4. **Physical Interpretation:**  
   - As the vehicle enters, crosses, and leaves the bridge, the midspan experiences acceleration due to the induced vibrations.
   - The recorded acceleration shows how the bridge responds dynamically, including oscillations due to its natural frequencies and damping.

---

## How to Use

1. Run `bridge_car2.tcl` in OpenSees.
2. After the run, open `accello.txt` to view the acceleration time history at the bridge's midspan.
3. For frequency analysis, you can perform an FFT on the acceleration data using Python, MATLAB, or similar tools.

---

## Notes

- The script uses a fine mesh and direct element loading for improved accuracy in dynamic response.
- No modal analysis or frequency output is included in this script (unlike `bridge_car.tcl`).
- The output can be used for further analysis, such as identifying dominant vibration frequencies or assessing bridge health.

---

**Author:**  
Williams Ochieng 
August 2025
