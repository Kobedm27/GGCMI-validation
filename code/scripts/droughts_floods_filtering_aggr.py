# # DROUGHTS & FLOODS FILTERING

import numpy as np
import xarray as xr
import pandas as pd 
from datetime import datetime, timedelta 
import pyreadr 

## 1. Get the data and join them

pr1 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1981_1990.nc", engine='netcdf4')
pr2 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1991_2000.nc", engine='netcdf4')
pr3 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_2001_2010.nc", engine='netcdf4')
pr4 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_2011_2019.nc", engine='netcdf4')

precip_days = xr.concat([pr1, pr2, pr3, pr4], dim='time')

# ## 2. Bring in crop data and growing season data 

# # Load crop data (from R)
cropdat_swh= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["swh_dat"] 
cropdat_wwh= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["wwh_dat"] 
cropdat_soy= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["soy_dat"] 
cropdat_ri2= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["ri2_dat"] 
cropdat_ri1= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["ri1_dat"] 
cropdat_mai= pyreadr.read_r("/p/projects/preview/Cluster_Testing/model_ready_data_othercrops.RData")["mai_dat"] 

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
    fill_value=0                 # Fill missing values with 0 (when the crop is not present in that grid cell)
)

# The pivot_table will result in multi-level columns (e.g., ('rain_area', 'swh')), so we flatten them
reshaped_data.columns = ['_'.join(col).strip() for col in reshaped_data.columns.values]

# Reset index to make 'lat' and 'lon' regular columns again
reshaped_data.reset_index(inplace=True)

# Drop duplicates to get unique grid cells
cropdat_unique = reshaped_data.drop_duplicates(subset=['lon', 'lat'])

# Crop names for reference
crop_names = ['mai', 'ri1', 'ri2', 'soy', 'swh', 'wwh']

# # Load growing seasons
season_firr_swh = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_swh_firr.nc") # Change crop accordingly
season_noirr_swh = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_swh_noirr.nc") # Change crop accordingly
season_firr_wwh = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_wwh_firr.nc") # Change crop accordingly
season_noirr_wwh = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_wwh_noirr.nc") # Change crop accordingly
season_firr_soy = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_soy_firr.nc") # Change crop accordingly
season_noirr_soy = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_soy_noirr.nc") # Change crop accordingly
season_firr_mai = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_mai_firr.nc") # Change crop accordingly
season_noirr_mai = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_mai_noirr.nc") # Change crop accordingly
season_firr_ri1 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_ri1_firr.nc") # Change crop accordingly
season_noirr_ri1 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_ri1_noirr.nc") # Change crop accordingly
season_firr_ri2 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_ri2_firr.nc") # Change crop accordingly
season_noirr_ri2 = xr.open_dataset("/p/projects/isimip/isimip/ISIMIP3a/InputData/socioeconomic/crop_calendar/2015soc/ggcmi-crop-calendar-phase3_2015soc_ri2_noirr.nc") # Change crop accordingly

season_firr_list = [season_firr_mai, season_firr_ri1, season_firr_ri2, season_firr_soy, season_firr_swh, season_firr_wwh]
season_noirr_list = [season_noirr_mai, season_noirr_ri1, season_noirr_ri2, season_noirr_soy, season_noirr_swh, season_noirr_wwh]

# Create dictionaries mapping crop names to season data
season_firr_dict = {crop: season for crop, season in zip(crop_names, season_firr_list)}
season_noirr_dict = {crop: season for crop, season in zip(crop_names, season_noirr_list)}


## 3. Define function to calulate longest consecutive wet/dry period ("drought or floods length")
def extreme_length(array):
    # INPUT:
    # - Array where we want to find maximum length of consecutive hot days
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

# The following function will calculate the climate indicators by carefully selecting the growing season days using ISIMIP´s crop calendars
# and regrouping them in "growing season years" which can span 2 calendar years in the Southern Hemisphere. For these growing season days, 
# a threshold climate value is calculated by the 95th/5th percentile. All days above/below this value are considered "wet"7"dry". We count the frequency of 
# hot days for each growing season year and location and we also compute the length of the longest consecutive period of wet/dry days for each 
# growing season year and location. 

