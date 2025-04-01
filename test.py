import requests

url = "http://127.0.0.1:8000/question-detect/"
files = {"file": open("doc.jpeg", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("Image saved as output.png")
else:
    print(f"Error: {response.status_code}")