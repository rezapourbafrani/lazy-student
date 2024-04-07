import sched

import utils
import threading
import chatAnalyst
import taskRunner
import winsound
from time import sleep, time
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import multiprocessing as mp
from playsound import playsound

global driver
# TODO Reza
# url = "https://demo.bigbluebutton.org/gl/nig-gbg-lty-dlq"
# TODO Saeed
test_flag = False

###########################################################
url = "https://demo.bigbluebutton.org/gl/sae-9zj-auc-yqe"
driver_address = ""
robot_time = 0


###########################################################
# TODO delete after check task runner
# driver_address = utils.os_recognizer()
# driver = webdriver.Chrome(driver_address)
# driver_address = utils.os_recognizer()
# driver = webdriver.Chrome(driver_address)
# driver.maximize_window()
# driver.execute_script("window.open()")
# driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL + "t")

# ----------------------------------------------------------------------------------------login

class Login:
    def __init__(self, user, driver):
        print("login start")
        # TODO for auto robot switch tab
        # tab = driver.window_handles[5]
        # driver.switch_to.window(tab)
        driver.get(url)
        sleep(2)
        # try:
        # TODO this 3 line is for test.bigblue not demo.bigblue
        # driver.find_element_by_xpath(".//input[@id='username']").send_keys("ali")
        # sleep(1)
        # driver.find_element_by_xpath(".//input[@class='submit_btn button success large']").click()

        name_element = WebDriverWait(driver, 30) \
            .until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/input[4]')))
        name_element.clear()
        name_element.send_keys(user)
        # driver.find_element_by_xpath("").clear()
        # driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/input[4]").send_keys(user)
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[2]/form/div/span/button").click()
        headphone_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/span/button[2]/span[1]')))
        headphone_element.click()
        # driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div/span/button[2]/span[1]").click()


# --------------------------------------------------------------------------------------- service
num = 0
e = taskRunner.BackService()


def ruun():
    global num
    num += 2
    print(num)
    e.showState()
    if num == 4:
        exit()
        # e.stop()
        # e.close(e)


if __name__ == "__main__":
    e.setup(2, ruun)
    # t = threading.Thread(target=e.run)
    e.showState()
    print("log")
    e.run()
    # t.start()
    # e.stop()
    # t.join()


# TODO delete after check task runner
def auto_user_chat(driver):
    read_thread = threading.Thread(target=chatAnalyst.read_and_answer_chat_box(driver), args=(1,))
    try:
        read_thread.start()
    except Exception as e:
        print("fuck this" + str(e))
        read_thread.start()
    change_detector_thread = threading.Thread(target=utils.change_detector(driver).start(), args=(2,))
    try:
        change_detector_thread.start()
    except Exception as e:
        print("fuck that" + str(e))
        change_detector_thread.start()
