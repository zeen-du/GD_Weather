# GD Weather Service

## Deploy
```shell
docker build -t gd-weather-service --network=host .
docker run -d --name gd_weather_service -e GD_SERVICE_URL=https://restapi.amap.com -e GD_API_KEY=xxx gd-weather-service
```