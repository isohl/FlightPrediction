import requests
import pygrib
import datetime
import time
import ftplib
import os
from collections import defaultdict
import numpy as np
import math
import logging

logger = logging.getLogger("FlightPrediction")

# Constant for Earths radius
EARTH_RADIUS_MILES = 3960.0

def change_in_latitude_miles(miles):
    return math.degrees(miles / EARTH_RADIUS_MILES)

def change_in_longitude_miles(latitude, miles):
    return math.degrees(miles / (EARTH_RADIUS_MILES * math.cos(math.radians(latitude))))


class WindModel(object):
    def __init__(self, center=None, radius=None, forecast_date=None, gfs_data_file=None, hrrr_data_file=None, keep_files=False):
        """
        Construct a wind model centered at a given Latitude/Longitude with a radius defined in miles
        :param center:
        :param radius:
        :param forecast_date:
        """
        if gfs_data_file is None and hrrr_data_file is None and (center is None or radius is None or forecast_date is None):
            raise Exception("Invalid center or radius for wind model")

        self.forecast_date = forecast_date
        self.gfs_data_file = gfs_data_file
        self.gfs_height_map = None
        self.gfs_latlons = None
        self.hrrr_data_file = hrrr_data_file
        self.hrrr_height_map = None
        self.hrrr_latlons = None

        if gfs_data_file is not None:
            self.gfs_height_map, self.gfs_latlons = self._parse_grbs(pygrib.open(gfs_data_file))
        if hrrr_data_file is not None:
            self.hrrr_height_map, self.hrrr_latlons = self._parse_grbs(pygrib.open(hrrr_data_file))

        if gfs_data_file is None and hrrr_data_file is None:
            lat_radius = change_in_latitude_miles(radius)
            lon_radius = max(change_in_longitude_miles(center[0] - lat_radius, radius), change_in_longitude_miles(center[0] + lat_radius, radius))

            self.NW_bound = [center[0] + lat_radius, center[1] - lon_radius]
            self.SE_bound = [center[0] - lat_radius, center[1] + lon_radius]

            self._load_gfs(keep_files)
            # self._load_hrrr(keep_files)

    @staticmethod
    def _load_file(url, local_name):
        resp = requests.get(url, stream=True)
        with open(local_name, "wb") as f:
            for i in resp.iter_content(chunk_size=1024):
                f.write(i)
        return local_name

    NAME_MAP = {
        'U component of wind' : 'UGRD',
        'V component of wind': 'VGRD',
        'Geopotential Height': 'HGT',
    }

    @staticmethod
    def _parse_grbs(grbs):
        height_map = defaultdict(dict)
        latlons = None
        logger.info("Parsing GRIB2 file with %s entries",grbs.messages)
        for grb in grbs:
            if grb['typeOfLevel'] == 'isobaricInhPa' and 'level' in grb.keys():
                data_name = WindModel.NAME_MAP[grb['name']]
                height_map[grb['level']][data_name] = grb.values
                if data_name == 'HGT':
                    height_map[grb['level']]['HGT-AVG'] = grb['avg']
                if latlons is None: latlons = grb.latlons()
        latlons = (latlons[0],latlons[1]-360)
        return height_map, latlons

    def _load_generic(self, ftp_dir, prefix, level_type, expected_forecast, forecast_zeros, filter_type, local_file, keep_file=False):
        try:
            ftp = ftplib.FTP("ftp.ncep.noaa.gov")
            ftp.login()
            ftp.cwd(ftp_dir)
            run_days = [(int(f.replace(prefix, "")), f) for f in ftp.nlst() if prefix in f]
            recent = max(run_days)[1]
            ftp.cwd(recent)
            forecasts = [f for f in ftp.nlst() if level_type in f and not f.endswith(".idx")]
            forecast_postfix = 'f' + str(int(expected_forecast)).zfill(forecast_zeros)
            logger.debug("Selected forecast_postfix: %s",forecast_postfix)
            if not any(forecast_postfix in x for x in forecasts):
                logger.warning("Could not find specified forecast in folder: %s",recent)
                ftp.cwd("..")
                run_days.remove(max(run_days))
                recent = max(run_days)[1]
                logger.info("Trying folder %s instead",recent)
                ftp.cwd(recent)
                forecasts = [f for f in ftp.nlst() if level_type in f and not f.endswith(".idx")]
            # logger.debug("Forecast options: %s", forecasts)
            selected_forecast = [x for x in forecasts if forecast_postfix in x][0]
            params = [
                "file=%s",
                "all_lev=on",
                "var_HGT=on",
                "var_UGRD=on",
                "var_VGRD=on",
                "subregion=",
                "leftlon=%s",
                "rightlon=%s",
                "toplat=%s",
                "bottomlat=%s",
                "dir=%s"
            ]
            constructed_url = "http://nomads.ncep.noaa.gov/cgi-bin/%s?" + "&".join(params)
            constructed_url = constructed_url % (
                filter_type, selected_forecast, self.NW_bound[1], self.SE_bound[1], self.NW_bound[0], self.SE_bound[0],
                "%2F"+recent)
            logger.debug("Constructed URL: %s",constructed_url)
            self._load_file(constructed_url, local_file)
            grbs = pygrib.open(local_file)
            return self._parse_grbs(grbs)
        except:
            raise
        finally:
            try:
                if not keep_file:
                    os.remove(local_file)
            except:
                pass

    def _load_gfs(self, keep_files):
        expected_forecast = max(min(int((self.forecast_date - datetime.datetime.utcnow()).total_seconds() / 3600), 384), 0)
        if expected_forecast >= 120: expected_forecast = expected_forecast / 3 * 3
        logger.info("Loading GFS+%s forecast",expected_forecast)
        local_file = os.path.join("saved","gfs." + str(time.time()) + ".grib2")
        self.gfs_height_map, self.gfs_latlons = self._load_generic("pub/data/nccf/com/gfs/prod", "gfs.", "pgrb2.0p25",
                                                                   expected_forecast, 3, "filter_gfs_0p25.pl", local_file, keep_file=keep_files)
        if keep_files:
            self.gfs_data_file = local_file

    def _load_hrrr(self, keep_files):
        expected_forecast = max(int((self.forecast_date - datetime.datetime.utcnow()).total_seconds() / 3600), 0)
        if expected_forecast > 18: return
        logger.info("Loading HRRR+%s forecast",expected_forecast)
        local_file = os.path.join("saved","hrrr." + str(time.time()) + ".grib2")
        self.hrrr_height_map, self.hrrr_latlons = self._load_generic("pub/data/nccf/com/hrrr/prod", "hrrr.", "wrfprs",
                                                                     expected_forecast, 2, "filter_hrrr_2d.pl", local_file, keep_file=keep_files)
        if keep_files:
            self.hrrr_data_file = local_file

    @staticmethod
    def get_closest_bounds(val, iterable):
        if iterable is None:
            return 0, 0
        arr = np.array(iterable)
        below = arr[arr <= val].max()
        above = arr[arr > val].min()
        return below, above

    @staticmethod
    def get_wind_from_map(lat, lon, alt, height_map, latlons):
        if height_map is None or latlons is None:
            return None, None

        alt_levels = WindModel.get_closest_bounds(alt, [height_map[x]["HGT-AVG"] for x in height_map])

        level_below, level_above = [level for x in alt_levels for level in height_map if height_map[level]["HGT-AVG"] == x]

        if level_below == level_above:
            return None, None

        def lerp(x, x_min, x_max, y_min, y_max):
            return float(y_min * (x_max - x) + y_max * (x - x_min)) / float(x_max - x_min)

        def interp_level(layer):
            lats = latlons[0][:, 0]
            lons = latlons[1][0, :]

            lat_bounds = WindModel.get_closest_bounds(lat, lats)
            lat_idx = [np.where(lats == lat_bounds[i])[0][0] for i in range(2)]
            lon_bounds = WindModel.get_closest_bounds(lon, lons)
            lon_idx = [np.where(lons == lon_bounds[i])[0][0] for i in range(2)]

            def lat_lerp(key, tmp_lon_idx):
                return lerp(lat, lat_bounds[0], lat_bounds[1], layer[key][lat_idx[0], tmp_lon_idx],
                            layer[key][lat_idx[1], tmp_lon_idx])

            lat_interp_0 = [lat_lerp("UGRD", lon_idx[0]), lat_lerp("VGRD", lon_idx[0])]
            lat_interp_1 = [lat_lerp("UGRD", lon_idx[1]), lat_lerp("VGRD", lon_idx[1])]

            return [lerp(lon, lon_bounds[0], lon_bounds[1], lat_interp_0[i], lat_interp_1[i]) for i in range(2)]

        interp_above = interp_level(height_map[level_above])
        interp_below = interp_level(height_map[level_below])

        return [lerp(alt, alt_levels[0], alt_levels[1], interp_below[i], interp_above[i]) for i in range(2)]

    def get_winds(self, lat, lon, alt):
        """
        Get the winds at a particular latitude, longitude and altitude (feet). Returns [North, East] wind in feet/s
        :param lat:
        :param lon:
        :param alt:
        :return:
        """
        alt_m = alt * 0.3048

        ugrd, vgrd = None, None
        # ugrd, vgrd = self.get_wind_from_map(lat, lon, alt_m, self.hrrr_height_map, self.hrrr_latlons)
        if ugrd is None or vgrd is None:
            ugrd, vgrd = self.get_wind_from_map(lat, lon, alt_m, self.gfs_height_map, self.gfs_latlons)

        if ugrd is None or vgrd is None:
            raise Exception("Received invalid gfs levels")

        return [ugrd * 3.28084, vgrd * 3.28084]

