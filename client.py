import requests

response = requests.get("http://127.0.0.1:5000/announcements/1")
#     json={"title": "down", "discription" : "ads afkan fafafaf", "owner": "skyzero"},     
# )

print(response.json())
print(response.status_code)

