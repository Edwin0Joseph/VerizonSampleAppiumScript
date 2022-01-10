import unittest
import pprint
from appium import webdriver
from time import sleep,time



from function_lib import get_APItoken_fromWebDriverURL
from headspin import APIs
from session_lib import KPIs,Session

class AndroidTest(unittest.TestCase):
    def setUp(self):

        
        self.desired_caps = {
            "deviceName": "iPhone 8",
            "udid": "acb5cf7c2b23ea2e484d6f34a3e2391160dc3b2c",
            "automationName": "XCUITest",
            "platformVersion": "15.0",
            "platformName": "iOS",
            "bundleId": "com.apple.Preferences"
        }

        # arguments
        self.url =        # Web Driver URL HERE

        # Appium Desire Capabilities (https://appium.io/docs/en/writing-running-appium/caps/)
        self.desired_caps["newCommandTimeout"] = 180

        test_name = "myVerizonSignin"
        print("\n    Test Name:",test_name)        

        # Test iOS APP
        self.app_name = "MyVerizon"
        # self.desired_caps["bundleId"] = "com.vzw.hss.myverizon"
        self.desired_caps["bundleId"] = "com.vzw.enterprise.MVM"


        api_token = get_APItoken_fromWebDriverURL(self.url)

        self.hs_apis = APIs(api_token)


        self.capture = True             # Start Capture
        network_capture = False         # Capture With Network: True | Capture Without Network: False

        if self.capture:
            if network_capture:
                # HEADSPIN Capabilities (https://ui-dev.headspin.io/docs/appium-capabilities)
                self.desired_caps["headspin:capture"] = True # Capture Video,Network
                # self.desired_caps["headspin:capture.video"] = True
                # self.desired_caps["headspin:capture.network"] = True
            else:
                # HEADSPIN Capabilities (https://ui-dev.headspin.io/docs/appium-capabilities)
                self.desired_caps["headspin:capture.video"] = True
                self.desired_caps["headspin:capture.network"] = False
            
        self.implicitly_wait_time = 60

        print("WEB DRIVER URL:",self.url)
        print(" ===== CAPABILITIES ========")
        pprint.pprint(self.desired_caps)
        print(" ===========================")
        
        print("\n[+] Connecting..\r",end="")
        self.driver = webdriver.Remote(self.url,self.desired_caps)
        print("[+] Connected Device: {}\r".format(self.desired_caps["udid"]))


        self.driver.execute_script(
                "mobile:terminateApp",
                {"bundleId":self.desired_caps["bundleId"]
                }
                )
        # self.driver.close_app()

        info = {}
        info["appName"] = self.app_name
        info["appVersion"] = self.__getAppVersion(self.desired_caps["udid"],self.desired_caps["bundleId"])

        self.session_kpi = KPIs()
        self.session = Session(api_token)

        self.session.set_testName(test_name)
        self.session.set_info(info)
        self.session.set_kpis(self.session_kpi.get_kpis())
        
       
    def tearDown(self):
        print("    Status:",self.status)

        if self.status == "Passed":
            self.session.set_testStatus("Passed")
        else:
            self.session.set_testStatus("Failed",failedReason=self.status)


        if self.capture:
            try:
                session_id = self.driver.session_id
                self.session.set_sessionId(session_id)
                # print("   Waterfall Session Link: https://ui-dev.headspin.io/sessions/{}/waterfall".format(session_id))
            except:
                print("    ! Failed to get Driver Session Id")        
        
        try:
            self.driver.quit()
        except:
            print("    ! Failed to Quit Driver")

        self.session.process()
    

        
    def test_app(self):
        self.driver.implicitly_wait(self.implicitly_wait_time)

        # sleep(4)       

        self.check_appLaunched()
        self.app_signin()
        self.app_signout()        

        self.status = "Passed"


    # Check App Launch    
    def check_appLaunched(self):
        self.status = "Failed_check_app_launched"

        print("[+] Launching {} app ...".format(self.app_name))
        start_time = time()
        self.driver.launch_app()

        self.driver.find_element_by_ios_predicate(
            "type==\"XCUIElementTypeButton\" AND name==\"I'm a customer\"")
        end_time = time()     
        print("[+] App Launched")
        self.session_kpi.add_kpi(
            "Launch_time",
            ts_start=start_time,
            ts_end=end_time,
            label_type="page-load-request")

    # App Sign In 
    def app_signin(self):
        self.status = "Failed_app_signin"


        sleep(4)

        customer_signin_btn = self.driver.find_element_by_ios_predicate(
            "type==\"XCUIElementTypeButton\" AND name==\"I'm a customer\"")
        # customer_signin_btn = self.driver.find_element_by_ios_predicate(
        #     "type==\"XCUIElementTypeButton\" AND name==\"Different user\"")
        customer_signin_btn.click()
        print("[+] Clicked 'I'm a customer'")

        sleep(8)


        #####  Account Login credentials ####

        username=         # PhoneNo. or username
        password=         # Password
        
        ####################################


        userField = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeTextField" AND name=="User ID or Verizon mobile number"')
        userField.click()
        userField.clear()
        userField.send_keys(username)
        print("[+] Username Entered")

        passwordField = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeSecureTextField" AND name=="Password"')
        passwordField.click()
        passwordField.clear()
        passwordField.send_keys(password)
        print("[+] Password Entered")


        signin_btn = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeButton" AND name=="Sign in"')

        sleep(4)

        start_time = time()
        signin_btn.click()
        print("[+] Clicked Signin")


        searchField = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeTextField" AND value=="What are you looking for?"')

        end_time = time()

        print("[+] App Signin:")
        self.session_kpi.add_kpi(
            "Signin_time",
            ts_start=start_time,
            ts_end=end_time + 0.600,
            label_type="page-load-request",
            options={"end_sensitivity": 1})
    

    # App Sign Out
    def app_signout(self):
        self.status = "Failed_app_signout"


        sleep(5)

        more_btn = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeButton" AND name=="More"')
        more_btn.click()
        print("[+] Clicked More")

        self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeStaticText" AND name=="Add-ons & Apps"')

        
        self.driver.swipe(183,351,183,211,800)
        print("[+] Swiped down")
        sleep(3)


        signout_btn = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeButton" AND name=="Sign Out"')
        signout_btn.click()
        print("[+] Clicked Sign Out")


        sleep(5)

        signoutAlert = self.driver.find_element_by_ios_predicate(
            'type=="XCUIElementTypeAlert" AND name=="Sign out"')

        signout = signoutAlert.find_element_by_ios_predicate(
                'type=="XCUIElementTypeButton" AND name=="Sign out"')
        signout.click()
        print("[+] Clicked (Alert) Sign out")


        self.driver.find_element_by_ios_predicate(
            "type==\"XCUIElementTypeButton\" AND name==\"I'm a customer\"")
        print("[+] App Sign out Successfully")



    def __getAppVersion(self,device_id:str,bundelId):       
        
        resp = self.hs_apis.listAllApps_iosIdevice(device_id)
        resp.raise_for_status()

        r = resp.json()["data"]
        del resp

        for iosAppDate in r:

            if iosAppDate["CFBundleIdentifier"] == bundelId:
                return iosAppDate["CFBundleShortVersionString"]

        print("    Error App not Found")        
        return None
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
