## COMPUTATION OF DRY AND WET EXTREME CLIMATE INDICATORS

# This script processes daily precipitation data from the GSWP3-W5E5 dataset to compute 
# annual indicators of wet and dry climate extremes.

# Indicators are calculated:
# - Per calendar year
# - At each grid cell where crops are grown
# - Only using the subset of days within the year when at least one of the five main crops 
#   (maize, soy, spring wheat, winter wheat, or rice) is typically grown at that location

# The growing season periods are derived from crop- and land-use-specific calendars.

# Note: Indicators are not computed per crop. Instead, for each grid cell and year, 
# we consider the union of growing season days across all crops present. These data 
# are further used for the crop aggregated analysis (see code/notebooks/main.qmd) presented in the main paper.

# Output: gridded climate extreme indicators saved to 
# GGCMI-validation/data/processed/extremes_indicators/extremes_indicators/crop_aggregated/

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

## 2. Bring in and process crop data and growing season data 

## 2.1 crop data 

# load crop data (earlier processed in R as RData)
cropdat_swh= pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")["dat_swh"] 
cropdat_wwh= pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")["dat_wwh"] 
cropdat_soy= pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")["dat_soy"] 
cropdat_ri2= pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")["dat_ri1"] 
cropdat_ri1= pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")["dat_ri2"] 
cropdat_mai= pyreadr.read_r(repo_path / "GGCMI-validation/data/processed/crop_specific_data.RData")["dat_mai"] 

# Add a column to each DataFrame indicating the crop name
cropdat_swh['crop'] = 'swh'
cropdat_wwh['crop'] = 'wwh'
cropdat_soy['crop'] = 'soy'
cropdat_ri2['crop'] = 'ri2'
cropdat_ri1['crop'] = 'ri1'
cropdat_mai['crop'] = 'mai'

# Concatenate all dataframes into one, keeping the crop column
cropdat_all = pd.concat([cropdat_swh, cropdat_wwh, cropdat_soy, cropdat_ri2, cropdat_ri1, cropdat_mai])

# Pivot the data to get one row per lat-lon, and separate columns for each crop's rain and irr areas
# We use pivot_table to reshape the data based on lat, lon, and crop

reshaped_data = cropdat_all.pivot_table(
    index=['lat', 'lon'],        # Index by lat-lon pairs
    columns='crop',              # Create separate columns for each crop
    values=['rain_area', 'irr_area'],  # Values for the rain and irr areas
    fill_value=0                 # Fill missing values with 0 (when the crop is not present in that gridcell)
)

# The pivot_table will result in multi-level columns (e.g., ('rain_area', 'swh')), so we flatten them
reshaped_data.columns = ['_'.join(col).strip() for col in reshaped_data.columns.values]

# Reset index to make 'lat' and 'lon' regular columns again
reshaped_data.reset_index(inplace=True)

# Drop duplicates to get unique grid cells
cropdat_unique = reshaped_data.drop_duplicates(subset=['lon', 'lat'])

# Crop names for reference
crop_names = ['mai', 'ri1', 'ri2', 'soy', 'swh', 'wwh']

## 2.2 Growing season data

# Load growing seasons
season_firr_swh = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_swh_firr.nc") 
season_noirr_swh = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_swh_noirr.nc")
season_firr_wwh = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_wwh_firr.nc") 
season_noirr_wwh = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_wwh_noirr.nc") 
season_firr_soy = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_soy_firr.nc") 
season_noirr_soy = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_soy_noirr.nc") 
season_firr_mai = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_mai_firr.nc") 
season_noirr_mai = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_mai_noirr.nc")
season_firr_ri1 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_ri1_firr.nc") 
season_noirr_ri1 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_ri1_noirr.nc") 
season_firr_ri2 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_ri2_firr.nc") 
season_noirr_ri2 = xr.open_dataset(repo_path / "GGCMI-validation/data/raw/other/ggcmi-crop-calendar-phase3_2015soc_ri2_noirr.nc") 

