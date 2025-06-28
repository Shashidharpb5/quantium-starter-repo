import pytest
import threading
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import app  # your main Dash app file

@pytest.fixture(scope="module")
def test_server():
    # Start the Dash app in a separate thread
    thread = threading.Thread(target=app.app.run, kwargs={"debug": False, "use_reloader": False})
    thread.daemon = True
    thread.start()
    # Wait for the server to come up
    timeout = 10
    url = "http://127.0.0.1:8050"
    while timeout:
        try:
            requests.get(url)
            break
        except:
            time.sleep(1)
            timeout -= 1
    yield url
    # No teardown needed, app will stop when test ends


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()


def test_header_present(test_server, driver):
    driver.get(test_server)
    header = driver.find_element(By.TAG_NAME, "h1")
    assert "Quantium Pink Morsel Sales Analysis" in header.text


def test_graph_present(test_server, driver):
    driver.get(test_server)
    graph = driver.find_element(By.ID, "sales-graph")
    assert graph is not None


def test_region_picker_present(test_server, driver):
    driver.get(test_server)
    radio = driver.find_element(By.ID, "region-radio")
    assert radio is not None
