# import json
import pandas
import numpy as np
from rembg.bg import remove
import io
from PIL import Image
import cv2
# import boto3
# import os

import pickle

def run(jobID, dataInput):
  """
  title:: 
      run
  description:: 
      Run the model/get the predictions according the service.
  inputs::
      jobID 
            Job ID from datashop application
      dataInput
           input Payload For the Service
  returns::
      insightsDataFileLocation
           insights data file location. 
  """
  result = remove(dataInput)

  img = Image.open(io.BytesIO(result)).convert("RGBA")

  img_np = np.array(img)
  insightsDataFileLocation = f"tmp/{jobID}-insights.png"
  cv2.imwrite(insightsDataFileLocation, img_np)
  print(insightsDataFileLocation)
  return insightsDataFileLocation
