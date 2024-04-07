import logging
import selenium
import requests

import xpathes

from datetime import datetime
from selenium import webdriver
from time import sleep, process_time, time

"""
join session start=0
 check message in message list
if Controlled -> say Controlled message by @function controlled answer
else Uncontrolled -> say Uncontrolled by @function uncontrolled answer

if new_started_class_flag == True:
    chatAnalyst disable 

"""
# TODO Saeed
clock_webservice_address = "https://api.codebazan.ir/time-date/?td=time"
###########################################################
driver_address = ""
response_answer = "null"
robot_answer_controlled = [["first", "0:00"]]
robot_answer_uncontrolled = [["first", "0:00"]]
temp_answer_uncontrolled = [["first", "0:00", 0]]
temp_answer_controlled = [["first", "0:00", 0]]
# ------------------------------Controlled message
say_yes = "بله"
say_no = "نه"
say_nothing = "null"
answer = say_nothing
say_hi = "سلام"
say_goodbye = "خسته"
say_bye = "خسته نباشید استاد"
# -----------------------------Controlled counter
max_repeat = 4
between_time = 7
hi_counter = 0
bye_counter = 0
yes_counter = 0
no_counter = 0
message_counter = 0
# -----------------------Flag Controlled just Once
hi_flag = False
bye_Flag = False
# ----------------------------------start and end
start = 1
end = 0
# -------------------------get data from chat box
user_count = 0
username = "admin"
time_send = "00:00"


###########################################################

# -----------------------------------------Controlled Answer

def controlled_answer(input_message, count, time):
    # ---------------------------------global variable
    global hi_flag
    global bye_Flag
    global yes_counter
    global no_counter
    global hi_counter
    global bye_counter
    global response_answer
    global robot_answer_controlled
    global temp_answer_controlled
    # ---------------------------------------------- online time
    time_now = datetime.now().strftime("%H:%M")
    # ("%H-%M-%p") # AM PM
    # time_now = requests.get(clock_webservice_address).text[:5]
    # --------------------------------------system time , send time , counter
    length = len(robot_answer_controlled)
    temp_answer_controlled.append([input_message, time, count])
    tempLength = len(temp_answer_controlled)
    response_answer = say_nothing
    # --------------------------------------robot matrix answer
    ########################################################
    print("****************** robot_answer_controlled *********************")
    print("length is : {}".format(length))
    for row in robot_answer_controlled:
        for i in row:
            print(i, end="  ")
        print()
    print("** end **")
    print()
    ########################################################
    ########################################################
    print("****************** temp_answer_controlled *********************")
    print("length is : {}".format(tempLength))
    for row in temp_answer_controlled:
        for i in row:
            print(i, end="  ")
        print()
    print("** end **")
    print()
    ########################################################
    # --------------------------------------robot matrix temp answer

    if count >= max_repeat:
        print()
        # print("================================================================= ok count >= 5")
        print("---------- controlled message : {} and counter : {}  time : {} now :{}---------".format(input_message,
                                                                                                       count, time,
                                                                                                       time_now))
        if input_message == say_hi:
            hi_counter = 0
            count = hi_counter
            if hi_flag:
                hi_counter = 0
                print("i say hi")
                return say_nothing
            hi_flag = True
        elif input_message == say_yes:
            yes_counter = 0
            count = yes_counter
        elif input_message == say_goodbye:
            bye_counter = 0
            count = bye_counter
            if bye_Flag:
                print("i say bye")
                return say_nothing
            bye_Flag = True
        elif input_message == say_no:
            no_counter = 0
            count = no_counter

        # length = len(robot_answer_controlled)
        # Get last message time for compare
        get_last_time = robot_answer_controlled[-1][1]
        # check verify and send answer
        getFirstIndexMessage = verify_message(temp_answer_controlled, input_message)
        # if counter 1 not found
        if getFirstIndexMessage == -1:
            print(" first  message not found !!")
            getFirstIndexMessage = 0
        # get first time
        getFirstIndexTime = temp_answer_controlled[getFirstIndexMessage][1]
        # reset temp
        temp_answer_controlled = [["first", "0:00", 0]]

        # check last controlled answer by new input message
        if robot_answer_controlled[-1][0] != input_message:
            print("1-message compare != last message")
            print(
                "first message  time : {}  and system time : {} ".format(getFirstIndexTime
                                                                         , time_now))
            if not time_comparator(getFirstIndexTime, time_now, between_time):
                print("2-between time passed")
                response_answer = input_message
                # hi and bye just once and don't need to add in robot_answer_controlled
                if input_message != say_hi and input_message != say_goodbye:
                    robot_answer_controlled.append([input_message, time])

                    print("============= 1-controlled_answer is : {}  and counter is : {}".format(response_answer,
                                                                                                  count))
                    print()
                    print("============= last message is : {}  and time is : {} --- last message != new message"
                          .format(robot_answer_controlled[-1][0], get_last_time))
                    print()
                    print(
                        "================================================================= Controlled response")
                if response_answer == say_goodbye:
                    return say_bye
            return response_answer
        # last answer message ==  input message check time -> 10 min between two answer
        elif time_comparator(get_last_time, time_now, 10):
            print("3-message compare == last message")
            if not time_comparator(getFirstIndexTime, time_now, between_time):
                print("4-between time passed")
                response_answer = input_message
                if input_message != say_hi and input_message != say_goodbye:
                    robot_answer_controlled.append([input_message, time])
                    print("============= 2-controlled_answer is : {}  and counter is : {}".format(response_answer,
                                                                                                  count))
                    print()
                    print("============= last message is : {}  and time is : {} --- last message == new message"
                          .format(robot_answer_controlled[-1][0], get_last_time))
                    print()
                    print(
                        "================================================================= Controlled response")
                if response_answer == say_goodbye:
                    return say_bye
                return response_answer
    return say_nothing


