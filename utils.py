import requests

import xpathes
import logging
import platform
import selenium
import taskRunner
import chatAnalyst
from time import sleep, process_time, time
import multiprocessing as mp
from playsound import playsound
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###########################################################
driver = ""
link_counter = 0
clock_webservice_address = "https://api.codebazan.ir/time-date/?td=time"
in_class_task_runner = taskRunner.BackService()
find_class_task = taskRunner.BackService()
enter_hour = -1
enter_min = -1
last_entered_class_time_check = "00:00"
current_time_check = "00:00"
teacher_finded_flag = False
master_not_found_counter = 0
class_time = "7:50"


###########################################################

# ------------------------------------------------ detect operator system
def os_recognizer():
    print("I Check your os for WebDriver ->->")
    os_name = platform.system()
    address = "driver/chromedriver.exe"

    if os_name == "Linux":
        address = "./driver/chromedriver_linux"
        print("Your os is Linux")
    elif os_name == "Windows":
        address = "driver/chromedriver.exe"
        print("Your os is Windows")
    return address


# ------------------------------------------------- show task progressbar
def show_progressbar():
    for i in range(1, 101):
        sleep(0.01)
        print("\r process is %d%%" % i, end="", flush=True)


###########################################################

# ------------------------------------------------- TimeCalender
class TimeCalender:
    dt_string = "00-00-00"

    def __init__(self):
        now = datetime.now()
        print("now =", now)
        time = now.strftime("%H-%M-{}")
        print("hour {} and min {} and sec {}".format(time[0:2], time[3:5], time[6:]))
        print("time =", time)
        # dd/mm/YY H:M:S
        self.dt_string = now.strftime("%d/%m/%Y %H:%M:{}")
        print("date and time =", self.dt_string)

    def create_date(self):
        return self.dt_string


# ----------------------------------------------- read today's plan
class TodayClasses:
    page = ""
    last_entered_class_time = ""

    def __init__(self, page=webdriver.Chrome):
        self.page = page
        self.last_entered_class_time = ""

    def start(self):
        global link_counter
        start_cpu = process_time()
        start_time = time()
        try:
            print("---- today class started ----")
            print("search again for class ->->")
            start_cpu = process_time()
            start_time = time()
            self.page.refresh()
            sleep(20)
            current_time = requests.get(clock_webservice_address).text[:5]
            current_hour = int(current_time[:2])
            current_min = int(current_time[3:5])
            links = self.page.find_elements_by_xpath(xpathes.joining_class_link)
            times = self.page.find_elements_by_xpath(xpathes.classes_time)
            link_counter = 0
            for link in reversed(links):
                global class_time
                class_time = times[link_counter].text[:5]
                self.last_entered_class_time = class_time
                # class_time = current_time[:5]
                class_time_hour = int(times[link_counter].text[:2])
                class_time_min = int(times[link_counter].text[3:5])
                real_link = link.get_attribute("href")
                print(real_link)
                print('->-> last class time : {}'.format(class_time))
                print('->-> current time : {}'.format(current_time))
                # TODO true or is for bypass if condition
                # late time for robot
                if True or current_hour == class_time_hour + 1 or \
                        (class_time_hour == current_hour and class_time_min <= current_min + 2):
                    # if times[link_counter].text[:5] != self.last_entered_class_time:
                    self.last_entered_class_time = class_time
                    global last_entered_class_time_check
                    last_entered_class_time_check = self.last_entered_class_time
                    """
                    update link problem
                    14:50     12:50  -> 2  120
                    9:50        12:50  -> 3  180 
                    """
                    if current_hour >= class_time_hour + 2:
                        last_entered_class_time_check = current_time
                        self.last_entered_class_time = current_time
                    link.click()
                    chatAnalyst.today_classes_flag = False
                    # TODO edit
                    if chatAnalyst.time_comparator(self.last_entered_class_time, current_time, 20):
                        xpathes.new_started_class_flag = True
                    print("I find your class ;)")
                    print("start class : {}  in dashboard".format(link_counter))
                    entered_to_class(self.page)
                    break
                    # else:
                    # print('its your pervious class ' + self.last_entered_class_time)
                else:
                    print("class time has been passed!")
                link_counter += 1
        except Exception as e:
            print("class finder error link counter is : {}".format(link_counter) + str(e))

            try:
                loop_process = mp.Process(target=playsound, args=('alarm.mp3',))
                loop_process.start()
                print("play alarm check internet ")

                timer_process = mp.Process(target=sleep(1))
                timer_process.start()

                loop_process.join()
                timer_process.join()
            except Exception as e:
                print("alarm error :" + str(e))
                print("alarm error in class finder")
        # print("TodayClasses start : cpu time: {} and time : {}".format(process_time() - start_cpu,
        # time() - start_time))


