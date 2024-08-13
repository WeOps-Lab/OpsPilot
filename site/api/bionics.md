The bionics service provides the ability to generate png images from JavaScript configurations and supports EChart charts


## Generate EChart Image

### Python Example
```python
import requests
import base64

url = 'http://bionics.ops-pilot/echart/generate'

options = {
    "options": {
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "data": [820, 932, 901, 934, 1290, 1330, 1320],
                "type": "line",
                "areaStyle": {}
            }
        ]
    },
    "width": 500,
    "height": 200,
    "theme": "westeros",
    "fontSize": 12,
    "mode": "base64"
}

response = requests.post(url, json=options)


if response.status_code == 200:
    
    image_data_base64 = response.text.replace("data:image/png;base64,", "")

    image_data = base64.b64decode(image_data_base64)

    with open("generated_chart.png", "wb") as image_file:
        image_file.write(image_data)

    print("Image successfully saved to 'generated_chart.png'")
else:
    print(f"Failed to generate image. Status code: {response.status_code}")
    print(f"Response: {response.text}")

```

### Rest API

```bash
curl --location --request POST --X POST 'http://bionics.ops-pilot/echart/generate' \
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
| Parameter   | Description                  | Mandatory | Default value | Remarks                                                                                                                                                              |
| ----------- | ---------------------------- | --------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The options | Echart chart Options         | is        |               |
| width       | Canvas width                 | No        | 500           | speed at which the Canvas size will be generated                                                                                                                     |
| height      | Canvas height                | no        | 200           | Canvas size speed at which the canvas will be generated                                                                                                              |
| theme       | Echart's theme               | no        | westeros      |                                                                                                                                                                      |
| fontSize    | Canvas font size             | no        | 12            |                                                                                                                                                                      |
| mode        | The returned image format is | no        | base64        | The optional base64/stream. In Base64 mode, the image is encoded as Base64 and returned to the caller; in Stream mode, the image is returned directly in stream mode |