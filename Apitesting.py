import os
import requests
import json

def upload_document(file_name, file_path):
  url = str(os.environ.get('BACKEND_URL'))+"/api/upload/uploadDocument"
  print("upload URL", url)
  payload={}
  files=[
    ('documentFile',(file_name,open(file_path+file_name,'rb'),'text/csv'))
  ]
  headers = {}

  print(files)
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  print(response.text)
  response_dict = json.loads(response.text)
  inputdata = response_dict["data"]["documentFileUrl"]
  print(inputdata)
  return inputdata["original"]

#create main
def main():
  file_name = "61ef72ed396fc5330c15f250-insights.png"
  file_path = "tmp/"
  print(upload_document(file_name, file_path))

#call main
if __name__ == "__main__":
  os.environ["BACKEND_URL"] = "http://34.129.168.181:8000"

  main()
