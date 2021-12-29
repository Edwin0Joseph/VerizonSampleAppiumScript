from headspin import APIs

class KPIs:

    def __init__(self):
        self.__kpis = {}

    

    def add_kpi(self,name:str,ts_start,ts_end,*,label_type:str="user",category:str=None,options:dict=None):

        type_list = ("user","page-load-request","audio-activity-request","video-content")

        label_type = label_type.lower().strip()
        

        if label_type not in type_list:
            raise Exception("Error - 'label_type' value should be"," or ".join(type_list))

        kpi =  {

            "label_type": label_type,
            "ts_start":ts_start,
            "ts_end":ts_end
            }
        
        kpi["options"] = options

        if category and label_type == "user":
            kpi["category"]
        

        self.__kpis[name] = kpi
    
    def get_kpis(self) -> dict:
        return self.__kpis


class Session:

    __session_id = None
    __session_time = {}

    def __init__(self,api_token):
        self.__test_name = None
        self.__info = None
        self.hs_api = APIs(api_token)

    def __add_userflowName(self):
        resp = self.hs_api.createUpload_userflow_status(self.__session_id,test_name=self.__test_name)

        try:
            resp.raise_for_status()

        except:
            print("    Failed to Add Session to Userflow '{}'".format(self.__test_name))
            print(resp.text)
    
    def __add_userflowStatus(self):

        resp = self.hs_api.createUpload_userflow_status(self.__session_id ,status=self.__test_status)

        try:
            resp.raise_for_status()

        except:
            print("    Failed to Add Session Status '{}' to Userflow {}".format(
                self.__test_status,self.__test_name
                ))            
            print(resp.text)

    def __add_nameDiscription(self):

        name = "{app_name}".format(
            app_name=self.__info["appName"]
            )
        
        description = "Test_Name:"+self.__test_name

        try:
            description += "\nApp_Package:"+self.__info["appPackage"]
        except KeyError:
            pass
        try:
            description += "\nBundle_ID:"+self.__info["bundleId"]
        except KeyError:
            pass

        description += "\nApp_Version:"+self.__info["appVersion"]
        description +=  "\nTest_Status:"+self.__test_status

        if self.__test_status.lower() == "passed" and self.__failed_reason:
            description += "\nFAILED REASON:"+self.__failed_reason        

        resp = self.hs_api.assignSessionNameDiscription(
            self.__session_id,
            name=name,
            description=description
            )
        resp.raise_for_status()
    
    def __verify_correct_sessionKpi(self,kpi):

        if self.__session_time:

            session_start_time = self.__session_time["start_time"]

            if session_start_time > self.__kpis[kpi]["ts_start"]:
                    self.__kpis[kpi]["ts_start"] += (session_start_time - self.__kpis[kpi]["ts_start"])
            
            try:
                session_end_time =self.__session_time["end_time"]

                if session_end_time < self.__kpis[kpi]["ts_end"]:
                    self.__kpis[kpi]["ts_end"] -= (self.__kpis[kpi]["ts_end"] - session_end_time)
            

            except:
                pass

    def __get_session_capture_time(self):

        if not self.__session_time:
            resp = self.hs_api.fetchTimestamp_session(self.__session_id)

            resp.raise_for_status()

            r = resp.json()

            self.__session_time["start_time"] = r["capture-started"]
            self.__session_time["end_time"] = r["capture-ended"]


    
    def __add_sessionKpis(self):

        for kpi in self.__kpis:

            self.__verify_correct_sessionKpi(kpi)            
            
            print("     . Adding {}".format(kpi))

            label_type = self.__kpis[kpi]["label_type"]

            if label_type == "page-load-request":
                self.__add_pageLoadAnalysisRegion(kpi)
            elif label_type == "video-content":
                self.__add_videoContentAnalysisRegion(kpi)
            elif label_type == "user":
                self.__add_labelRegion(kpi)
    

    def __add_labelRegion(self,kpi):

        options = self.__kpis[kpi]["options"]

        if  "category" in options:
            arguments= {"category":options["category"]}
        else:
            arguments= {"category":"Desired Region"}


        resp = self.hs_api.addLabels_session(
            self.__session_id,
            name=kpi,
            ts_start=self.__kpis[kpi]["ts_start"],
            ts_end=self.__kpis[kpi]["ts_end"],
            label_type=self.__kpis[kpi]["label_type"],
            arguments=arguments
        )
            
        try:
            resp.raise_for_status()
            # print("Label:",resp.text)
        except:
            print(
                "    ! Failed to Add '{}' Region in Session '{}'".format(
                    kpi,
                    self.__session_id
                    )
                )
            print(resp.text)
    
    def __add_pageLoadAnalysisRegion(self,kpi):        

        options = self.__kpis[kpi]["options"]


        # start_sensitivity = end_sensitivity = None

        # resp = self.hs_api.pageLoadAnalysis_set(
        #         self.__session_id,
        #         name=kpi,
        #         ts_start=self.__kpis[kpi]["ts_start"],
        #         ts_end=self.__kpis[kpi]["ts_end"],
        #         start_sensitivity=start_sensitivity,
        #         end_sensitivity=end_sensitivity
        #         )

        

        if options:
            arguments = {}
            try:
                arguments["start_sensitivity"] = options["start_sensitivity"]
            except KeyError:
                pass
            try:
                arguments["end_sensitivity"] = options["end_sensitivity"]
            except KeyError:
                pass
            try:
                arguments["video_box"] = options["video_box"]
            except KeyError:
                pass
        else:
            arguments =  None

        resp = self.hs_api.addLabels_session(
            self.__session_id,
            name=kpi,
            ts_start=self.__kpis[kpi]["ts_start"],
            ts_end=self.__kpis[kpi]["ts_end"],
            label_type=self.__kpis[kpi]["label_type"],
            arguments=arguments
        )
            
        try:
            resp.raise_for_status()
            # print("Page Load Label:",resp.text)
        except:
            print(
                "    Failed to Add '{}' Page Load Analysis Region in Session '{}'".format(
                    kpi,
                    self.__session_id
                    )
                )
            print(resp.text)
    
    def __add_videoContentAnalysisRegion(self,kpi):

        resp = self.hs_api.addLabels_session(
            self.__session_id,
            name=kpi,
            ts_start=self.__kpis[kpi]["ts_start"],
            ts_end=self.__kpis[kpi]["ts_end"],
            label_type=self.__kpis[kpi]["label_type"],
        )
            
        try:
            resp.raise_for_status()
            # print("Video Content Label:",resp.text)
        except:
            print(
                "    Failed to Add '{}' Video Content Analysis Region in Session '{}'".format(
                    kpi,
                    self.__session_id
                    )
                )
            print(resp.text)
    

    def __add_tags(self):

        if self.__info:
            tags =[]
            tags.append({"app_version":self.__info["appVersion"]})

            resp = self.hs_api.addTages_session(self.__session_id,tags)

            try:
                resp.raise_for_status()
            except:
                print("    ! Error Adding Tags")
            

        
    def get_WaterfallURL(self):
        url = "https://ui-dev.headspin.io/sessions/{}/waterfall".format(
            self.__session_id
        )

        return url
    
    def set_session_startTime(self,capture_started:float,capture_ended:float=None):
        self.__session_time["start_time"] = capture_started

        if capture_ended:
            self.__session_time["end_time"] = capture_ended

    def set_sessionId(self,session_id:str):
        self.__session_id = session_id

    def set_testName(self,test_name:str):
        self.__test_name = test_name

    def set_info(self,info:dict):
        self.__info = info
    
    def set_testStatus(self,test_status:str ,failedReason:str=None):
        self.__test_status = test_status.strip().capitalize()

        if failedReason:
            self.__failed_reason = failedReason
        else:
            self.__failed_reason = None
    
    def set_kpis(self,kpis:dict):
        self.__kpis = kpis

    def process(self):
        if self.__session_id :
            print(" Waterfall URL :",self.get_WaterfallURL())
            print("\n  === Session ===")

            print("   + Adding Userflow Name")
            self.__add_userflowName()

            print("   + Adding Name & Description")
            self.__add_nameDiscription()

            self.__get_session_capture_time()
            print("   + Adding Metrics")
            self.__add_sessionKpis()

            print("   + Adding Session Tags")
            self.__add_tags()
            
            print("   + Adding Userflow Status")
            self.__add_userflowStatus()

            
            

        
   
    

