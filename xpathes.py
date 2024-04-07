# true & yes button xpath in polls
# /html/body/div/main/div[1]/div/div[2]/div[1]/button
# false & no button xpath in polls
# /html/body/div/main/div[1]/div/div[2]/div[2]/button
login_btn = "//*[@id='login']/input[3]"
joining_class_link = "//a[contains(@href, '/mod/bigbluebuttonbn/bbb_view.php')]"
classes_time = "//small[contains(@class, 'text-right text-nowrap ml-1')]"
main_body = ".//html/body"
# yes_button_xpath = "//button[@class='button--Z2dosza md--Q7ug4 primary--1IbqAO pollingButton--ZQBQjq']"
yes_button_xpath = "/html/body/div/main/div[1]/div/div[2]/div[1]/button"
no_button_xpath = "/html/body/div/main/div[1]/div/div[2]/div[2]/button"
messages_in_chatbox_xpath = "//div[@class='item--ZDfG6l']"
end_class_btn_xpath = "//*[@id='app']/div/div/div/div/button"
end_class_btn_xpath2 = "/html/body/div/div/div/div/div/button"
end_class_btn_xpath3 = "//*[@id='app']/div/div/div/button"
end_class_btn_xpath4 = "/html/body/div/div/div/div/button"
headphone_btn_xpath = "/html/body/div[2]/div/div/div[1]/div/div/span/button[2]/span[1]"
headphone_btn_xpath2 = "/html/body/div[2]/div/div/div[1]/div/div/span/button/span[1]"
headphone_btn_xpath3 = "/html/body/div[2]/div/div/div[1]/div/span/button/span[1]"

# ----------------------------------------------------------------------check class time
master_xpath = "//div[contains(@class, 'presenter--')]"
# master_xpath = "//div[contains(@class, 'avatar-- presenter--')]"
# master_xpath = "//div[@class='avatar--Z2lyL8K moderator--24bqCT presenter--Z1INqI5 voice--2oPUk4']"
# master or admin
# "avatar--Z2lyL8K moderator--24bqCT presenter--Z1INqI5 voice--2oPUk4"
# normal users
# class ="avatar--Z2lyL8K listenOnly--1qW98O voice--2oPUk4"

audioOff = ".//i[@class ='icon--2q1XXw icon-bbb-audio_off']"
audioON = ".//i[@class ='icon--2q1XXw icon-bbb-listen']"
audio_btn = "//*[@id='tippy-18']"
# //*[@id="tippy-19"]/span[1]
# //*[@id="tippy-19"]
# //*[@id="app"]/main/section/div/section[2]/div/div[2]/span


#  --------------------------------------------------------------------regex test start
# item--ZDfG6l
messages_list_user = "//div[@class='item--ZDfG6l']"
messages_counter = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[2]/p"
message_user = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[1]/div"
message_time = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[1]/time"
messages = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[2]"
#  --------------------------------------------------------------------regex test end
chat = "//div[@class='Z2vq9Jh']"
chat_text = "//div[@class='message--Z2n2nXu']"
messages_list4 = "//div[@class='item--ZDfG6l']/div[@class='wrapper--Z1BLczb']/div[@class='content--Z2nhld9']/div[@class='messages--Z2vq9Jh']"
chat_input = "//*[@id='message-input']"
chat_send_btn = ".//i[@class ='icon--2q1XXw icon-bbb-send']"
###########################################################
# global flags
global login_flag
global logout_flag
global end_session_flag
global today_classes_flag
global in_session_flag
global change_detector_flag
new_started_class_flag = False
findClass_flag = False

##########################################################
# global var
# last_entered_class_time = ""
last_html_file = ""

#########################################################
# adobe connect


# joining_class_link = "//a[contains(@href, '/mod/bigbluebuttonbn/bbb_view.php')]"
# classes_time = "//small[contains(@class, 'text-right text-nowrap ml-1')]"
# main_body = ".//html/body"
# yes_button_xpath = "//button[@class='button--Z2dosza md--Q7ug4 primary--1IbqAO pollingButton--ZQBQjq']"
# no_button_xpath = "/html/body/div/main/div[1]/div/div[2]/div[2]/button"
# messages_in_chatbox_xpath = "//div[@class='item--ZDfG6l']"
# end_class_btn_xpath = "//*[@id='app']/div/div/div/button"
# headphone_btn_xpath = "/html/body/div[2]/div/div/div[1]/div/div/span/button[2]/span[1]"
#
#
# #  --------------------------------------------------------------------regex test start
# # item--ZDfG6l
# messages_list_user = "//div[@class='item--ZDfG6l']"
# messages_counter = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[2]/p"
# message_user = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[1]/div"
# message_time = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[1]/time"
# messages = "//*[@id='chat-messages']/div[{start}]/div/div[2]/div[2]"
# #  --------------------------------------------------------------------regex test end
# chat = "//div[@class='Z2vq9Jh']"
# chat_text = "//div[@class='message--Z2n2nXu']"
# messages_list4 = "//div[@class='item--ZDfG6l']/div[@class='wrapper--Z1BLczb']/div[@class='content--Z2nhld9']/div[@class='messages--Z2vq9Jh']"
# chat_input = "//*[@id='message-input']"
# chat_send_btn = ".//i[@class ='icon--2q1XXw icon-bbb-send']"
