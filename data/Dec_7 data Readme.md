# Data collected in Dec 7

## Experiments: 2 Trails
In each trail, there are 2 mins long data collected.
- Qualysis(Camera): 1kHz Capture rate, Unit mm
- Arduino(Motor): 100Hz Capture rate, Unit rad

## Datas
### Raw Data files: CSV files

Ard: Arduino files, data of motor angle
- time: (in sec)
- ard: angle_1(rad), angle_2(rad), stair_command(each number from 0-4 related to a specific height of stairs)

Qua: Non-calibrated files of Foot and Top trajectory

### Processed Data files: json files

In json files, all top and foot data are calibirated as unit of millimeter.
