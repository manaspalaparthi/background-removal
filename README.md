#Background removal service

**dowload the model to models/ folder**

https://models.s3.ap-southeast-2.amazonaws.com/u2net.onnx


**Building a docker**

Include necessary packages for your model in requirements.txt. We prefer you to use pip freeze > requirements.txt 


**docker build** dockerimagename:tagname .

**RUN Command for DOCKER**

To run the container 

```
docker pull ashith1/rgbm-service:docker
```

please datashop backend with live backend.

```
docker run -d -e BACKEND_URL=datashopbackend -p 5000:5000 ashith1/rgbm-service:docker
```
