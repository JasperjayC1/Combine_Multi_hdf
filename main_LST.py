import xarray as xr
import os
import glob
import numpy as np
from datetime import datetime,timedelta
file_pattern = "/mnt/d/cym/NCC/MODIS_LST_11C3.061/MOD11C3.A*.hdf"
file_list = glob.glob(file_pattern)
LST_Day_CMG = np.zeros((283,3600,7200))
LST_Night_CMG = np.zeros((283,3600,7200))
i = 0
for file_name in file_list:
    ds = xr.open_dataset(file_name,engine='netcdf4')['LST_Day_CMG']
    LST_Day_CMG[i,::] = ds.values
    ds.close()
    ds2 = xr.open_dataset(file_name,engine='netcdf4')['LST_Night_CMG']
    LST_Night_CMG[i,::] = ds2.values
    ds2.close()
    i += 1
  
# 创建一个空字典
nc_dict = {}
# 将time, lat, lon, var_masked添加到字典中
nc_dict['time'] = {'dims': ('time',), 'data': np.arange(np.datetime64('2000-02','M'),np.datetime64('2023-09','M'),np.timedelta64(1,'M'))}
nc_dict['lat'] = {'dims': ('lat',), 'data': np.linspace(90,-90,3600)}
nc_dict['lon'] = {'dims': ('lon',), 'data': np.linspace(-180,180,7200)}
nc_dict['LST_Day_CMG'] = {'dims': ('time', 'lat', 'lon'), 'data': LST_Day_CMG}
nc_dict['LST_Night_CMG'] = {'dims': ('time', 'lat', 'lon'), 'data': LST_Night_CMG}

# 使用`from_dict`，将字典转化为xr.Dataset对象
data = xr.Dataset.from_dict(nc_dict)
data.to_netcdf("/mnt/d/cym/NCC/MODIS_LST_11C3.061/LST.nc")
