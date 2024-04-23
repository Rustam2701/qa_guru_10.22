import pytest
import allure
from dotenv import load_dotenv
from utils import allure
from appium import webdriver
from selene import browser


def pytest_addoption(parser):
    parser.addoption("--context", action="store", default="emulator_local",
                     help="Context for load options")


def pytest_configure(config):
    context = config.getoption("--context")
    env_file = f'.env.{context}'
    load_dotenv(dotenv_path=env_file)


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    from config import config_app
    context = request.config.getoption("--context")
    with allure.step('Set options'):
        options = config_app.to_driver_options(context=context)
        browser.config.driver = webdriver.Remote(config_app.REMOTE_URL, options=options)
        browser.config.timeout = config_app.TIMEOUT

    yield

    with allure.step('Add screenshot'):
        allure.add_screenshot(browser)

    if context == 'bstack':
        with allure.step('Add video'):
            allure.add_video(browser)

    with allure.step('Close driver'):
        browser.quit()
