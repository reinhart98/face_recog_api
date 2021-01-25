import time
import face_recognition
import base64
import os
import shutil
import compareController as cc
from PIL import Image

compareControl = cc.compareController()

class Controller:
    def __init__(self):
        pass
    
    def rot(self,path,angle):
        image = Image.open(path)
        image= image.rotate(angle)
    
        image.save(path, quality=100)
    
    def most_frequent(self,List): 
        return max(set(List), key = List.count) 
    
    def decodeImage(self,req_data):
        base64Encode = req_data['base64_encode']
        base64Encode = bytes(base64Encode,'ascii')
        # print(base64Encode)
        image_name = req_data['image_name']

        image_64_decode = base64.decodebytes(base64Encode) 
        decodePath = 'decode_images\\{}'.format(image_name)
        dirNameExist = os.path.isdir(decodePath)
        if(dirNameExist):
            dirCheck = os.listdir(decodePath)
            dircheckLen = len(dirCheck)
            if(dircheckLen == 0):
                image_result_pathname = 'decode_images\\{}\\{}.jpg'.format(image_name,image_name)
                image_result = open(image_result_pathname, 'wb') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                return image_result_pathname
            else:
                image_result_pathname = 'decode_images\\{}\\{}{}.jpg'.format(image_name,image_name,dircheckLen+1)
                image_result = open(image_result_pathname, 'wb') # create a writable image and write the decoding result
                image_result.write(image_64_decode)
                return image_result_pathname

        else:
            path = 'decode_images\\{}'.format(image_name)
            os.mkdir(path)
            image_result_pathname = 'decode_images\\{}\\{}.jpg'.format(image_name,image_name)
            image_result = open(image_result_pathname, 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            return image_result_pathname
    
    def decodeImageAndAddtoRegis(self,base64Encode,regisName):
        base64Encode = bytes(base64Encode,'ascii')
        image_64_decode = base64.decodebytes(base64Encode) 
        decodePath = 'images\\{}'.format(regisName)
        dirCheck = os.listdir(decodePath)
        dircheckLen = len(dirCheck)
        if(dircheckLen <= 7):
            image_result_pathname = 'images\\{}\\{}{}.jpg'.format(regisName,regisName,dircheckLen+1)
            image_result = open(image_result_pathname, 'wb') # create a writable image and write the decoding result
            image_result.write(image_64_decode)
            return {
                "return_status":"success",
                "return_message":"added images for user {} ".format(regisName)
            }
        else:
            return{
                "return_status":"failed",
                "return_message":"already 8 or more images in user {}".format(regisName)
            }




    
    def predicImage(self,req_data):
        action = req_data['action']
        try:
            if(action == 'predict'):
                # decode images base64 and place it to decode folder
                res = self.decodeImage(req_data)
                image_name = req_data['image_name']
                dirImageNameExist = os.path.isdir("images\\{}".format(image_name))
                if(dirImageNameExist == False):
                    return {
                        "return_status":"failed",
                        "return_message":"user not yet registered, data not available on images"
                    }
                else:
                    picture_to_predic = face_recognition.load_image_file("images\\{}\\{}.jpg".format(image_name,image_name))
                    my_face_encoding = face_recognition.face_encodings(picture_to_predic)[0]

                    
                    for i in range(4):
                        unknown_picture = face_recognition.load_image_file(res)
                        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)
                        if(len(unknown_face_encoding) == 0):
                            self.rot(res,90)
                        else:
                            break

                    if(len(unknown_face_encoding) != 0):
                        unknown_face_encoding = unknown_face_encoding[0]
                        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding,tolerance=0.4)
                    
                        if results[0] == True:
                            return {
                                "return_status":"success",
                                "return_message":"same"
                            }
                        else:
                            return {
                                "return_status":"success",
                                "return_message":"not same"
                            }
                    else:
                        return{
                            "return_status":"failed",
                            "return_message":"No faces found in the image!"
                        }
                    
            elif(action == 'regis'):
                image_name = req_data['image_name']
                r = shutil.rmtree("decode_images\\{}".format(image_name))
                print(r)
                # check images dir if dir with image_name exist
                dirNameExist = os.path.isdir('images\\{}'.format(image_name))
                if(dirNameExist):
                    dircheck = os.listdir('images\\{}'.format(image_name))
                    if(len(dircheck) > 0):
                        return {
                            "return_status":"failed",
                            "return_message":"already registered"
                        }
                    else:
                        
                        res = self.decodeImage(req_data)
                        shutil.copy(res,'images\\{}'.format(image_name))
                        return {
                            "return_status":"success",
                            "return_message":"user {} registered".format(image_name)
                        }
                else:
                    # print("regis")
                    # create dir with image name
                    os.mkdir('images\\{}'.format(image_name))
                    res = self.decodeImage(req_data)
                    # print(res)
                    shutil.copy(res,'images\\{}'.format(image_name))
                    return {
                        "return_status":"success",
                        "return_message":"registered user {}".format(image_name)
                    }
            elif(action == 'addUserImage'):
                image_name = req_data['image_name']
                base64data = req_data['base64_encode']
                # check if name already exist in image path or not
                dirImageNameExist = os.path.isdir("images\\{}".format(image_name))
                print(dirImageNameExist)
                if(dirImageNameExist == False):
                    return {
                        "return_status":"failed",
                        "return_message":"user folder not yet registered, data not available on images"
                    }
                else:
                    res = self.decodeImageAndAddtoRegis(base64data,image_name)
                    return res
            
            elif(action == 'deleteRegistration'):
                image_name = req_data['image_name']
                regispath = 'images\\{}'.format(image_name)
                r = shutil.rmtree(regispath)
                return{
                    "return_status":'success',
                    "return_message":'success delete registration user {}'.format(image_name)
                }

            elif(action == 'predictToAll'):
                res = self.decodeImage(req_data)
                image_name = req_data['image_name']
                dirImageNameExist = os.path.isdir("images\\{}".format(image_name))
                if(dirImageNameExist == False):
                    return {
                        "return_status":"failed",
                        "return_message":"user not yet registered, data not available on images"
                    }
                else:
                    for i in range(4):
                        resCompare = compareControl.main("images\\{}".format(image_name),res,2,0.4,True)
                        if(resCompare == False):
                            self.rot(res,90)
                        else:
                            break
                    if(resCompare != False):
                        freqMost = self.most_frequent(resCompare)
                        if(freqMost):
                            return {
                                "return_status":"success",
                                "return_message":"same"
                            }
                        else:
                            return {
                                "return_status":"success",
                                "return_message":"not same"
                            }
                    else:
                        return {
                            "return_status":"failed",
                            "return_message":"no person found!"
                        }
        except Exception as e:
            return{
                "return_status":"failed",
                "return_message":str(e)
            }


    