season_firr_list = [season_firr_mai, season_firr_ri1, season_firr_ri2, season_firr_soy, season_firr_swh, season_firr_wwh]
season_noirr_list = [season_noirr_mai, season_noirr_ri1, season_noirr_ri2, season_noirr_soy, season_noirr_swh, season_noirr_wwh]

# Create dictionaries mapping crop names to season data
season_firr_dict = {crop: season for crop, season in zip(crop_names, season_firr_list)}
season_noirr_dict = {crop: season for crop, season in zip(crop_names, season_noirr_list)}

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
      # - cropdat: dataframe with locations where crops are grown and land use information in terms of irrigation or rainfed. Every row should be a unique location.
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
    
    # Iterate over rows of cropdata: different locations (gridcells) and crops
      for index, row in cropdat.iterrows():
        lat = row['lat']
        lon = row['lon']

        # Initialize variables to hold the min and max growing season days across all crops
        start_day_loc = np.inf
        end_day_loc = -np.inf
        start_day_crop = np.inf
        end_day_crop = -np.inf

        # Determine land use and select appropriate calendar dates:
        # Integrate firr and noirr in three cases using the landuse data: if only rainfed, we pick the noirr, if only irr, we pick the firr growing season 
        # and if it is a combination of the two we extend the growing season such that it covers both irr and firr (so all days where either irr or firr crops are grown)

    # Iterate over each crop's growing season
        for crop in crop_names:
            
            # Columns for rain_area and irr_area for the current crop
            rain_area = row[f"rain_area_{crop}"]
            irr_area = row[f"irr_area_{crop}"]
    
            # If no crop area is present, skip this crop
            if rain_area == 0 and irr_area == 0:
                continue
        
            # Get the firr and no-irr growing season for the crop
            season_firr = season_firr_dict[crop]
            season_noirr = season_noirr_dict[crop]

            # Extract the start and end days of the growing seasons
            start_day_firr = season_firr['planting_day']
            end_day_firr = season_firr['maturity_day']
            start_day_noirr = season_noirr['planting_day']
            end_day_noirr = season_noirr['maturity_day']
        
            # Get the start and end days based on rain/irr area
            if rain_area > 0 and irr_area == 0:  # Only rainfed
                start_day_loc = start_day_noirr.sel(lat=lat, lon=lon).values
                end_day_loc = end_day_noirr.sel(lat=lat, lon=lon).values
            
            elif irr_area > 0 and rain_area == 0:  # Only irrigated
                start_day_loc = start_day_firr.sel(lat=lat, lon=lon).values
                end_day_loc = end_day_firr.sel(lat=lat, lon=lon).values

            elif rain_area > 0 and irr_area > 0:  # Both rainfed and irrigated
                # Get growing season for both rainfed and irrigated, then extend
                rainfed_start = start_day_firr.sel(lat=lat, lon=lon).values
                rainfed_end = end_day_firr.sel(lat=lat, lon=lon).values
                irrigated_start = start_day_noirr.sel(lat=lat, lon=lon).values
                irrigated_end = end_day_noirr.sel(lat=lat, lon=lon).values

                # Extend the growing season to include both rainfed and irrigated periods
                start_day_crop = min(rainfed_start, irrigated_start)
                end_day_crop = max(rainfed_end, irrigated_end)

            # Update the overall growing season days across crops
            start_day_loc = min(start_day_loc, start_day_crop)
            end_day_loc = max(end_day_loc, end_day_crop)

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
FDD.to_netcdf(repo_path / "GGCMI-validation/data/processed/extremes_indicators/crop_aggregated/FDD_aggr.nc")  
FWD.to_netcdf(repo_path / "GGCMI-validation/data/processed/extremes_indicators/crop_aggregated/FWD_aggr.nc") 
LDS.to_netcdf(repo_path / "GGCMI-validation/data/processed/extremes_indicators/crop_aggregated/LDS_aggr.nc") 
LWS.to_netcdf(repo_path / "GGCMI-validation/data/processed/extremes_indicators/crop_aggregated/LWS_aggr.nc")  
TPR.to_netcdf(repo_path / "GGCMI-validation/data/processed/extremes_indicators/crop_aggregated/TPR_aggr.nc") 