# ----------------------------------------Uncontrolled Answer

def uncontrolled_answer(input_message, time):
    global message_counter
    global response_answer
    global robot_answer_uncontrolled
    global temp_answer_uncontrolled
    # ---------------------------------------------- online time
    now = datetime.now()
    time_now = now.strftime("%H-%M")
    # time_now = requests.get(clock_webservice_address).text[:5]
    response_answer = say_nothing
    # first message
    message_counter = 1
    length_temp = len(temp_answer_uncontrolled)
    length = len(robot_answer_uncontrolled)

    # --------------------------------------robot matrix answer

    # ----------------------------------------------show robot_answer_uncontrolled
    #######################################################
    print("****************** robot_answer_uncontrolled   *********************")
    print("length is : {}".format(length))
    for row in robot_answer_uncontrolled:
        for i in row:
            print(i, end="  ")
        print()
    print("** end **")
    print()
    ########################################################

    # -------------------------find last time and count message

    for i in range(0, length_temp):
        if temp_answer_uncontrolled[i][0] == input_message:
            message_counter += 1
    # add message to temp by time and counter
    temp_answer_uncontrolled.append([input_message, time, message_counter])
    # ----------------------------------------------show temp_answer_uncontrolled
    #######################################################
    print("****************** temp_answer_uncontrolled uncontrolled message  *********************")
    print("length is : {}".format(length_temp))
    for row in temp_answer_uncontrolled:
        for i in row:
            print(i, end="  ")
        print()
    print("** end **")
    print()
    #######################################################
    # check count new uncontrolled message
    if message_counter >= max_repeat:

        print("============= uncontrolled_input  is : {}  and counter is : {} time : {} now : {}".format(input_message,
                                                                                                         message_counter
                                                                                                         , time
                                                                                                         , time_now))
        # reset counter first
        message_counter = 1
        # last answer
        length = len(robot_answer_uncontrolled)
        get_last_time = robot_answer_uncontrolled[-1][1]
        # get last message index
        getFirstIndexMessage = verify_message(temp_answer_uncontrolled, input_message)
        if getFirstIndexMessage == -1:
            getFirstIndexMessage = 0
        getFirstIndexTime = temp_answer_uncontrolled[getFirstIndexMessage][1]
        temp_answer_uncontrolled = [["first", "0:00", 0]]
        print("first message time : {}  and system time : {} ".format(getFirstIndexTime
                                                                      , time_now))

        if not time_comparator(getFirstIndexTime, time_now, between_time):
            print("last time : {}   sys_time : {}".format(get_last_time, time_now))
            # check time between last answer and new
            if time_comparator(get_last_time, time_now, 10):
                robot_answer_uncontrolled.append([input_message, time])
                response_answer = input_message
                print("============== 2-uncontrolled_answer is : {} and counter is {} ".format(response_answer,
                                                                                               message_counter))
                print()
                print("============= last message is : {}  and time is : {} "
                      .format(robot_answer_uncontrolled[-1][0], get_last_time))
                return response_answer
    return say_nothing


