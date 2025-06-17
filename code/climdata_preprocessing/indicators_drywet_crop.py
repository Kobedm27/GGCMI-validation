## COMPUTATION OF DRY AND WET EXTREME CLIMATE INDICATORS

# Define crop name here
crop = "mai"  # options: mai, soy, ri1, ri2, swh, wwh

# This script processes daily precipitation data from the GSWP3-W5E5 dataset to compute 
# annual indicators of wet and dry climate extremes.

# Indicators are calculated:
# - Per calendar year
# - At each grid cell where crops are grown
# - Only using the subset of days within the year when the corresponding crop is grown

# The growing season periods are derived from crop- and land-use-specific calendars.

# These data are further used for the crop specific analysis
# (see code/notebooks/main.qmd) presented in the appendix.

# Output: gridded climate extreme indicators saved to 
# GGCMI-validation/data/processed/extremes_indicators/extremes_indicators/crop_specific/

import numpy as np
import xarray as xr
import pandas as pd 
from datetime import datetime, timedelta 
import pyreadr 

# User-defined base path to the repository
repo_path = Path("") #change accordingly!

## 1. Get the precipitation data and join them

pr1 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/climdata/gswp3-w5e5_obsclim_pr_global_daily_1981_1990.nc", engine='netcdf4')
pr2 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/climdata/gswp3-w5e5_obsclim_pr_global_daily_1991_2000.nc", engine='netcdf4')
pr3 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/climdata/gswp3-w5e5_obsclim_pr_global_daily_2001_2010.nc", engine='netcdf4')
pr4 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/climdata/gswp3-w5e5_obsclim_pr_global_daily_2011_2019.nc", engine='netcdf4')

precip_days = xr.concat([pr1, pr2, pr3, pr4], dim='time')

## 2. Bring in crop data and growing season data 

# Load crop data (earlier processed in R as RData)
cropdat = pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")[f"dat_{crop}"]
cropdat_unique = cropdat.drop_duplicates(subset = ["lon", "lat"])

# Load growing seasons
season_firr = xr.open_dataset(repo_path / f"GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_{crop}_firr.nc")
season_noirr = xr.open_dataset(repo_path / f"GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_{crop}_noirr.nc")

## 3. Define function to calculate longest consecutive wet/dry period 
def extreme_length(array):
    # INPUT:
    # - Array where we want to find maximum length of consecutive dry/wet days
    # OUTPUT:
    # - Maximum length of dry or wet days 

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

# The following function will calculate the climate extreme indicators by carefully selecting the growing season days using ISIMIP´s crop calendars
# and regrouping them in "growing season years" which can span 2 calendar years in the Southern Hemisphere. For these growing season days, 
# a threshold climate value is calculated by the 95th/5th percentile. All days above/below this value are considered extremely "wet"/"dry". We count the frequency of 
# wet/days days for each growing season year and location and we also compute the length of the longest consecutive period of wet/dry days for each 
# growing season year and location. 

