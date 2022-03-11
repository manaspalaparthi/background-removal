import json
import requests
import zipfile
import os
import backend
from kafka import KafkaProducer

def run(input_dict, dataLocation):
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
        return updateJob_kafka(input_dict, insightsS3Link, None)

    except Exception as e:
        return updateJob_kafka(input_dict, None, str(e))


def updateJob_kafka(input_dict, insightsS3Link, err):
    """
    title::
        __updateJob
    description::
        Update the dataapplication with insightsLink.
    inputs::
    jobID
       Job ID from datashop application.
       kafka_URL from input_dict["kafkaBrokerURL"]
       kafka_Group from input_dict["kafkaGroupId"]
       kafka_Topic from input_dict["kafkaTopic"]

    insightsS3Link
       Downloadable URL of the insights.

    returns::
             none
    """

    #status_map = {'status_code': '', 'json_response': ''}
    #dataShopEndpointURL = f"{os.environ.get('BACKEND_URL')}/api/job/updateJob"

    jobID = input_dict["jobID"]
    kafka_URL = input_dict["kafkaBrokerURL"]
    kafka_Group = input_dict["kafkaGroupId"]
    kafka_Topic = input_dict["kafkaTopic"]

    if "".__eq__(kafka_URL) and "".__eq__(kafka_Group) and "".__eq__(kafka_Topic):
        return "ERROR NO KAFKA CONFIGURATION"

    if (err):
        payload = json.dumps({
            "insightFileURL": "N/A",
            "jobid": jobID,
            "jobStatus": "failed"

        })
    else:
        payload = json.dumps({
            "insightFileURL": insightsS3Link,
            "jobid": jobID,
            "jobStatus": "success"
        })

    producer = KafkaProducer(bootstrap_servers=kafka_URL, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    producer.send(kafka_Topic, payload)

    # Quit Kafka
    producer.close()

    return None


def zip_output_files(fileLocationToZip):

    zip_file = "tmp/post-process/" + fileLocationToZip.split("/")[-1]+ ".zip"
    
    with zipfile.ZipFile(zip_file, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(fileLocationToZip):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, basename(filePath))
                
    print(f"Files zipped to : {zip_file}")