DT = 1.0/60.0 # 1 second

def euler(model, start_point, asc_rate, des_rate, launch_alt, burst_alt):
    """Perform an Euler integration. Start point in degrees and arguments in feet and feet/minute"""
    trackup = []
    trackdown = []

    cur_position = start_point
    cur_altitude = launch_alt+0.0001

    burst = False

    while cur_altitude > launch_alt:
        ugrd, vgrd = model.get_winds(cur_position[0],cur_position[1], cur_altitude)
        dx_miles = vgrd * DT * 0.0113636 # to miles/minute
        dy_miles = ugrd * DT * 0.0113636 # to miles/minute
        cur_position[0] += change_in_latitude_miles(dx_miles)
        cur_position[1] += change_in_longitude_miles(cur_position[0], dy_miles)

        if cur_altitude >= burst_alt:
            burst = True

        new_point = (cur_position[0], cur_position[1], cur_altitude)
        if burst:
            trackdown.append(new_point)
            cur_altitude -= des_rate * DT
        else:
            trackup.append(new_point)
            cur_altitude += asc_rate * DT

    return trackup, trackdown


def webPredict(data):
    keys = ["date", "time", "lat", "lon", "launch-alt", "burst-alt", "asc-rate", "des-rate"]
    for key in keys:
        try:
            (data[key])
        except:
            raise Exception, "Invalid %s, Data:%s" % (str(key), data)
    rawTime = datetime.datetime.strptime(data["time"], "%H:%M")
    timeDay = datetime.timedelta(hours=rawTime.hour, minutes=rawTime.minute)
    forecast_date = datetime.datetime.strptime(data["date"], '%Y-%m-%d') + timeDay
    launch_site = [float(data["lat"]), float(data["lon"])]
    model = WindModel(center=launch_site, radius=100, forecast_date=forecast_date)
    return euler(model, launch_site, float(data["asc-rate"]), float(data["des-rate"]), float(data["launch-alt"]), float(data["burst-alt"]))



if __name__ == "__main__":
    # Test
    center = [43.98824490544571, -112.73088455200195]
    radius = 100 # miles
    forecast_date = datetime.datetime.utcnow() + datetime.timedelta(6)
    # model = WindModel(center=center, radius=radius, forecast_date=forecast_date, keep_files=True)
    model = WindModel(gfs_data_file="saved/gfs.1498452054.93.grib2")
    # print model.get_winds(43.816442,-111.7459983, 5000)
    print euler(model, center, 1100, 1500, 5000, 90000)
