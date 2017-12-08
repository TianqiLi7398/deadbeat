# Data collected in Dec 7

## Experiments: 3 Trails
In each trail, there are 2 mins long data collected.
- Qualysis(Camera): 1kHz Capture rate, Unit mm
- Arduino(Motor): 100Hz Capture rate, Unit rad
*** Specially, in the end of first trail, you can see there is a failure jump. Please exclude that.

## Raw files: CSV files

Ard: Arduino files, data of motor angle
- time: (in sec)
- ard: angle_1(rad), angle_2(rad), stair_command(each number from 0-4 related to a specific height of stairs)

Qua: Calibrated files of Foot and Top trajectory

## Processed files: json files
