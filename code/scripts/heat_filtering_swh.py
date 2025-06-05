# HEAT FILTERING    

import numpy as np
import xarray as xr
import pandas as pd 
from datetime import datetime, timedelta 
import pyreadr 

## 1. Get the data and join them

temp1 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_tasmax_global_daily_1981_1990.nc", engine='netcdf4')
temp2 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_tasmax_global_daily_1991_2000.nc", engine='netcdf4')
temp3 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_tasmax_global_daily_2001_2010.nc", engine='netcdf4')
temp4 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_tasmax_global_daily_2011_2019.nc", engine='netcdf4')

temp_days = xr.concat([temp1, temp2, temp3, temp4], dim='time')

## 2. Bring in crop data and growing season data 

# Load crop data (from R)
cropdat= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["swh_dat"] # crop can be changed here
cropdat_unique = cropdat.drop_duplicates(subset = ["lon", "lat"])

# Load growing seasons
season_firr = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_swh_firr.nc") # Change crop accordingly
season_noirr = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_swh_noirr.nc") # Change crop accordingly

## 3. Define function to calulate longest hot period ("heatwave length")
def heatwaves_length(array):
    # INPUT:
    # - Array where we want to find maximum length of consecutive hot days
    # OUTPUT:
    # - Maximum length of heatwaves

    max_length = 0
    current_length = 0
    for value in array:
        if value == 1:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 0
    return max_length


## 4. Calculate growing season statistics

# The following function will:


