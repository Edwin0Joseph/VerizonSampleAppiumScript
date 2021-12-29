package io.headspin.tests;

import io.appium.java_client.MobileElement;
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.remote.MobileCapabilityType;
import org.openqa.selenium.By;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.SessionId;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.Reporter;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.TimeUnit;

//@Listeners({ExtentITestListenerClassAdapter.class})
public class Example extends ExtentBase {
    public static URL url;
    public static DesiredCapabilities capabilities;
    public static AndroidDriver<MobileElement> driver;

    @BeforeClass(alwaysRun = true)
    public void setUp() throws MalformedURLException {
        System.out.println("SETUP");
        url = new URL("https://us-mv.headspin.io:3018/v0/<Token Here>/wd/hub");
        capabilities = new DesiredCapabilities();
        capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, "Pixel");
        capabilities.setCapability(MobileCapabilityType.UDID, "FA6AF0300712");
        capabilities.setCapability(MobileCapabilityType.AUTOMATION_NAME, "UiAutomator2");
        capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
        capabilities.setCapability("appPackage", "com.android.settings");
        capabilities.setCapability("appActivity", "com.android.settings.Settings");
    }

    @Test(groups = {"a:AJ", "d:android", "t:tag", "example"})
    public void launchSettingsApp() {
        System.out.println("Launching settings app");
        driver = new AndroidDriver<>(url, capabilities);
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);


        SessionId sessionId = driver.getSessionId();


        WebDriverWait wait = new WebDriverWait(driver, 15);
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("com.android.settings:id/settings_homepage_container")));

        Reporter.log("Session URL: https://ui-dev.headspin.io/sessions/" + sessionId.toString() + "/waterfall");

    }


    @AfterClass
    public void tearDown() {
        System.out.println("TEARDOWN");
        try {
            driver.quit();
        } catch (Exception e) {
            System.out.println("Failed to quit driver");
            e.printStackTrace();
        }
    }

}