# ----------------------------------------time_comparator

def time_comparator(last_time, system_time, com_number):
    # -----------------------------convert last & system time to integer

    com_number = int(com_number)
    com_h = 0
    com_m = 0
    # Fn version
    # '8:03' or '12:55'
    if len(last_time) == 4:
        try:
            last_h = int(last_time[0:1])
            last_m = int(last_time[2:])
        except:
            last_h = int(last_time[0:1])
            last_m = int(last_time[3:])

    elif len(last_time) <= 4:
        last_h = int(last_time[0:1])
        last_m = int(last_time[2:4])
    elif len(last_time) <= 5:
        last_h = int(last_time[0:2])
        last_m = int(last_time[3:5])

    # En version
    # '8:03 AM' or '12:55 PM'
    # 03-23-AM
    elif len(last_time) >= 8:
        last_h = int(last_time[0:2])
        last_m = int(last_time[3:5])
        if last_time[5:] == "AM":
            last_h += 12
    else:
        last_h = int(last_time[0:1])
        last_m = int(last_time[2:4])
        if last_time[5:] == "PM":
            last_h += 12

    sys_h = int(system_time[0:2])
    sys_m = int(system_time[3:5])

    # convert com to time
    com_h = int(com_number / 60)
    com_m = int(com_number - (com_h * 60))
    # add to last time
    last_h += com_h
    last_m += com_m
    # 118 -> 59
    if last_m >= 60:
        last_h += 1
        last_m -= 60

    # TODO time detail
    # print()
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print("sys_h : {} sys_m : {}".format(str(sys_h), str(sys_m)))
    # print("last_h : {} last_m : {}".format(str(last_h), str(last_m)))
    # print()
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print("temp_m_sys : {} temp_m_last : {}".format(str(temp_m_sys), str(last_m)))
    if sys_h == last_h:
        if sys_m >= last_m:
            return True
        else:
            return False

    elif sys_h > last_h:
        return True
    return False


# ----------------------------------------verify send message
def verify_message(temp_answer, input_message):
    for message in temp_answer:
        if input_message in message and 1 in message:
            return temp_answer.index(message)
    return -1


# ----------------------------------------read_and_answer_chat_box

def read_and_answer_chat_box(inside_driver=selenium.webdriver.chrome.webdriver.WebDriver):
    # ---------------------------------global variable
    print("start read")
    global end
    global start
    global time_send
    global user_count
    global hi_counter
    global yes_counter
    global bye_counter
    global no_counter
    global response_answer
    user_count = 0
    time_send = "00-00"
    try:
        user_list = inside_driver.find_elements_by_xpath(xpathes.messages_list_user)

        end = len(user_list)
        print("--------------------------------------------------------------  end : {} start : {}".format(end, start))
        print()
        # TODO reza
        if xpathes.new_started_class_flag:
            print("You idiot are late")
            start = end + 1
            xpathes.new_started_class_flag = False
        try:
            for i in range(start, end + 1):
                message_list = inside_driver.find_elements_by_xpath(xpathes.messages_counter.format(start=i))
                time_list = inside_driver.find_elements_by_xpath(xpathes.message_time.format(start=i))
                # don't edit this work current
                for element in time_list:
                    time_send = element.text
                for message in message_list:
                    # print("message : {}".format(message.text))
                    # --------------------------------------------------------controlled message
                    if message.text.find(say_hi) != -1:
                        hi_counter += 1
                        response_answer = controlled_answer(say_hi, hi_counter, time_send)
                    elif message.text.find(say_goodbye) != -1:
                        bye_counter += 1
                        response_answer = controlled_answer(say_goodbye, bye_counter, time_send)
                    elif message.text.find(say_yes) != -1:
                        yes_counter += 1
                        response_answer = controlled_answer(say_yes, yes_counter, time_send)
                    elif message.text.find(say_no) != -1:
                        no_counter += 1
                        response_answer = controlled_answer(say_no, no_counter, time_send)
                    # -------------------------------------------------------Uncontrolled message
                    else:
                        response_answer = uncontrolled_answer(message.text, time_send)
                    # return response for chat box
                    if response_answer != "null":
                        print("read end and response is : {}".format(response_answer))
                        if end >= 4:
                            start = end + 1
                        return response_answer

        except Exception as e:
            print("error read chat box")
            logging.exception(e)
            inside_driver.refresh()

    except Exception as e:
        print("error get user list")
        logging.exception(e)
        inside_driver.refresh()

    # TODO null response log
    # print("read end and response is : {}".format(response_answer))
    if end >= 4:
        start = end + 1
    return say_nothing