# ------------------------------------------------ detect changes in opened page
class ChangeDetector:
    page = ""

    def __init__(self, page=webdriver.Chrome):
        self.page = page
        xpathes.last_html_file = self.page.find_element_by_xpath(xpathes.main_body).get_attribute("innerHTML")

    def start(self):
        print("search again for anythings .........")
        print()
        # TODO time

        start_cpu = process_time()
        start_time = time()
        new_html = self.page.find_element_by_xpath(xpathes.main_body).get_attribute("innerHTML")
        # if xpathes.last_html_file != new_html:
        # if True:
        try:
            if not teacher_finded_flag:
                teacher_isnot_here(self.page)
            find_and_click_poll(self.page)
            check_audio(self.page)
            find_and_click_on_endclassbtn(self.page)
            class_time_ended(self.page)
            xpathes.last_html_file = new_html
            # print( "change detector : cpu time: {} and time : {}".format(process_time() - start_cpu,
            # time() - start_time))
        except Exception as e:
            print("change detector : " + str(e))
        # else:
        #     print("------------ no change in html body ----------------")


###########################################################

# ------------------------------------------------ In main dashboard
def in_dashboard(Todayclass_obj):
    try:
        print()
        print(" I am in Dashboard ;) ")
        if xpathes.findClass_flag:
            Todayclass_obj.start()
            show_progressbar()
        else:
            find_class_task.stop()

    except Exception as e:
        print("in dashboard" + str(e))
        logging.exception(e)
        sleep(20)
        in_dashboard(Todayclass_obj)


# ------------------------------------------------ find class task runner
def find_class(driver):
    class_finder_obj = TodayClasses(driver)
    find_class_task = taskRunner.BackService()
    find_class_task.setup(600, in_dashboard, actionargs=[class_finder_obj])
    find_class_task.run()


# ------------------------------------------------ In class task runner
def in_class_task(page, change_detector_object):
    # Get time
    start_cpu = process_time()
    start_time = time()
    current_time = requests.get(clock_webservice_address).text[:5]
    if not xpathes.findClass_flag:
        # check time for hy message
        # task start
        if chatAnalyst.time_comparator(last_entered_class_time_check, current_time, 20):
            print("say hy flag disabled")
            chatAnalyst.hi_flag = True
        read_and_answer_chat_box(page)
        change_detector_object.start()
        # print("in_class_task : cpu time: {} and time : {}".format(process_time() - start_cpu, time() - start_time))
        show_progressbar()


# -------------------------------------------- enter to class
def entered_to_class(page=webdriver.Chrome):
    print("---- I'm in class ----")
    find_headphone(page)
    # TODO why? reza
    enter_time = requests.get(clock_webservice_address).text
    global master_not_found_counter
    global teacher_finded_flag
    teacher_finded_flag = False
    master_not_found_counter = 0

    print("->-> Now reset chat_box_reader")
    chatAnalyst.reset_chat_box_reader()
    print("->-> enable change detector")
    change_detector_object = ChangeDetector(page)
    print("->-> disable find class ")
    xpathes.findClass_flag = False
    print("->-> start class tasks ")

    in_class_task_runner.setup(25, in_class_task, actionargs=[page, change_detector_object])
    in_class_task_runner.run()


# -------------------------------------------- find headphone
def find_headphone(page=webdriver.Chrome):
    print("Now search for headphone click ->->")
    start_cpu = process_time()
    start_time = time()
    # sleep(7)
    headphone_founded = False
    try:
        headphone_element = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, xpathes.headphone_btn_xpath)))
        headphone_element.click()
        sleep(1)
        headphone_element2 = WebDriverWait(page, 15).until(
            EC.presence_of_element_located((By.XPATH, xpathes.headphone_btn_xpath3)))
        headphone_element2.click()

        headphone_founded = True
        sleep(1)
    except Exception as e:
        print("headphone element not found")

    if not headphone_founded:
        try:
            headphone_element = WebDriverWait(page, 15).until(
                EC.presence_of_element_located((By.XPATH, xpathes.headphone_btn_xpath2)))
            headphone_element.click()
            sleep(1)
            headphone_element2 = WebDriverWait(page, 15).until(
                EC.presence_of_element_located((By.XPATH, xpathes.headphone_btn_xpath3)))
            headphone_element2.click()
            headphone_founded = True
            sleep(1)
        except Exception as e:
            print("headphone element not found  in body/span")

    if not headphone_founded:
        try:
            headphone_element = WebDriverWait(page, 15).until(
                EC.presence_of_element_located((By.XPATH, xpathes.headphone_btn_xpath3)))
            headphone_element.click()
            headphone_founded = True
            sleep(1)
        except Exception as e:
            print("headphone element not found")
    # print("find_headphone : cpu time: {} and time : {}".format(process_time() - start_cpu, time() - start_time))


