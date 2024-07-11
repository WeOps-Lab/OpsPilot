# Bionics

![](https://wedoc.canway.net/imgs/img/嘉为蓝鲸.jpg)

Bionic是一个后端图表生成服务，具备将前端图表在`无需Headless浏览器`的条件下，在服务端生成图片，并返回给客户端:

* 支持生成EChart图片


## 调用示例

### 生成EChart图片

参数说明

参数|描述|必填|默认值|备注
---|----|----|----|---
options|Echart的图表Options|是||
width|Canvas宽度|否|500|Canvas的大小会生成的速度
height|Canvas高度|否|200|Canvas的大小会生成的速度
theme|Echart的主题|否|westeros||
fontSize|Canvas字体大小|否|12||
mode|返回的图片形式|否|base64| 可选  base64/stream, Base64模式下，图片会被编码为Base64返回调用端，Stream模式下，图片会直接以stream的模式返回


示例
```
curl --location --request POST --X POST 'http://127.0.0.1:7001/echart/generate' \
--header 'User-Agent: Apipost client Runtime/+https://www.apipost.cn/' \
--header 'Content-Type: application/json' \
--data '{
	"options":{
      "xAxis": {
        "type": "category",
        "boundaryGap": false,
        "data": [ "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ]
      },
      "yAxis": {
        "type": "value"
      },
      "series": [
        {
          "data": [ 820, 932, 901, 934, 1290, 1330, 1320 ],
          "type": "line",
          "areaStyle": {}
        }
      ]
    }
}'
```


生成的样例图表为

![示例图片](./doc/images/%E7%A4%BA%E4%BE%8B.png)