def season_stat(climate, season_firr_dict, season_noirr_dict, cropdat):
      # INPUT: 
      # - climate: xarray dataset with climate variable
      # - season_firr: dictionary of full irrigation crop calendar xarray dataset
      # - season_noirr: dictionary of full rainfed crop calendar xarray dataset
      # - cropdat: dataframe with locations where <crop> is grown and land use information in terms of irrigation or rainfed. Every row should be a unique location.
      # OUTPUT:
      # - FDD: xarray data array with the Frequency of extreme Dry Days for each location and growing season year
      # - FWD: xarray data array with the Frequency of extreme Wet Days for each location and growing season year
      # - TPR: xarray data array with the Total Precipitation throughout the growing season year for each location
      # - LDS: xarray data with the longest period of consecutive dry days (Longest Dry Spell) for each location and growing season year
      # - LWS: xarray data with the longest period of consecutive wet days (Longest Wet Spell) for each location and growing season year

     # Get coordinates from climate
      climate['time'] = pd.to_datetime(climate['time'].values)
      unique_years = np.unique(climate['time.year'].values)
      latitudes = np.unique(cropdat["lat"])
      longitudes = np.unique(cropdat["lon"])
      
      FDD = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      FWD = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      TPR = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      LWS = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      LDS= xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
    
    # Iterate over rows of cropdata: different locations (gridcells) where <crop> is grown
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
            # Calculate 95th percentile across all growing season days as threshold for wet
            pr_p95 = climate_loc_growing["pr"].quantile(0.95, dim = "time", skipna= True)
            # Calculate 5th percentile across all growing season days as threshold for dry
            dr_p05 = climate_loc_growing["pr"].quantile(0.05, dim = "time", skipna= True)

            # Loop over each year 
            for year in unique_years:
                current_year = year
                # Select data for current year
                climate_current = climate_loc.sel(time = climate_loc["time.year"]  == current_year) 
                dayofyear_current = climate_current["time"].dt.dayofyear
                # Select only the days within the growing season
                climate_current_growing = climate_current.sel(time = (dayofyear_current >= start_day_loc) & (dayofyear_current <= end_day_loc))
                total_days = end_day_loc - start_day_loc + 1  # +1 to include both start and end days
                # Threshold the selected days with the 95 percentile value (1 if precip is above threshold, otherwise 0)
                wet_binary_current = (climate_current_growing["pr"]>= pr_p95).astype(int)
                # Threshold the selected days with the 5 percentile value (1 if precip is below threshold, otherwise 0)
                dr_binary_current = (climate_current_growing["pr"]<= dr_p05).astype(int)
                # Count how many ones (wet and dry days) we have in this year for the current location
                drydays_current = dr_binary_current.sum(dim = "time")
                wetdays_current = wet_binary_current.sum(dim = "time")

                # Add the data to the initialised xarray data arrays as frequency 
                FDD.loc[current_year, lat, lon] = drydays_current/total_days # Frequency of extreme Dry Days
                FWD.loc[current_year, lat, lon] = wetdays_current/total_days #Frequency of extreme Wet Days

                
                # Total precipitation
                TPR.loc[current_year, lat, lon] = climate_current_growing["pr"].sum(dim = "time")

                # Apply the extreme_length function to get this statistic and add to data array 
		    # Longest Dry Spell
                LDS.loc[current_year, lat, lon] = xr.apply_ufunc(
                    extreme_length,
                    dr_binary_current,
                    input_core_dims=[['time']],
                    vectorize=True,
                    dask='allowed',
                    output_dtypes=[int]
                )
		    # Longest Wet Spell

                LWS.loc[current_year, lat, lon] = xr.apply_ufunc( 
                    extreme_length,
                    wet_binary_current,
                    input_core_dims=[['time']],
                    vectorize=True,
                    dask='allowed',
                    output_dtypes=[int]
                )
                
             
        # Handle growing seasons spanning two calendar years
        if end_day_loc < start_day_loc: 
           # Masking of the growing season to get all growing season days (ones for days within growing season, zeros outside)
            climate_loc_growing = climate_loc.where((dayofyear >= start_day_loc) | (dayofyear <= end_day_loc), drop=True) # OR (|) statement instead of AND (&)
            # Calculate 95 percentile across all growing season days as threshold for wet
            pr_p95 = climate_loc_growing["pr"].quantile(0.95, dim = "time", skipna= True) 
            # Calculate 5th percentile across all growing season days as threshold for dry
            dr_p05 = climate_loc_growing["pr"].quantile(0.05, dim = "time", skipna= True) 

            # Loop over each year 
            for year in unique_years:
                # Only from the second year in the data we have a complete growing season. That´s why we calculate always for the year + 1
                current_year = year +1

                if year == 2019: # Last year is also not a complete growing season
                    FDD.loc[year, lat, lon] = 0
                    FWD.loc[year, lat, lon] = 0
                    LDS.loc[year, lat, lon] = 0
                    LWS.loc[year, lat, lon] = 0
		    TPR.loc[year, lat, lon] = 0
                else: 
                    # Get current climate data 
                    climate_current = climate_loc.sel(time = climate_loc["time.year"]  == current_year)  
                    # Get climate data from previous year
                    climate_previous = climate_loc.sel(time = climate_loc["time.year"]  == year) 
                    dayofyear_current = climate_current["time"].dt.dayofyear
                    dayofyear_previous = climate_previous["time"].dt.dayofyear
                    total_days = (365 - start_day_loc +1) + end_day_loc # +1 to include the start day
                    # growing season consists of end of pevious year and beginning of current year: keep two split in previous and current growing season days
                    climate_current_growing = climate_current.sel(time = dayofyear_current <= end_day_loc)
                    climate_previous_growing = climate_previous.sel(time = dayofyear_previous >= start_day_loc)
                    # Threshold the selected days with the 95 percentile value (1 if rainfall is above threshold, otherwise 0)
                    wet_binary_current = (climate_current_growing["pr"]>= pr_p95)
                    wet_binary_previous = (climate_previous_growing["pr"] >= pr_p95)
                    # Threshold the selected days with the 5 percentile value (1 if rainfall is below threshold, otherwise 0)
                    dr_binary_current = (climate_current_growing["pr"] <= dr_p05)
                    dr_binary_previous = (climate_previous_growing["pr"] <= dr_p05)
                    # Count how many ones (wet and dry days) we have in this year for the current location
                    drydays_current = dr_binary_current.astype(int).sum(dim = "time")
                    drydays_previous = dr_binary_previous.astype(int).sum(dim = "time")
                    wetdays_current = wet_binary_current.astype(int).sum(dim = "time")
                    wetdays_previous = wet_binary_previous.astype(int).sum(dim = "time")
                    # Calculate frequency by combining both the dry and wet days from the end of previous year and beginning of next year within growing season. Add to xarray data array. 
                    FDD.loc[current_year, lat, lon] = (drydays_current + drydays_previous)/total_days # Frequency of extreme Dry Days
                    FWD.loc[current_year, lat, lon] = (wetdays_current + wetdays_previous)/total_days # Frequency of extreme Wet Days

                    # Total precipitation
                    TPR.loc[current_year, lat, lon] = climate_current_growing["pr"].sum(dim = "time") + climate_previous_growing["pr"].sum(dim = "time") 

                    # Apply the extreme_length function to get this statistic and add to data array. 
			# Longest Dry Spell
                    LDS.loc[current_year, lat, lon] = xr.apply_ufunc(
                        extreme_length,
                        xr.concat([dr_binary_previous, dr_binary_current], dim='time'), # Combine previous and current growing season days
                        input_core_dims=[['time']],
                        vectorize=True,
                        dask='allowed',
                        output_dtypes=[int]
                    )
			# Longest Wet Spell
                    LWS.loc[current_year, lat, lon] = xr.apply_ufunc(
                        extreme_length,
                        xr.concat([wet_binary_previous, wet_binary_current], dim='time'), # Combine previous and current growing season days
                        input_core_dims=[['time']],
                        vectorize=True,
                        dask='allowed',
                        output_dtypes=[int]
                    )

      return FDD, FWD, TPR, LDS, LWS


## 5. Perform main function 
FDD, FWD, TPR, LDS, LWS = season_stat(precip_days, season_firr_dict, season_noirr_dict, cropdat_unique)

## 6. Save new datasets as netcdf files
FDD.to_netcdf(repo_path / f"GGCMI-validation/data/processed/extremes_indicators/crop_specific/FDD_{crop}.nc")  
FWD.to_netcdf(repo_path / f"GGCMI-validation/data/processed/extremes_indicators/crop_specific/FWD_{crop}.nc") 
LDS.to_netcdf(repo_path / f"GGCMI-validation/data/processed/extremes_indicators/crop_specific/LDS_{crop}.nc") 
LWS.to_netcdf(repo_path / f"GGCMI-validation/data/processed/extremes_indicators/crop_specific/LWS_{crop}.nc")  
TPR.to_netcdf(repo_path / f"GGCMI-validation/data/processed/extremes_indicators/crop_specific/TPR_{crop}.nc") 
