# Deadbeat notandum

This repository contains research records (data, plots, code) for Minitar Hopper deadbeat control. This project is conducted by Lab of Prof. Sam Burden in University of Washington, collaborated with Lab of Prof. Shai Revzen in University of Michigan.

The readme file will keep updated.

## Updates

### Dec 7th
Data collected for look-up table. (2 trails total)
Method:
- hopper jumps 10 times per stair transition, stair transitted randomly. Stair height: {-2, 8, 18, 28} mm.
- 2 Markers's trajectory (x,y,t) (Foot and Top) captured at 1kHz by Qualysis, offline (recorded and exported to .mat files in Qualysis software)
- 2 Motors angle (theta_1, theta_2, t) collected by Arduino mainboard in 100 Hz.
- Plot shows obvious change in Top Marker after each transition.


### Dec 5th 
Tianqi redesigned this repo to make it readable.

### Nov 30
Data collected for look-up table. (3 trils total)
Method:
- hopper jumps 20 times per stair transition, stair transitted randomly. Stair height: {-5, 0, 5, 10, 15} mm.
- 2 Markers's trajectory (x,y,t) (Foot and Top) captured at 1kHz by Qualysis, offline (recorded and exported to .mat files in Qualysis software)
- 2 Motors angle (theta_1, theta_2, t) collected by Arduino mainboard in 100 Hz.
- Plot shows no obvious change in Top Marker after each transition. Higher stair required.

### Nov 14
Data collected for look-up table.
Method:
- hopper jumps 20 times per stair transition, stair transitted randomly. Stair height: {-5, 0, 5, 10, 15} mm.
- 2 Markers's trajectory (x,y,t) (Foot and Top) captured at 100 Hz by Qualysis, real-time (use pyserial to stream data from Qualysis into VirtualMachine).
- 2 Motors angle (theta_1, theta_2, t) collected by Arduino mainboard in 100 Hz.
- Smoother trajectory required.

## Repo Notation
### data
All data(raw and processed) will go in this data, with notation of collected date

### plot
plot result of specific dataset collected
