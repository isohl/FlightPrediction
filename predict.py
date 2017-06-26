import requests
import pygrib
import datetime
import time
import ftplib
import os
from collections import defaultdict
import numpy as np


class WindModel(object):
    def __init__(self, center=None, radius=None, forecast_date=None):
        """
        Construct a wind model centered at a given Latitude/Longitude with a radius defined in degrees
        :param center:
        :param radius:
        :param forecast_date:
        """
        if center is None or radius is None or forecast_date is None:
            raise Exception("Invalid center or radius for wind model")

        self.center = center
        self.radius = radius
        self.forecast_date = forecast_date
        self.gfs_height_map = None
        self.gfs_latlons = None
        self.hrrr_height_map = None
        self.hrrr_latlons = None

        self.NW_bound = [self.center[0] - self.radius, self.center[1] - self.radius]
        self.SE_bound = [self.center[0] + self.radius, self.center[1] + self.radius]

        self._load_gfs()
        self._load_hrrr()

    @staticmethod
    def _load_file(url, local_name):
        resp = requests.get(url, stream=True)
        with open(local_name, "wb") as f:
            for i in resp.iter_content(chunk_size=1024):
                f.write(i)
        return local_name

    @staticmethod
    def _parse_grbs(grbs):
        height_map = defaultdict()
        layer_map = defaultdict(defaultdict())
        latlons = None
        for grb in grbs:
            if grb['typeOfLevel'] == 'isobaricInhPa':
                height_map[grb["layer"]][grb["name"]] = grb.value
                if latlons is None: latlons = grb.latlons()
        for level in layer_map:
            layer = layer_map[level]
            height_map[layer["HGT"]] = {"UGRD":layer["UGRD"], "VGRD":layer["VGRD"], "hPa":layer}
        return height_map, latlons

    def _load_generic(self, ftp_dir, prefix, level_type, expected_forecast, filter_type):
        try:
            ftp = ftplib.FTP("ftp.ncep.noaa.gov")
            ftp.login()
            ftp.cwd(ftp_dir)
            recent = max((int(f.replace(prefix, "")), f) for f in ftp.nlst() if prefix in f)[1]
            ftp.cwd(recent)
            forecasts = [f for f in ftp.nlst() if level_type in f and not f.endswith(".idx")]
            selected_forecast = [x for x in forecasts if 'f' + str(expected_forecast).zfill(3) in x][0]
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
            constructed_url = constructed_url % (filter_type, selected_forecast, self.NW_bound[1], self.SE_bound[1], self.NW_bound[0], self.SE_bound[0], recent)
            print constructed_url
            local_file = self._load_file(constructed_url, prefix + str(time.time()) + ".grib2")
            grbs = pygrib.open(local_file)
            return self._parse_grbs(grbs)
        except:
            raise
        finally:
            try:
                os.remove(local_file)
            except: pass


    def _load_gfs(self):
        expected_forecast = max(min((self.forecast_date - datetime.datetime.utcnow()).total_seconds() / 3600, 384),0)
        if expected_forecast >= 120: expected_forecast = expected_forecast / 3 * 3
        self.gfs_height_map, self.gfs_latlons = self._load_generic("pub/data/nccf/com/gfs/prod", "gfs.", "pgrb2.0p25", expected_forecast,"filter_gfs_0p25.pl")

    def _load_hrrr(self):
        expected_forecast = max((self.forecast_date - datetime.datetime.utcnow()).total_seconds() / 3600,0)
        if expected_forecast > 18: return
        self.hrrr_height_map, self.hrrr_latlons = self._load_generic("pub/data/nccf/com/hrrr/prod", "hrrr.", "wrfprs", expected_forecast,"filter_hrrr_2d.pl")

    @staticmethod
    def get_closest_bounds(val, iterable):
        if iterable is None:
            return 0, 0
        below = 0
        above = 0
        for level in iterable:
            if level < val:
                below = level
            if above <= below:
                above = level
        return below, above

    @staticmethod
    def get_wind_from_map(lat, lon, alt, height_map, latlons):
        if height_map is None or latlons is None:
            return None, None

        level_below, level_above = WindModel.get_closest_bounds(alt, height_map)

        if level_below == level_above:
            return None, None

        def lerp(x, x_min, x_max, y_min, y_max):
            return float(y_min * (x_max - x) + y_max * (x - x_min)) / float(x_max - x_min)

        def interp_level(layer):
            lats = latlons[0][:,0]
            lons = latlons[1][0,:]

            lat_bounds = WindModel.get_closest_bounds(lat, lats)
            lat_idx = [np.where(lats==lat_bounds[i])[0][0] for i in range(2)]
            lon_bounds = WindModel.get_closest_bounds(lon, lons)
            lon_idx = [np.where(lons == lon_bounds[i])[0][0] for i in range(2)]

            def lat_lerp(key, tmp_lon_idx):
                return lerp(lat, lat_bounds[0], lat_bounds[1], layer[key][lat_idx[0],tmp_lon_idx],layer[key][lat_idx[1],tmp_lon_idx])

            lat_interp_0 = [lat_lerp("UGRD",lon_idx[0]),lat_lerp("VGRD",lon_idx[0])]
            lat_interp_1 = [lat_lerp("UGRD", lon_idx[1]), lat_lerp("VGRD", lon_idx[1])]

            return [lerp(lon, lon_bounds[0], lon_bounds[1], lat_interp_0[i], lat_interp_1[i]) for i in range(2)]

        interp_above = interp_level(height_map[level_above])
        interp_below = interp_level(height_map[level_below])

        return [lerp(alt, level_below, level_above, interp_below[i], interp_above[i]) for i in range(2)]

    def get_winds(self, lat, lon, alt):
        """
        Get the winds at a particular latitude, longitude and altitude (feet). Returns [North, East] wind in feet/s
        :param lat:
        :param lon:
        :param alt:
        :return:
        """
        alt_m = alt * 0.3048

        ugrd, vgrd = self.get_wind_from_map(lat, lon, alt_m, self.hrrr_height_map, self.hrrr_latlons)
        if ugrd is None or vgrd is None:
            ugrd, vgrd = self.get_wind_from_map(lat, lon, alt_m, self.gfs_height_map, self.gfs_latlons)

        if ugrd is None or vgrd is None:
            raise Exception("Received invalid gfs levels")

        return [ugrd * 3.28084, vgrd * 3.28084]
