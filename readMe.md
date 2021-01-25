# GUIDE

- install cmake separately if u run on windows, you need install cmake separately if you are in windows
- `pip install -r requirements.txt`
- `python app.py`

## images folder save know or registered picture with folder of the name or the person

## decoded_image is where the images from api is saved and then used for compare or recognition

## Ex Postman API, change the ip into the ip of yours where you run the code

### json key

```
{
    "image_name": "image name to compare in the image folder",
    "base64_encode": "base64 image format string",
    "action": "regis"
}
```

#### action list

- regis : regis user known image to folder image
- predict : predict 1:1 image
- addUserImage : add image to folder user image
- deleteRegistration
- predictToAll : predict image sent with all images in folder image
