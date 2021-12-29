import requests
import json


class APIs:
    
    def __init__(self,api_token:str):

        self.headers = {
            "Authorization":"Bearer {}".format(api_token)
            }
        self.root_url = 'https://api-dev.headspin.io'
    

    def listAllDevices(self):
        api_URL = self.root_url+"/v0/devices"

        response = requests.get(api_URL,headers=self.headers)

        return response
    
    
    def sendADB_cmd(self,device_id:str,adb_cmd:str) -> requests.Response:
        api_URL = self.root_url+"/v0/adb/{}/shell".format(device_id)
        data  = adb_cmd

        response = requests.post(api_URL,headers=self.headers,data=data)

        return response
    
    def install_apk(self,device_id,*,apk_file_path:str=None,apk_id:str=None) -> requests.Response:

        api_URL = self.root_url+"/v0/adb/{}/install".format(device_id)

        if apk_id:
            api_URL += "?apk_id={}".format(apk_id)

            response = requests.post(api_URL,headers=self.headers)
        elif apk_file_path:

            with open(apk_file_path,"rb") as bin_file:
                data = bin_file.read()

            response = requests.post(api_URL,headers=self.headers,data=data)
        
        else:
            raise ValueError("Error should have either apk_file_path or apk_id")
        
        return response
    
    def uninstall_app_android(self,device_id,package_name):
        api_URL = self.root_url+"/v0/adb/{}/uninstall?package={}".format(device_id,package_name)

        response = requests.post(api_URL,headers=self.headers)

        return response


    
    def createUpload_userflow_status(self,session_id:str,test_name:str=None,status:str=None) -> requests.Response:
        api_URL = self.root_url+"/v0/perftests/upload"

        data = { "session_id": session_id }

        if test_name:
            data["test_name"] = test_name
        if status:
            data["status"] = status
        
        if data:
            response = requests.post(api_URL,headers=self.headers,data=json.dumps(data))

        return response
    
    def pageLoadAnalysis_set(self,session_id:str,name:str,ts_start,ts_end,start_sensitivity:float=None,end_sensitivity:float=None,video_box:list=None) ->requests.Response:

        api_URL = self.root_url+"/v0/sessions/analysis/pageloadtime/{}".format(session_id)

        region = {  "name": name,"ts_start":ts_start,"ts_end":ts_end }

        if start_sensitivity:
            region["start_sensitivity"] = start_sensitivity
        if end_sensitivity:
            region["end_sensitivity"] = end_sensitivity

        if video_box:
            region["video_box"] = video_box


        data = {  "regions":[ region ] }

        response = requests.post(api_URL,headers=self.headers,data=json.dumps(data))

        return response
    

    def addLabels_session(self,session_id:str,name:str,ts_start,ts_end,*,label_type:str="user",arguments:dict=None) -> requests.Response :
        
        api_URL = self.root_url+"/v0/sessions/{}/label/add".format(session_id)

        label = {  "name": name,"ts_start":ts_start,"ts_end":ts_end }

        if label_type:
            label["label_type"] = label_type

        if arguments :
            if label_type == "user" and "category" in arguments:
                label["category"] = arguments["category"]
            
            if label_type == "page-load-request":
                if "start_sensitivity" in arguments:
                    label["data"] = { "start_sensitivity" : arguments["start_sensitivity"] }

                if "end_sensitivity" in arguments:
                    label["data"] = { "end_sensitivity" : arguments["end_sensitivity"] }

                if "video_box" in arguments:
                    label["video_box"] = arguments["video_box"]
        
        data = { "labels" : [ label ] }

        response = requests.post(api_URL,headers=self.headers,data=json.dumps(data))

        return response


    
    def assignSessionNameDiscription(self,session_id:str,name:str=None,description:str=None) -> requests.Response:

        api_URL = self.root_url+"/v0/sessions/{}/description".format(session_id)

        data = {}

        if name:
            data["name"] = name
        if description:
            data["description"] = description

        if data :
            response = requests.post(api_URL,headers=self.headers,data=json.dumps(data))       
        
        return response
    
    def get_allDeviceAutomaticTestingConfig(self) ->requests.Response:

        api_URL = self.root_url+"/v0/devices/automation-config"

        response = requests.get(api_URL,headers=self.headers)

        return response
    
    def get_allDevices(self) -> requests.Response:
        api_URL = self.root_url+"/v0/devices"

        response = requests.get(api_URL,headers=self.headers)

        return response
    
    def lockDevice_android(self,device_id:str) -> requests.Response:
        api_URL = self.root_url+"/v0/adb/{}/lock".format(device_id)


        response = requests.post(api_URL,headers=self.headers)

        return response
    
    def unlockDevice_android(self,device_id:str) -> requests.Response :

        api_URL = self.root_url+"/v0/adb/{}/unlock".format(device_id)

        response = requests.post(api_URL,headers=self.headers)
        
        return response
    
    def unlock_device(self,*,selector:dict=None) -> requests.Response :

        api_URL = self.root_url+"/v0/devices/unlock"

        if selector:
            data = json.dumps(selector)

            response = requests.post(api_URL,headers=self.headers,data=data)
        else:
            response = requests.post(api_URL,headers=self.headers)
        
        return response


    

    def start_sessionCapture(self,device_address:str,allow_replace:bool=True,capture_network:bool=False):
        api_URL = self.root_url+"/v0/sessions"

        data = {
            "session_type": "capture",
            "device_address": device_address,
            "allow_replace": allow_replace,
            "capture_video": True,
            "capture_network" : capture_network
        }
        response = requests.post(api_URL, headers=self.headers, data = json.dumps(data))

        return response
    
    def stop_sessionCapture(self,session_id:str) -> requests.Response :
         api_URL = self.root_url+"/v0/sessions/{}".format(session_id)

         data = "{\"active\": false}"

         response = requests.patch(api_URL,headers=self.headers,data=data)

         return response
        
    def fetchTimestamp_session(self,session_id:str) -> requests.Response :

        api_URL = self.root_url+"/v0/sessions/{}/timestamps".format(session_id)

        response = requests.get(api_URL,headers= self.headers)

        return response
    
    def addTages_session(self,session_id:str,tags:list) -> requests.Response:

        api_URL = self.root_url+"/v0/sessions/tags/{}".format(session_id)

        data = {
            "tags":tags
        }

        response = requests.post(api_URL,headers=self.headers,data=json.dumps(data))

        return response
    
    def listAllApps_iosIdevice(self,device_id:str,return_result="JSON" ) -> requests.Response :


        api_URL = self.root_url+"/v0/idevice/{}/installer/list".format(device_id)

        if return_result == None:
            pass        
        elif return_result.upper() == "JSON":
            api_URL += "?json"
        elif return_result.upper() == "XML":
            api_URL += "?flags=--xml"

        response = requests.get(api_URL,headers=self.headers)

        return response

    def listUploadedAPKsInfo(self):

        api_URL = self.root_url+"/v0/apps/apks"

        response = requests.get(api_URL,headers=self.headers)

        return response
    
    def adbBridge(self,device_id:str) -> requests.Response:

        api_URL = self.root_url+"/v0/adb/{}/bridge".format(device_id)

        response = requests.post(api_URL,headers=self.headers)

        return response

















        

    
