from urllib.parse import urljoin

from app.api.config import settings

WEATHER_URL = urljoin(settings.gd_service_url, "v3/gd_weather/weatherInfo")
GEO_URL = urljoin(settings.gd_service_url, "v3/geocode/geo")
POI_URL = urljoin(settings.gd_service_url, "v3/place/text")
