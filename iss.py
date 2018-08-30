import requests
import json

response=requests.get("http://api.open-notify.org/iss-now.json")
response_json=response.content

response_dict=json.loads(response_json)

print(response_dict)
print(response_dict['timestamp'])



