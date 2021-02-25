import json
import requests
headers = {"Authorization": "Bearer ya29.a0AfH6SMDT7CvvI-GDh-2yOZn3jGGpfEHPPZKCQl1zCrfWMPe7xm0R5vOUzWjv61tGP4ZqJCHFBwRYKPF7gc-iXkh0j63pJifm9WSRvgKb3zpnQP-1hJdjDcpxiddE_L0fbvzZioMD4L8JhnRjleuQgsHI8N7O8pBfbeOiPV6Y3Ck"}
para = {
    "name": "test.jpg",
    "parents": ["1lMBii79CfFiG7t9KcUS0cB-4EvmpV8Pf"]
}
files = {
    'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    'file': open("./files/ttt.jpg", "rb")
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files
)
print(r.text)