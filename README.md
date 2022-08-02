# GD Weather Service

## Deploy
```shell
docker build -t gd-weather-service --network=host .
docker run -d --name gd_weather_service -e GD_SERVICE_URL=https://restapi.amap.com -e GD_API_KEY=xxx -e token=xxx gd-weather-service
```

## curl
```shell
curl --location --request GET 'http://localhost:8000/weather?text=上海' \
--header 'token: xxx'
```