import xarray as xr
import numpy as np
merge_data = np.zeros((275,3600,7200))
i = 0
for yr in range(2000,2023):
    for mon in range(1,13):
        try:
            if mon < 10:
                ds = xr.open_dataset("/mnt/d/cym/NCC/MODIS_NDVI_001/MODIS NDVI/" + str(yr) +"-"+ "0" + str(mon) + ".hdf",engine='netcdf4')['CMG 0.05 Deg Monthly NDVI']
                merge_data[i,::] = ds.values
                ds.close()
                i += 1
            else:
                ds = xr.open_dataset("/mnt/d/cym/NCC/MODIS_NDVI_001/MODIS NDVI/" + str(yr) +"-"+ str(mon) + ".hdf",engine='netcdf4')['CMG 0.05 Deg Monthly NDVI']
                merge_data[i,::] = ds.values
                ds.close()
                i += 1
        except:
            continue

# 创建一个空字典
nc_dict = {}
# 将time, lat, lon, var_masked添加到字典中
nc_dict['time'] = {'dims': ('time',), 'data': np.arange(np.datetime64('2000-02','M'),np.datetime64('2023-01','M'),np.timedelta64(1,'M'))}
nc_dict['lat'] = {'dims': ('lat',), 'data': np.linspace(90,-90,3600)}
nc_dict['lon'] = {'dims': ('lon',), 'data': np.linspace(-180,180,7200)}
nc_dict['NDVI_0.01'] = {'dims': ('time', 'lat', 'lon'), 'data': merge_data}
# 使用`from_dict`，将字典转化为xr.Dataset对象
data = xr.Dataset.from_dict(nc_dict)
data.to_netcdf("/mnt/d/cym/NCC/MODIS_NDVI_001/NDVI_001.nc")
