import requests
import zipfile
import os
import cv2


"""
    title:: pre_process
    description:: takes dataset URL and jobID as input, download the dataset and read the input.
    
"""
def run(jobID, url,json1):
    """
    title:: 
        run
    description:: 
        takes dataset URL and jobID as input, download the dataset and read the input
    inputs:: 
    jobID 
       Job ID from datashop application
    url
       Downloadable URL of the dataset
    json1
       json data from the model.
        
    returns:: 
    payloadforservice
        payload for model/service
    """
    
    if( (json1 == '') and (url == '') ):
        inputPayloadForService = ''
        return inputPayloadForService
    elif( url == ''  ):
        inputPayloadForService = json1['body']
        return inputPayloadForService            
    elif( json1 == '' ):
        input_file_location,fileName = downloadFile(jobID,url)
        if fileName.endswith(".zip"):
            extracted_folder,files_list = extract_zip_file(input_file_location) 
            extractedFileLocation = extracted_folder+files_list[0]
            #Write your code here to handle your files in zip.
            os.chdir(extracted_folder)
            with open(extractedFileLocation) as f: 
                inputPayloadForService = f.read()  
        else:
            #Handle your file located in location - input_file_location
            image = cv2.imread(input_file_location)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            success, encoded_image = cv2.imencode('.png', image)
            content2 = encoded_image.tobytes()

            # Handle your file located in location - input_file_location
            # with open(input_file_location) as f:
            inputPayloadForService = content2
        return inputPayloadForService
    
    else:
        fileName = url.split("/")[-1]
        input_file_location = f"tmp/{jobID}-{fileName}"
        req = requests.get(url)
        with open(input_file_location, 'wb') as fileHandle :
            fileHandle.write(req.content)
        print(f"File Downloaded to {input_file_location}")
        with open(input_file_location) as f: 
            inputPayloadFromURL = f.read()  
        
        inputPayloadFromJSON = json1['body']            
        inputPayloadForService = [inputPayloadFromURL,inputPayloadFromJSON]    
        
        return inputPayloadForService



def extract_zip_file(zipped_file):
    """
    title:: 
        extract_zip_file
    description:: 
        extract the files in the zip file.
    inputs::
        zipped_file
             URL for the downloaded zipfile.
    returns::
         extracted_folder
              extracted zip files 
    """
    
    extracted_folder = "tmp/pre-process/" + zipped_file.split("/")[-1].replace(".zip", "")+"/"
    with zipfile.ZipFile(zipped_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_folder)
    print(f"Files extracted to {extracted_folder}")
    print(f"list of filenames:  {zip_ref.namelist()}")
    
    return extracted_folder, zip_ref.namelist()
     
def downloadFile(jobID,url):     
    fileName = url.split("/")[-1]
    input_file_location = f"tmp/{jobID}-{fileName}"
    # try:
    req = requests.get(url)
        
    with open(input_file_location, 'wb') as fileHandle :
        fileHandle.write(req.content)
    print(f"File Downloaded to {input_file_location}")

    return input_file_location,fileName
    # except:
    #     print("Error in downloading file")
    #     raise ValueError("Erro Downloading File")