# ----------------------------------------reset_chat_box_reader

def reset_chat_box_reader():
    # ready for change -> global
    global robot_answer_controlled
    global robot_answer_uncontrolled
    global temp_answer_uncontrolled
    global temp_answer_controlled
    global hi_counter
    global bye_counter
    global yes_counter
    global message_counter
    global hi_flag
    global bye_Flag
    global start
    global end
    global user_count

    robot_answer_controlled = [["first", "0:00"]]
    robot_answer_uncontrolled = [["first", "0:00"]]
    temp_answer_uncontrolled = [["first", "0:00", 0]]
    temp_answer_controlled = [["first", "0:00", 0]]
    # -----------------------------Controlled counter
    hi_counter = 0
    bye_counter = 0
    yes_counter = 0
    message_counter = 0
    # -----------------------Flag Controlled just Once
    hi_flag = False
    bye_Flag = False
    # ----------------------------------start and end
    start = 1
    end = 0
    # -------------------------get data from chat box
    user_count = 0

# -------------- test controlled message
# temp_answer_controlled = [["بله", "14:54", 1], ["نه", "15:02", 1], ["بله", "15:03", 4], ["نه", "15:05", 4]]
# temp_answer_uncontrolled = [["x", "15:01", 1], ["y", "15:01", 1], ["x", "15:05", 4], ["y", "15:05", 4]]
# # verify_message(temp_answer_controlled, say_no)
#
# print(controlled_answer(say_yes, 5, "15:04") ) # null
# temp_answer_controlled = [["بله", "15:02", 1], ["نه", "14:59", 1], ["بله", "15:03", 4], ["نه", "15:10", 4]]
# print(controlled_answer(say_no, 5, "15:04") ) # نه
# temp_answer_uncontrolled = [["x", "15:45", 1], ["y", "15:38", 1], ["x", "15:18", 4], ["y", "15:05", 4]]
#     , ["x", "15:05", 4]
#     , ["x", "15:05", 4]
#     , ["x", "15:05", 4]
#     , ["y", "15:05", 4]
#     , ["y", "15:05", 4]
#     , ["y", "15:05", 4]]
# uncontrolled_answer("x", "15:39")
# temp_answer_uncontrolled = [["x", "15:38", 1], ["y", "15:40", 1], ["x", "15:18", 4], ["y", "15:05", 4]
#     , ["x", "15:05", 4]
#     , ["x", "15:05", 4]
#     , ["x", "15:05", 4]
#     , ["y", "15:05", 4]
#     , ["y", "15:05", 4]
#     , ["y", "15:05", 4]]
# uncontrolled_answer("y", "15:39")

# -------------- test time comparator

# print(time_comparator("3:20 PM", "15-30", 10))  # true
# print(time_comparator("9:20 AM", "09-25", 10))  # False
# print(time_comparator("1:59 PM", "14-04", 10))  # False
# print(time_comparator("1:59 PM", "14-59", 10))  # True
# print(time_comparator("10:41 AM", "14-35", 10))  # True
# print(time_comparator("۲۲:۱۴", "14-35", 10))  # False
# print(time_comparator("۲:۱۴", "14-35", 10))  # True
# print(time_comparator("۱۳:۴۹", "13-52", 10))  # False
# print(time_comparator("9:50", "11:20", 30))  # True
# print(time_comparator("10:2", "11:20", 30))  # True
# print(time_comparator("9:2", "11:20", 30))  # True
# print(time_comparator("09:50", "11:45", 110))  # True
# print(time_comparator("09:50", "09:56", 5))  # True
# print(time_comparator("09:50", "12:50", 175))  # True
# print(time_comparator("09:02", "09:23", 20))  # True
# print(time_comparator("۳:۳۶", "03:37", 7))  # False
# print(time_comparator("۳:0۶", "03:37", 10))  # True
# سلام and counter : 4  time : ۱۳:۱۲ now :13:13