# -------------------------------------------- check audio
def check_audio(page=webdriver.Chrome):
    print("Now check audio ->->")
    start_cpu = process_time()
    start_time = time()
    try:
        audioOff = WebDriverWait(page, 10).until(
            EC.presence_of_element_located((By.XPATH, xpathes.audioOff)))
        print("headphone is Off ")
        audioOff.click()
        find_headphone(page)
        # audio_btn = WebDriverWait(page, 15).until(
        #     EC.presence_of_element_located((By.XPATH, xpathes.audio_btn)))
        # audio_btn.click()
    except Exception as e:
        print("Headphone may be is On :| ")
        try:
            WebDriverWait(page, 10).until(
                EC.presence_of_element_located((By.XPATH, xpathes.audioON)))
            print("Everything is good headphone is On ;) ")
        except Exception as e:
            print("Check headphone error try again later ")
            print(str(e))
    # print("check_audio : cpu time: {} and time : {}".format(process_time() - start_cpu, time() - start_time))


# ------------------------------------------------ detect poll is in page
def find_and_click_poll(page=webdriver.Chrome):
    print("Now found poll ->->")
    start_cpu = process_time()
    start_time = time()
    try:
        poll = page.find_element_by_xpath(xpath=xpathes.yes_button_xpath)
        print("->-> I'm found poll just click ")
        try:
            loop_process = mp.Process(target=playsound, args=('alarm.mp3',))
            loop_process.start()
            print("->-> play alarm check internet ")

            timer_process = mp.Process(target=sleep(1))
            timer_process.start()
            print("->-> play alarm 3 second ")

            loop_process.join()
            timer_process.join()
        except Exception as e:
            print("alarm error :" + str(e))
            print("alarm error in class finder")
        # TODO after test enable      attention !!!!!!!
        poll.click()
    except Exception:
        print("->-> poll not found")
    # print("find_and_click_poll : cpu time: {} and time : {}".format(process_time() - start_cpu, time() - start_time))


# TODO saeed test
# -------------------------------------------- check presenter
def teacher_isnot_here(page=webdriver.Chrome):
    print("check master presenter ->->")
    start_cpu = process_time()
    start_time = time()
    time_now = requests.get(clock_webservice_address).text
    try:
        if chatAnalyst.time_comparator(last_entered_class_time_check, time_now[:5], 30):
            try:
                master_element = page.find_element_by_xpath(xpathes.master_xpath)
                print("master is here ")
            except Exception as e:
                print("master is not here ")
                print(str(e))
                global master_not_found_counter
                print("master is not here counter is : {}".format(master_not_found_counter))
                master_not_found_counter += 1
                if master_not_found_counter > 5:
                    print("->-> end session and wait for another session")
                    end_class_without_btn(page)
    except Exception as e:
        print("time comparator not work !!")
        print(str(e))
    # print("teacher_isnot_here : cpu time: {} and time : {}".format(process_time() - start_cpu, time() - start_time))
    # TODO reza
    #################################################################
    # if enter_min > 29 and now_min <= 10:
    #     try:
    #         teacher_element = page.find_element_by_xpath(xpathes.teacher_xpath)
    #         print("master 1------------------------")
    #         end_class_without_btn(page)
    #
    #     except Exception as e:
    #         print('teacher is talking bullshit')
    #         teacher_finded_flag = True
    #
    # elif now_min >= enter_min + 30:
    #     try:
    #         teacher_element = page.find_element_by_xpath(xpathes.teacher_xpath)
    #         print("master 2------------------------")
    #         end_class_without_btn(page)
    #     except Exception as e:
    #         print('teacher is talking bullshit')
    #         teacher_finded_flag = True


# TODO saeed test
# -------------------------------------------- read and answer chat
def read_and_answer_chat_box(inside_driver=selenium.webdriver.chrome.webdriver.WebDriver):
    print("Now check chat box and answer ->->")
    start_cpu = process_time()
    start_time = time()
    time_now = requests.get(clock_webservice_address).text
    print("current time : {}".format(str(time_now[:5])))
    try:
        text = chatAnalyst.read_and_answer_chat_box(inside_driver)
        if text != "null":
            print("->-> warning warning response is coming : {}".format(text))
            # TODO after test enable      attention !!!!!!!
            print("wow wow response is ok : {}".format(text))
            # inside_driver.find_element_by_xpath(xpathes.chat_input).send_keys(text)
            # sleep(5)
    #         inside_driver.find_element_by_xpath(xpathes.chat_send_btn).click()
    #         print("I send message to class :)")
    except Exception as e:
        logging.exception(e)
        print("error when read chat box or analyst" + str(e))

    # print( "read_and_answer_chat_box : cpu time: {} and time : {}".format(process_time() - start_cpu,
    # time() - start_time))


