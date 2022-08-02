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

{
    "service": "GD Weather Service",
    "msg": "上海 黄浦区 当前天气:晴 气温:30 风向:北 风力:≤3 湿度:83\n日期:2022-08-02 星期:2 白天天气:多云 夜间天气:多云 最高气温:35 最低气温: 29\n日期:2022-08-03 星期:3 白天天气:晴 夜间天气:晴 最高气温:37 最低气温: 29\n日期:2022-08-04 星期:4 白天天气:晴 夜间天气:晴 最高气温:37 最低气温: 29\n日期:2022-08-05 星期:5 白天天气:多云 夜间天气:阴 最高气温:37 最低气温: 30\n更新时间: 2022-08-02 23:01:03"
}
```