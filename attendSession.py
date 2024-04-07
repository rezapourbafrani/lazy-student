import logging
import xpathes
import taskRunner
import chatAnalyst
from time import sleep
import multiprocessing as mp
from selenium import webdriver
from playsound import playsound
from utils import os_recognizer, TodayClasses, show_progressbar,find_class

###########################################################

"""
--------check internet 
--------today_classes -----find session
--------login session -----change_detector,in_class
--------logout        ----- repeat :)

in Task Runner :

     {   
         today_classes  is True until find class = False       ->   login = True
         login     ->   is True and after login  = False       ->   change_detector,**in_class**   = True
         logout    ->   is False and after end session = True  ->   today_classes = True 
         change_detector

         *in class : 
         {  chat_listener  -> read and answer chat box
            poll           -> answer poll if find
            voice          -> check master voice
         }  

     }   



"""
# -----------------------------------------------------init

driver = ""
driver_address = ""
url = "https://el.ardakan.ac.ir/login/index.php"
find_class_task = taskRunner.BackService()


# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
#
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get("https://www.python.org")
# print(driver.title)
# driver.quit()


###########################################################
class Login_in_main_page:
    def __init__(self, user, password, url_site):
        global driver_address
        global driver
        driver_address = os_recognizer()
        opts = webdriver.ChromeOptions()
        print("---- login started ----")
        opts.add_argument('allow-file-access-from-files')
        opts.add_argument('use-fake-device-for-media-stream')
        opts.add_argument('use-fake-ui-for-media-stream')
        driver = webdriver.Chrome(driver_address, options=opts)
        driver.maximize_window()
        driver.get(url_site)
        try:
            driver.find_element_by_name("username").send_keys(str(user))
            driver.find_element_by_name("password").send_keys(str(password))
            sleep(3)
            driver.find_element_by_class_name("loginButton").click()
            sleep(4)
            chatAnalyst.login_flag = True
            chatAnalyst.today_classes_flag = True
            xpathes.findClass_flag = True
            # in_dashboard(class_finder_obj)
            find_class(driver)
            # find_class_task.setup(120, in_dashboard, actionargs=[class_finder_obj])
            # find_class_task.run()
        except Exception as e:
            print(str(e))
            print(" internet error ")

            loop_process = mp.Process(target=playsound, args=('alarm.mp3',))
            loop_process.start()

            timer_process = mp.Process(target=sleep(1))
            timer_process.start()

            loop_process.join()
            timer_process.join()
            sleep(50)
            if not login_flag:
                del self
                Login_in_main_page(user, password, url)


# ---------------------------------------- defined for use in task_runner (search for available classes)
# def find_class(Todayclass_obj):
#     xpathes.findClass_flag = False
#     Todayclass_obj.start()
#     show_progressbar()


# ----------------------------- init flags
in_session_flag = False
change_detector_flag = False
login_flag = False
logout_flag = False
end_session_flag = False
today_classes_flag = False
new_started_class_flag = False