# -------------------------------------------- end of class normal
def end_session(page=webdriver.Chrome, end_classbtn=webdriver.Chrome.find_element_by_xpath):
    print("Class ended by master")
    print("->-> Now reset chat_box_reader")
    chatAnalyst.reset_chat_box_reader()
    try:
        in_class_task_runner.stop()
    except Exception:
        print("in_class_task_runner doesn't exist ! :|  ")

    print("->-> enable find class ")
    xpathes.findClass_flag = True
    end_classbtn.click()
    find_class(page)


# -------------------------------------------- check class time end
def class_time_ended(page=webdriver.Chrome):
    print("I'm check time for end session ->->")
    start_cpu = process_time()
    start_time = time()
    time_now = requests.get(clock_webservice_address).text
    """
        after 1:45 start time class close class
        9:50
        11:45    close that
        
        
        7:50 - 9:30
        12:50 (7:50)- 14:30    14:45 close classes
        after 3h don't close class        
    
    """
    try:
        if chatAnalyst.time_comparator(last_entered_class_time_check, time_now[:5], 110):
            if chatAnalyst.time_comparator(last_entered_class_time_check, time_now[:5], 175):
                print("This is next class everything is Ok ")
            else:
                try:
                    master_element = page.find_element_by_xpath(xpathes.master_xpath)
                except Exception as e:
                    print("master is not here ")
                    print("->-> end session and wait for another session")
                    end_class_without_btn(page)

    except Exception as e:
        print("time comparator not work !!")
        print(str(e))
    # print("class_time_ended : cpu time: {} and time : {}".format(process_time() - start_cpu, time() - start_time))
    # 10:34
    # 10:08
    # if enter_min < 10:
    #     if now_hour >= enter_hour + 1 and now_min >= enter_min + 50:
    #         print("end enter_min < 10")
    #         end_class_without_btn(page)
    # else:
    #     if now_hour >= enter_hour + 2 and now_min >= enter_min - 10:
    #         print("end else enter_min < 10")
    #         end_class_without_btn(page)


# -----------------------------------------  click on end class button

def end_class_without_btn(page=webdriver.Chrome):
    print("class ended by time or teacher not founded ->->")
    print("->-> Now reset chat_box_reader")
    chatAnalyst.reset_chat_box_reader()
    try:
        in_class_task_runner.stop()
    except Exception:
        print("in_class_task_runner doesn't exist ! :|  ")

    print("->-> enable find class ")
    xpathes.findClass_flag = True
    page.back()
    sleep(3)
    find_class(page)


# ----------------------------------------- find and click on end class button

def find_and_click_on_endclassbtn(page=webdriver.Chrome):
    print("Now check end session btn ->->")
    start_cpu = process_time()
    start_time = time()
    time_now = requests.get(clock_webservice_address).text
    print("find end = {}".format(last_entered_class_time_check))
    try:
        if chatAnalyst.time_comparator(last_entered_class_time_check, time_now[:5], 105):
            print("Now find end session btn ->->")
            try:
                end_class_btn = WebDriverWait(page, 15).until(
                    EC.presence_of_element_located((By.XPATH, xpathes.end_class_btn_xpath)))
                end_session(page, end_class_btn)
            except Exception as e:
                print("class not ended id not found  4-div" + str(e))
                try:
                    end_class_btn = WebDriverWait(page, 15).until(
                        EC.presence_of_element_located((By.XPATH, xpathes.end_class_btn_xpath2)))
                    end_session(page, end_class_btn)
                except Exception as e:
                    print("class not ended button isn't in body  5-div" + str(e))
                    try:
                        end_class_btn = WebDriverWait(page, 15).until(
                            EC.presence_of_element_located((By.XPATH, xpathes.end_class_btn_xpath3)))
                        end_session(page, end_class_btn)
                    except Exception as e:
                        print("class not ended yet id not found  3-div" + str(e))
                        try:
                            end_class_btn = WebDriverWait(page, 15).until(
                                EC.presence_of_element_located((By.XPATH, xpathes.end_class_btn_xpath4)))
                            end_session(page, end_class_btn)
                        except Exception as e:
                            print("class not ended yet button isn't in body  4-div" + str(e))
    except Exception as e:
        print("time comparator not work !!")
        print(str(e))
    # print("find_and_click_on_endclassbtn : cpu time: {} and time : {}".format(process_time() - start_cpu,
    #                                                                           time() - start_time))
