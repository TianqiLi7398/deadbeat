import experiment as ex
import time

exp_time = 10
mo = ex.mocap()
mo.startMeasurement()
time.sleep(exp_time)
mo.startReplay()

dat = mo.streamDataStore(exp_time)
time.sleep(exp_time)
mo.stopMeasurement()

un_dat = ex.unwrap_data(dat)

