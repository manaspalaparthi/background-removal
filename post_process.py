import json
import requests
import zipfile
import os
import backend 

def run(jobID, dataLocation):
    """
    title:: 
        run
    description:: 
        takes dataset URL and jobID as input, download the dataset and read the input
    inputs:: 
    jobID 
       Job ID from datashop application
    dataFileURL
        Downloadable URL of the dataset
        
    returns:: 
    payloadforservice
        payload for model/service
    
    """
    insightsS3Link = ""
    file_name = dataLocation.split("/")[-1]
    file_path = dataLocation.replace(file_name,"")

    try:
        insightsS3Link = backend.upload_image(file_name, file_path)
        print("insights link here:",insightsS3Link)
        return updateJob(jobID, insightsS3Link, None)

    except Exception as e:
        return updateJob(jobID, None, str(e))
        

def updateJob(jobID, insightsS3Link, err):
    """
    title:: 
        __updateJob
    description:: 
        Update the dataapplication with insightsLink.
    inputs:: 
    jobID 
       Job ID from datashop application.
    insightsS3Link
       Downloadable URL of the insights.
        
    returns:: 
    payloadforservice
        response from the datashop application.
    """

    status_map = {'status_code': '', 'json_response': ''}
    dataShopEndpointURL = os.environ.get('BACKEND_URL')+"/api/job/updateJob"

    if(err):
        payload = json.dumps({
            "insightFileURL": "N/A",
            "jobid":jobID
        })
    else:
        payload = json.dumps({
                    "insightFileURL": insightsS3Link,
                    "jobid":jobID
                })

    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("PUT", dataShopEndpointURL, headers=headers, data=payload)
    status_map["json_response"] = json.dumps(response.text)
    status_map["status_code"] = response.status_code
    return status_map


    
def zip_output_files(fileLocationToZip):

    zip_file = "tmp/post-process/" + fileLocationToZip.split("/")[-1]+ ".zip"
    
    with zipfile.ZipFile(zip_file, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(fileLocationToZip):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
                
    print(f"Files zipped to : {zip_file}")