def season_stat(climate, season_firr, season_noirr, cropdat):
      # INPUT: 
      # - climate: xarray.Dataset with climate variable
      # - season_firr: full irrigation crop calendar xarray
      # - season_noirr: full rainfed crop calendar xarray
      # - cropdat_uniaue: dataframe with locations where maize is grown and land use information in terms of irrigation or rainfed. Every row should be a unique location.
      # OUTPUT:
      # - hotdays_freq:
      # - heatwaves:

     # Extract the start and end days of the growing seasons
      start_day_firr = season_firr['planting_day']
      end_day_firr= season_firr['maturity_day']
      start_day_noirr = season_noirr['planting_day']
      end_day_noirr= season_noirr['maturity_day']

     # Get coordinates from climate
      climate['time'] = pd.to_datetime(climate['time'].values)
      unique_years = np.unique(climate['time.year'].values)
      latitudes = np.unique(cropdat["lat"])
      longitudes = np.unique(cropdat["lon"])

      # Initialize empty xarray data arrays 
      hotdays_freq = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      heatwaves = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
    
    # Iterate over rows of cropdata: different locations (gridcells) where maize is grown
      for index, row in cropdat.iterrows():
        lat = row['lat']
        lon = row['lon']

        # Determine land use and select appropriate calendar dates:
        # Integrate firr and noirr in three cases using the landuse data: if only rainfed, we pick the noirr, if only irr, we pick the firr growing season 
        # and if it is a combination of the two we extend the growing season such that it covers both irr and firr (so all days where either irr or firr crops are grown)
        if row['rain_area'] > 0 and row['irr_area'] == 0:
            start_day_loc = start_day_noirr.sel(lat=lat, lon=lon).values
            end_day_loc = end_day_noirr.sel(lat=lat, lon=lon).values
        elif row['irr_area'] > 0 and row['rain_area'] == 0:
            start_day_loc = start_day_firr.sel(lat=lat, lon=lon).values
            end_day_loc = end_day_firr.sel(lat=lat, lon=lon).values
        elif row['rain_area'] > 0 and row['irr_area'] > 0:
            rainfed_start = start_day_firr.sel(lat=lat, lon=lon).values
            rainfed_end = end_day_firr.sel(lat=lat, lon=lon).values
            irrigated_start = start_day_noirr.sel(lat=lat, lon=lon).values
            irrigated_end = end_day_noirr.sel(lat=lat, lon=lon).values

                  # Extend growing season to include both irrigated and rainfed dates
            start_day_loc = min(rainfed_start, irrigated_start)
            end_day_loc = max(rainfed_end, irrigated_end)

        # Get climate data and day of years array for current gridcell 
        climate_loc = climate.sel(lat=lat, lon=lon)
        climate_loc['time'] = pd.to_datetime(climate_loc['time'].values)
        dayofyear = climate_loc["time"].dt.dayofyear

        # Handle growing seasons within the same year
        if start_day_loc <= end_day_loc:
            # Masking of the growing season to get all growing season days (ones for days within growing season, zeros outside)
            climate_loc_growing = climate_loc.where((dayofyear >= start_day_loc) & (dayofyear <= end_day_loc), drop=True)
            # Calculate 95 percentile across all growing season days as threshold
            temp_p95 = climate_loc_growing["tasmax"].quantile(0.95, dim = "time", skipna= True)

            # Loop over each year 
            for year in unique_years:
                current_year = year
                # Select data for current year
                climate_current = climate_loc.sel(time = climate_loc["time.year"]  == current_year) 
                dayofyear_current = climate_current["time"].dt.dayofyear
                # Select only the days within the growing season
                climate_current_growing = climate_current.sel(time = (dayofyear_current >= start_day_loc) & (dayofyear_current <= end_day_loc))
                total_days = end_day_loc - start_day_loc + 1  # +1 to include both start and end days
                # Threshold the selected days with the 95 percentile value (1 if temperature is above threshold, otherwise 0)
                temp_binary_current = (climate_current_growing["tasmax"]>= temp_p95).astype(int)
                # Count how many ones (hot days) we have in this year for the current location
                hotdays_current = temp_binary_current.sum(dim = "time")
                # Add the data to the initialised xarray data array
                hotdays_freq.loc[current_year, lat, lon] = hotdays_current/total_days

                # Apply the heatwaves_length function to get this statistic and add to data array 
                heatwaves.loc[current_year, lat, lon] = xr.apply_ufunc(
                    heatwaves_length,
                    temp_binary_current,
                    input_core_dims=[['time']],
                    vectorize=True,
                    dask='allowed',
                    output_dtypes=[int]
                )
                
             
        # Handle growing seasons spanning two years
        if end_day_loc < start_day_loc: 
           # Masking of the growing season to get all growing season days (ones for days within growing season, zeros outside)
            climate_loc_growing = climate_loc.where((dayofyear >= start_day_loc) | (dayofyear <= end_day_loc), drop=True) # OR (|) statement instead of AND (&)
            # Calculate 95 percentile across all growing season days as threshold
            temp_p95 = climate_loc_growing["tasmax"].quantile(0.95, dim = "time", skipna= True) # Heavy rainfall

            for year in unique_years:
                current_year = year +1
                if year == 2019: # Last year is not a comple growing season
                    hotdays_freq.loc[year, lat, lon] = 0
                    heatwaves.loc[year, lat, lon] = 0
                else: 
                    climate_current = climate_loc.sel(time = climate_loc["time.year"]  == current_year)  # We discard the first year because incomplete growing season
                    climate_previous = climate_loc.sel(time = climate_loc["time.year"]  == year) 
                    dayofyear_current = climate_current["time"].dt.dayofyear
                    dayofyear_previous = climate_previous["time"].dt.dayofyear
                    total_days = (365 - start_day_loc +1) + end_day_loc # +1 to include the start day
                    # Current growing season consists of end of pevious year and beginning of current year
                    # Filter
                    climate_current_growing = climate_current.sel(time = dayofyear_current <= end_day_loc)
                    climate_previous_growing = climate_previous.sel(time = dayofyear_previous >= start_day_loc)

                    temp_binary_current = (climate_current_growing["tasmax"]>= temp_p95)
                    temp_binary_previous = (climate_previous_growing["tasmax"] >= temp_p95)
                    hotdays_current = temp_binary_current.astype(int).sum(dim = "time")
                    hotdays_previous = temp_binary_previous.astype(int).sum(dim = "time")
                    hotdays_freq.loc[current_year, lat, lon] = (hotdays_current + hotdays_previous)/total_days

                    # Apply the heatwaves_length function
                    heatwaves.loc[current_year, lat, lon] = xr.apply_ufunc(
                        heatwaves_length,
                        xr.concat([temp_binary_previous, temp_binary_current], dim='time'),
                        input_core_dims=[['time']],
                        vectorize=True,
                        dask='allowed',
                        output_dtypes=[int]
                    )

      return hotdays_freq, heatwaves


## 4. Perform main function 
hotdays_freq, heatwaves = season_stat(temp_days, season_firr, season_noirr, cropdat_unique)

## 5. Save new datasets as netcdf files
hotdays_freq.to_netcdf("hotdays_freq_swh.nc")  # change name according to crop
heatwaves.to_netcdf("heatwaves_swh.nc")  # change name according to crop