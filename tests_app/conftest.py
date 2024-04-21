import pytest
from appium.options.android import UiAutomator2Options
from selene import browser
import os
from dotenv import load_dotenv
from appium import webdriver
import allure

from action_of_selene import utils

load_dotenv()
USERNAME = os.getenv('USER_NAME')
ACCESSKEY = os.getenv('ACCESS_KEY')


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test",

            # Set your access credentials
            "userName": USERNAME,
            "accessKey": ACCESSKEY
        }
    })

    browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub', options=options)
    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG,
    )

    allure.attach(
        browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils.allure.attach_bstack_video(session_id)