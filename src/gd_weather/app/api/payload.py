# -*- coding: utf-8 -*-
from typing import List, Optional

from pydantic import BaseModel, validator


class POIModel(BaseModel):
    pname: Optional[str]  # 省份
    cityname: Optional[str]  # 市
    adname: Optional[str]  # 区
    address: Optional[str]  # 地址
    name: Optional[str]  # 名称
    location: Optional[str]  # 经纬度(lng,lat)
    level: Optional[str]
    adcode: Optional[str]  # 城市code

    @property
    def lng(self):
        # 精度 longitude
        return float(self.location.split(",")[0]) if self.location else None

    @property
    def lat(self):
        # 纬度 latitude
        return float(self.location.split(",")[1]) if self.location else None

    @property
    def level_in_address(self):
        return self.level in ["热点商圈", "兴趣点", "门牌号", "单元号", "道路", "道路交叉路口", "公交站台、地铁站", "村庄"]

    @validator("address", pre=True)
    def address_check(cls, value):
        return "" if not value else value

    @property
    def complete_address(self):
        return f"{self.cityname}{self.adname}{self.name}"


class Casts(BaseModel):
    date: str
    week: str
    dayweather: str
    nightweather: str
    daytemp: str
    nighttemp: str
    daywind: str
    nightwind: str
    daypower: str
    nightpower: str

    @classmethod
    def format_str(cls, values):
        return f"日期:{values['date']} 星期:{values['week']} 白天天气:{values['dayweather']} " \
               f"夜间天气:{values['nightweather']} 最高气温:{values['daytemp']} 最低气温: {values['nighttemp']}"


class Forecast(BaseModel):
    province: str
    city: str
    adcode: str
    reporttime: str  # 数据发布的时间
    casts: List[Casts]

    @classmethod
    def format_str(cls, values):
        resp = ""
        for value in values['casts']:
            string = f"日期:{value['date']} 星期:{value['week']} 白天天气:{value['dayweather']} " \
                     f"夜间天气:{value['nightweather']} 最高气温:{value['daytemp']} 最低气温: {value['nighttemp']}\n"
            resp += string
        return resp


class Lives(BaseModel):
    province: str
    city: str
    adcode: str
    weather: str  # 天气现象（汉字描述）
    temperature: str  # 实时气温，单位:摄氏度
    winddirection: str  # 风向描述
    windpower: str  # 风力级别，单位:级
    humidity: str  # 空气湿度
    reporttime: str  # 数据发布的时间

    @classmethod
    def format_str(cls, values):
        return f"{values['province']} {values['city']} 当前天气:{values['gd_weather']} 气温:{values['temperature']} " \
               f"风向:{values['winddirection']} 风力:{values['windpower']} 湿度:{values['humidity']}\n"


class WeatherModel(BaseModel):
    reporttime: Optional[str]
    lives: Optional[List[Lives]]
    forecasts: Optional[List[Forecast]]
