import time
import unittest
import sys

import pytest
import xmlrunner
import HtmlTestRunner
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


def error_message():
    print("Element not available")


class ChallengeStoriAutomation(unittest.TestCase):
    # @pytest.fixture(params=["firefox", "chrome"], scope="class")
    def setUp(self):
        # browser = request.param
        #match browser:
        #    case "firefox":
        #        self.driver = webdriver.Firefox(executable_path="C://Selenium/geckodriver.exe")
        #        self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        #        self.driver.maximize_window()
        #    case "chrome":
        #        self.driver = webdriver.Chrome(executable_path="C://Selenium/chromedriver.exe")
        #        self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        #        self.driver.maximize_window()
        #    case _:
        #        print("Browser not available. Try other instead")
        self.driver = webdriver.Chrome(executable_path="C://Selenium/chromedriver.exe")
        self.driver.get("https://rahulshettyacademy.com/AutomationPractice/")
        self.driver.maximize_window()

    def test_suggestion_class(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            driver.find_element(By.XPATH, "//input[@id='autocomplete']").send_keys("Me")
            WebDriverWait(driver, 50).until(ec.visibility_of_element_located((By.XPATH, "//ul[@id='ui-id-1']")))
            driver.find_element(By.XPATH, "//div[contains(text(), 'Mexico')]").click()
        except TimeoutException:
            error_message()

    def test_dropdown_class(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            options = Select(driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/fieldset/select"))
            for i in range(2, 4):
                options.select_by_index(i)
                time.sleep(4)
        except TimeoutException:
            error_message()

    def test_switch_window(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            driver.find_element(By.XPATH, "//button[@id='openwindow']").click()
            main_page = driver.current_window_handle
            new_window = 0
            for i in driver.window_handles:
                new_window = i
            driver.switch_to.window(new_window)
            popup = WebDriverWait(driver, 20).until(
                ec.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'NO THANKS')]")))
            popup.click()
            assert driver.find_element(By.XPATH,
                                       "/html/body/section[@id='welcome']//h3[contains(text(), 'Money Back')]").is_displayed()
            driver.close()
            driver.switch_to.window(main_page)
        except TimeoutException:
            error_message()

    def test_switch_tab(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            driver.find_element(By.XPATH, "//fieldset/a[@id='opentab']").click()
            main_tab = driver.current_window_handle
            child_tab = driver.window_handles[1]
            driver.switch_to.window(child_tab)
            all_courses_button = driver.find_element(By.CSS_SELECTOR, ".view-all-courses-btn")
            actions = ActionChains(driver)
            actions.move_to_element(all_courses_button).perform()
            time.sleep(2)
            driver.save_screenshot("test_switch_tab.png")
            driver.switch_to.window(main_tab)
        except TimeoutException:
            error_message()

    def test_switch_to_alert(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            text_box = driver.find_element(By.XPATH, "//input[@id='name']")
            text_box.send_keys("Stori Card")
            driver.find_element(By.CSS_SELECTOR, "#alertbtn").click()
            alert = Alert(driver)
            print(alert.text)
            alert.accept()

            text_box.send_keys("Stori Card")
            driver.find_element(By.CSS_SELECTOR, "#confirmbtn").click()
            confirm = Alert(driver)
            print(confirm.text)
            assert confirm.text == "Hello Stori Card, Are you sure you want to confirm?"
            confirm.accept()
        except TimeoutException:
            error_message()

    def test_web_table(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            list_of_courses = driver.find_elements(By.CSS_SELECTOR, ".table-display>tbody>tr>td:nth-of-type(3)")
            courses = []
            for i in list_of_courses:
                if i.text == "25":
                    position = str(list_of_courses.index(i) + 2)
                    courses.append(driver.find_element(By.CSS_SELECTOR,
                                                       ".table-display>tbody>tr:nth-child(" + position + ")>td:nth-of-type(2)").text)
            print("$25 courses are: " + str(courses))

        except TimeoutException:
            error_message()

    def test_web_table_fixed(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            list_of_careers = driver.find_elements(By.CSS_SELECTOR, ".tableFixHead>table>tbody>tr>td:nth-of-type(2)")
            engineers = []
            for i in list_of_careers:
                if i.text == "Engineer":
                    position = str(list_of_careers.index(i) + 1)
                    engineers.append(driver.find_element(By.CSS_SELECTOR,
                                                         ".tableFixHead>table>tbody>tr:nth-child(" + position + ")>td:nth-of-type(1)").text)
            print("Engineers: " + str(engineers))
        except TimeoutException:
            error_message()

    def test_iframe(self):
        driver = self.driver
        try:
            WebDriverWait(driver, 10).until(ec.visibility_of_all_elements_located)
            driver.switch_to.frame("courses-iframe")
            text = driver.find_element(By.XPATH, "/html/body/div/div[2]/section[4]/div/div/div/div[2]/ul/li[2]").text
            print(text)
        except TimeoutException:
            error_message()


if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="Report"))
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output="Report"))