def season_stat(climate, season_firr_dict, season_noirr_dict, cropdat):
      # INPUT: 
      # - climate: xarray dataset with climate variable
      # - season_firr: dictionary of full irrigation crop calendar xarray dataset
      # - season_noirr: dictionary of full rainfed crop calendar xarray dataset
      # - cropdat_unique: dataframe with locations where maize is grown and land use information in terms of irrigation or rainfed. Every row should be a unique location.
      # OUTPUT:
      # - drydays_freq: xarray data array with the frequency of very dry days for each location and growing season year
      # - raindays_freq: xarray data array with the frequency of very wet days for each location and growing season year
      # - tot_pr: xarray data array with the total precipitation throughout the growing season year for each location
      # - droughts: xarray data with the longest period of consecutive dry days for each location and growing season year
      # - floodss: xarray data with the longest period of consecutive wet days for each location and growing season year

     # Get coordinates from climate
      climate['time'] = pd.to_datetime(climate['time'].values)
      unique_years = np.unique(climate['time.year'].values)
      latitudes = np.unique(cropdat["lat"])
      longitudes = np.unique(cropdat["lon"])

      # Initialize empty xarray data arrays 
      raindays_freq = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      drydays_freq = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      wetdays_freq = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      tot_pr = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      floods = xr.DataArray(
       np.zeros((len(unique_years), len(latitudes), len(longitudes))),
       coords={"year": unique_years, "lat": latitudes, "lon": longitudes},
       dims=["year", "lat", "lon"]
        )
      
      droughts= xr.DataArray(
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
        # Assuming 'reshaped_data' is the DataFrame from earlier that contains lat, lon, and area information for all crops.

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
                pr_binary_current = (climate_current_growing["pr"]>= pr_p95).astype(int)
                # Threshold the selected days with the 5 percentile value (1 if precip is below threshold, otherwise 0)
                dr_binary_current = (climate_current_growing["pr"]<= dr_p05).astype(int)
		        # Threshold the selected days where it rains 
                wet_binary_current = (climate_current_growing["pr"]> 0).astype(int)
                # Count how many ones (wet and dry days) we have in this year for the current location
                raindays_current = pr_binary_current.sum(dim = "time")
                drydays_current = dr_binary_current.sum(dim = "time")
                wetdays_current = wet_binary_current.sum(dim = "time")

                # Add the data to the initialised xarray data arrays as frequency 
                raindays_freq.loc[current_year, lat, lon] = raindays_current/total_days
                drydays_freq.loc[current_year, lat, lon] = drydays_current/total_days
                wetdays_freq.loc[current_year, lat, lon] = wetdays_current/total_days

                
                # Total precipitation
                tot_pr.loc[current_year, lat, lon] = climate_current_growing["pr"].sum(dim = "time")

                # Apply the extreme_length function to get this statistic and add to data array 
                droughts.loc[current_year, lat, lon] = xr.apply_ufunc(
                    extreme_length,
                    dr_binary_current,
                    input_core_dims=[['time']],
                    vectorize=True,
                    dask='allowed',
                    output_dtypes=[int]
                )

                floods.loc[current_year, lat, lon] = xr.apply_ufunc(
                    extreme_length,
                    wet_binary_current,
                    input_core_dims=[['time']],
                    vectorize=True,
                    dask='allowed',
                    output_dtypes=[int]
                )
                
             
        # Handle growing seasons spanning two years
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

                if year == 2019: # Last year is also not a comple growing season
                    drydays_freq.loc[year, lat, lon] = 0
                    raindays_freq.loc[year, lat, lon] = 0
                    wetdays_freq.loc[year, lat, lon] = 0
                    droughts.loc[year, lat, lon] = 0
                    floods.loc[year, lat, lon] = 0
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
                    pr_binary_current = (climate_current_growing["pr"]>= pr_p95)
                    pr_binary_previous = (climate_previous_growing["pr"] >= pr_p95)
                    # Threshold the selected days with the 5 percentile value (1 if rainfall is below threshold, otherwise 0)
                    dr_binary_current = (climate_current_growing["pr"] <= dr_p05)
                    dr_binary_previous = (climate_previous_growing["pr"] <= dr_p05)
		            # Threshold the wet days
                    wet_binary_current = (climate_current_growing["pr"] > 0)
                    wet_binary_previous = (climate_previous_growing["pr"] > 0)
                    # Count how many ones (wet andd ry days) we have in this year for the current location
                    drydays_current = dr_binary_current.astype(int).sum(dim = "time")
                    drydays_previous = dr_binary_previous.astype(int).sum(dim = "time")
                    raindays_current = pr_binary_current.astype(int).sum(dim = "time")
                    raindays_previous = pr_binary_previous.astype(int).sum(dim = "time")
                    wetdays_current = wet_binary_current.astype(int).sum(dim = "time")
                    wetdays_previous = wet_binary_previous.astype(int).sum(dim = "time")
                    # Calculate frequency by combining both the dry and wet days from the end of previous year and beginning of next year within growing season. Add to xarray data array. 
                    drydays_freq.loc[current_year, lat, lon] = (drydays_current + drydays_previous)/total_days
                    raindays_freq.loc[current_year, lat, lon] = (raindays_current + raindays_previous)/total_days
                    wetdays_freq.loc[current_year, lat, lon] = (wetdays_current + wetdays_previous)/total_days

                    # Total precipitation
                    tot_pr.loc[current_year, lat, lon] = climate_current_growing["pr"].sum(dim = "time") + climate_previous_growing["pr"].sum(dim = "time") 

                    # Apply the extreme_length function to get this statistic and add to data array. 
                    droughts.loc[current_year, lat, lon] = xr.apply_ufunc(
                        extreme_length,
                        xr.concat([dr_binary_previous, dr_binary_current], dim='time'), # Combine previous and current growing season days
                        input_core_dims=[['time']],
                        vectorize=True,
                        dask='allowed',
                        output_dtypes=[int]
                    )

                    floods.loc[current_year, lat, lon] = xr.apply_ufunc(
                        extreme_length,
                        xr.concat([wet_binary_previous, wet_binary_current], dim='time'), # Combine previous and current growing season days
                        input_core_dims=[['time']],
                        vectorize=True,
                        dask='allowed',
                        output_dtypes=[int]
                    )

      return drydays_freq, raindays_freq, wetdays_freq, tot_pr, droughts, floods


## 4. Perform main function 
drydays_freq, raindays_freq, wetdays_freq, tot_pr, droughts, floods = season_stat(precip_days, season_firr_dict, season_noirr_dict, cropdat_unique)

## 5. Save new datasets as netcdf files
raindays_freq.to_netcdf("raindays_freq_aggr.nc")  # change name according to crop
drydays_freq.to_netcdf("drydays_freq_aggr.nc")  # change name according to crop
wetdays_freq.to_netcdf("wetdays_freq_aggr.nc") 
droughts.to_netcdf("droughts_aggr.nc")  # change name according to crop
floods.to_netcdf("floods_aggr.nc")  # change name according to crop
tot_pr.to_netcdf("tot_pr_aggr.nc")  # change name according to crop




# '# Convert dictionaries to xarray.DataArray
# latitudes = cropdat['lat'].unique()
# longitudes = cropdat['lon'].unique()
# years =  raindays_freq_dict[(latitudes[0], longitudes[0])].year.values

# raindays_freq = xr.DataArray(
#         np.zeros((len(years), len(latitudes), len(longitudes))),
#         coords=[years, latitudes, longitudes],
#         dims=["year", "lat", "lon"]
#     )

# drydays_freq = xr.DataArray(
#         np.zeros((len(years), len(latitudes), len(longitudes))),
#         coords=[years, latitudes, longitudes],
#         dims=["year", "lat", "lon"]
#     )

# tot_pr = xr.DataArray(
#         np.zeros((len(years), len(latitudes), len(longitudes))),
#         coords=[years, latitudes, longitudes],
#         dims=["year", "lat", "lon"]
#     )

#       # Fill the xarray.DataArray with the calculated values
# for (lat, lon), data in raindays_freq_dict.items():
#     raindays_freq.loc[:, lat, lon] = data.values

# for (lat, lon), data in drydays_freq_dict.items():
#     drydays_freq.loc[:, lat, lon] = data.values

# for (lat, lon), data in tot_pr_dict.items():
#     tot_pr.loc[:, lat, lon] = data.values



# mask.to_netcdf("mask_mai.nc")

# mask = xr.open_dataset("/p/projects/preview/Cluster_Testing/mask_mai.nc")["mask"]

# # The first and last growing season years of the locations with multiple year growing season are incomplete (first or second year of growing season part) so need to be either disregarded or carefully interpreted. 

# # Masking 
# precip_growing_days= precip_days.where(mask != 0, drop = True)

# # Add the mask as a coordinate for grouping
# precip_growing_days['growing_season_year'] = (('time', 'lat', 'lon'), mask.data)

# precip_growing_days = precip_growing_days.dropna(dim='time', how='all')

# precip_growing_days.to_netcdf("precip_growing_days_mai.nc") # change name according to crop


# ## 4. Threshold definition
# pr_p95 = precip_growing_days["pr"].quantile(0.95, dim = "time", skipna= True) # Heavy rainfall
# dr_p95 = precip_growing_days["pr"].quantile(0.05, dim = "time", skipna= True) # Heavy droughts 

# pr_p95.to_netcdf("pr_p95_mai.nc") # change name according to crop
# dr_p95.to_netcdf("dr_p95_mai.nc") # change name according to crop

# ## 5. Thresholding

# # Days beyond the threshold are marked as 1, other days as 0
# pr_binary = (precip_growing_days >= pr_p95).astype(int)
# dr_binary = (precip_growing_days <= dr_p95).astype(int)

#dr_binary['growing_season_year'] = (('time', 'lat', 'lon'), mask.data.astype("int"))
#pr_binary['growing_season_year'] = (('time', 'lat', 'lon'), mask.data.astype("int"))

# pr_binary.to_netcdf("pr_binary_mai.nc") # change name according to crop
# dr_binary.to_netcdf("dr_binary_mai.nc") # change name according to crop

## 6. Count of extreme rainfall days per year

# Sum all the ones 
# Fill nas with zeros to avoid memory problem
#dr_binary = dr_binary.fillna(0)

# dr_binary= xr.open_dataset("/p/projects/preview/Cluster_Testing/dr_binary_mai.nc")

# Check if there are any NaNs in growing_season_year
#unique_years = dr_binary['growing_season_year'].values
#print("Unique values in growing_season_year:", set(unique_years.flatten()))


# Exclude days not part of any growing season year (growing_season_year == 0) and years 1981 and 2020
#valid_season_mask = (dr_binary['growing_season_year'] != 0) & \
                    #(dr_binary['growing_season_year'] != 1981) & \
                    #(dr_binary['growing_season_year'] != 2020)

# Apply the mask to filter out the invalid days
#filtered_ds = dr_binary.where(valid_season_mask, drop=True)

#dr_binary["time.year"] = mask.data.astype("int") 
#filtered_ds["time.year"] = filtered_ds["growing_season_year"] 

# dr_binary = dr_binary.set_coords('growing_season_year')

#Create a new coordinate for the growing season year
#filtered_ds.to_netcdf("filtered.nc")

#df = dr_binary.to_dataframe().reset_index()

#print(df)

#df.to_csv('output.csv', index=False)
# Group by growing_season_year and lat, lon, then sum the pr values
#grouped = df.groupby(['growing_season_year', 'lat', 'lon'])['pr'].sum().reset_index()

# Convert back to xarray
#drydays = grouped.set_index(['growing_season_year', 'lat', 'lon']).to_xarray()

# Group by growing_season_year and calculate the total precipitation for each growing season year
#drydays = filtered_ds["pr"].groupby("growing_season_year").sum(dim = "time")
#drydays.to_netcdf("drydays_mai.nc") 

#filtered_ds = xr.open_dataset("C:/Users/kobede/Documents/PREVIEW/ISIMIP3a validation/Scripts/Data processing/filtered.nc")
#df = pd.read_csv("C:/Users/kobede/Documents/PREVIEW/ISIMIP3a validation/Scripts/Data processing/output.csv")
#drydays = xr.open_dataset("C:/Users/kobede/Documents/PREVIEW/ISIMIP3a validation/Scripts/Data processing/drydays_mai.nc")
#drydays
#drydays.sel(lat = 45.25, lon = 1.75)["pr"].values

#drydays = filtered_ds["pr"].groupby("time.year").sum(dim = "time")

#drydays

# Fill nas with zeros to avoid memory problem
#precip_growing_days= precip_growing_days.fillna(0)
# Calculate the total number of days in each growing season year
#total_days = precip_growing_days.groupby('growing_season_year').count(dim = "time")

# Divide the count by total days in the growing season
#raindays_freq = raindays / total_days
# drydays_freq = drydays / total_days

# raindays_freq.to_netcdf("raindays_freq_mai.nc")  # change name according to crop
# drydays_freq.to_netcdf("drydays_freq_mai.nc")  # change name according to crop

# # We also compute the total precipitation

# tot_pr = precip_growing_days.groupby('growing_season_year').sum(dim='time')
# tot_pr.to_netcdf("tot_pr_mai.nc")  # change name according to crop

# ## 7. Length of extremes
# # We use the following function 

# # Apply the function along the time dimension after grouping by year
# #floods = pr_binary.groupby('growing_season_year').apply(
#     #lambda x: xr.apply_ufunc(
#        # extreme_length, 
#         #x,
#         #input_core_dims=[['time']],
#         #vectorize=True,
#         #dask='allowed',
#         #output_dtypes=[int]
#     #)
# #)

# droughts = dr_binary.groupby('growing_season_year').apply(
#     lambda x: xr.apply_ufunc(
#         extreme_length, 
#         x,
#         input_core_dims=[['time']],
#         vectorize=True,
#         dask='allowed',
#         output_dtypes=[int]
#     )
# )

# #floods.to_netcdf("floods_mai.nc") # change name according to crop
# droughts.to_netcdf("droughts_mai.nc") # change name according to crop