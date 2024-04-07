import time
import App
import saveData
import functools
import attendSession
from tkinter import *
import threading
import gui_tools
from tkinter import messagebox
from PIL import ImageTk, Image
import utils, attendSession

"""
       ui  :                    click set :
       main_window_show          main_button_set   
       insert_window_show        insert_button_set  
       run_window_show


insert_button_set  ->  insert_btn_click   ->  get input and send to app.py  verify
run_window_show     ->  login 

"""
# --------------check input insert window
check_pass = "password"
check_user = "username"
check_mob = "9100000000"
check_url = "http://example.ir"


# ------------------------------------------------- gui
def start_clock(main_window, label):
    gui_tools.Clock(main_window, label)


class Gui:
    def __init__(self):
        self.width_main = 720
        self.height_main = 640

        self.main_window_show()

    def main_button_set(self):
        def insert_btn_click():
            self.back_main_window.unload()
            # self.label.destroy()
            self.back_main_window.destroy()
            self.insert_window_show()

        def about_btn_click():
            self.main_window.update()
            messagebox.showinfo("راه ارتباطی", "www.google.com")

        def start_btn_click():
            check_value = App.Verify.check_mobile()
            # print(str(check_value))
            # TODO check_value is just for test because json read_data dont work so after test remove it
            # check_value = 1
            if check_value == 1:
                try:
                    user_data = saveData.read_data()
                    # TODO saeed json ro str mishnase va username & password & url ro nemitune meghdar dehi kone!moshkel az khoruji read_data() toie khat balas ((((toie check_mobile ham estefade kardi onja ham dorostesh kon )))))
                    username = user_data.get("user")
                    password = user_data.get("pass")
                    url = user_data.get("url")
                    # username = '9618143106'
                    # password = '9618143106'
                    # url = 'https://el.ardakan.ac.ir/login/index.php'
                    # switch window
                    self.back_main_window.unload()
                    # # self.label.destroy()
                    self.back_main_window.destroy()
                    self.run_window_show(username, password, url)
                except Exception as e:
                    print(str(e))
                    messagebox.showinfo("  خطا  ",
                                        "  اطلاعات وارد شده را بررسی کنید یا با پشتیبانی تماس حاصل فرمایید  ")
            elif check_value == 2:
                messagebox.showinfo("  اخطار  ", "  شما با سریال شخص دیگری قصد اجرا برنامه دارید  ")
            else:
                messagebox.showinfo("  اخطار  ", "  شما ثبت نام نکرده اید   ")

        def exit_btn_click():
            # TODO check exit after insert
            # self.main_window.deiconify()
            # self.main_window.update()
            # self.back_main_window = gui_tools.ImageLabel(self.main_window)
            # self.back_main_window.pack()
            # self.back_main_window.load('images/exit_window.jpg')
            # self.back_main_window.place(x=0, y=0, relwidth=1, relheight=1)
            # image2 = Image.open('images/exit_window.jpg')
            # image1 = ImageTk.PhotoImage(image2)
            # self.width_main = image1.width()
            # self.height_main = image1.height()
            # self.main_window.geometry("%dx%d+0+0" % (self.width_main, self.height_main))
            # gui_tools.center_window(self.width_main, self.height_main, self.main_window)
            # self.main_window.update()
            # end()

            time.sleep(2)
            self.main_window.deiconify()
            self.back_main_window = gui_tools.ImageLabel(self.main_window)
            image2 = Image.open('images/exit_window.jpg')
            image1 = ImageTk.PhotoImage(image2)
            w = image1.width()
            h = image1.height()
            gui_tools.center_window(w, h, self.main_window)
            self.back_main_window.pack()
            self.back_main_window.load('images/exit_window.jpg')
            self.main_window.update()
            time.sleep(2)
            end()
            # self.main_window.destroy()

        def end():
            time.sleep(2)
            self.main_window.destroy()
            self.main_window.quit()
            utils.in_class_task_runner.stop()
            attendSession.find_class_task.stop()

        # button icon
        exit_photo = PhotoImage(file='images/logout.png')
        add_photo = PhotoImage(file='images/add.png')
        support_photo = PhotoImage(file='images/support.png')
        run_photo = PhotoImage(file='images/run.png')

        # resize images
        exit_image = exit_photo.subsample(2, 2)
        add_image = add_photo.subsample(2, 2)
        support_image = support_photo.subsample(3, 3)
        run_image = run_photo.subsample(2, 2)

        # telegram id
        id_label = Label(self.main_window, text="@GitGpAdmin", font=('arial', 24, 'bold'),
                         fg="#0000D8", bg='white').place(x=520, y=538)

        exit_btn = Button(self.main_window, text="  خروج ", command=exit_btn_click,
                          image=exit_image, compound=LEFT,
                          font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
                          activeforeground="white",
                          activebackground="blue",
                          bg="white", fg="#0000D8").place(x=10, y=540)

        support_btn = Button(self.main_window, text="  پشتیبانی  ", command=about_btn_click,
                             image=support_image, compound=LEFT,
                             activeforeground="white",
                             activebackground="blue",
                             font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
                             bg="white", fg="#0000D8").place(x=100, y=540)

        insert_btn = Button(self.main_window, text="  درج اطلاعات   ", command=insert_btn_click,
                            image=add_image, pady=2, compound=LEFT,
                            activeforeground="white",
                            activebackground="blue",
                            font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
                            bg="white", fg="#0000D8").place(x=30, y=100)

        start_btn = Button(self.main_window, text="  شروع به کار ", command=start_btn_click,
                           image=run_image, pady=2, compound=LEFT,
                           activeforeground="white",
                           activebackground="blue",
                           font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
                           bg="white", fg="#0000D8").place(x=30, y=150)

        # set center and mainloop and clock
        gui_tools.center_window(self.width_main, self.height_main, self.main_window)
        # digit clock
        label = Label(self.main_window, text="", font=('arial', 40, 'bold'), fg="#0000D8", bg='white')
        label.pack()

        gui_tools.Clock(self.main_window, label)
        # clock = threading.Thread(target=startClock, args=(self.main_window, label))
        # clock.start()
        self.main_window.mainloop()

    def insert_button_set(self):
        def insert_btn_click():
            #  check input
            if not (
                    entry_url.get() == check_url
                    or entry_pass.get() == check_pass
                    or entry_user.get() == check_user
                    or entry_mob.get() == check_mob
                    or len(entry_url.get()) == 0
                    or len(entry_pass.get()) == 0
                    or len(entry_user.get()) == 0
                    or len(entry_mob.get()) == 0):
                # IF not empty do :
                print("->-> I send your data to WebApi To check !! ")
                verify_user = App.Verify(entry_mob.get(), entry_user.get(), entry_pass.get(), entry_url.get())
                # print(str(verify_user.get_result_code()))
                if verify_user.get_result_code() == 1:
                    messagebox.showinfo("درج اطلاعات ", "اطلاعات ثبت شد")
                    print("Your account is valid :)")
                elif verify_user.get_result_code() == 2:
                    messagebox.showinfo("  خطا  ", "  اکانت شما معتبر نمی باشد  ")
                    print("Your account is not valid :)")
                else:
                    messagebox.showinfo("  خطا  ", "  اطلاعات ورودی بررسی کنید یا با پشتیبانی تماس حاصل فرمایید  ")
                    print("Your account is not valid :)")
            else:
                messagebox.showinfo(" توجه  ", "اطلاعات با دقت وارد نمایید")
                print("Check your data !!")

        def back_btn_click():
            self.insert_window.destroy()
            # create main again
            self.main_window = Toplevel()
            self.back_main_window = gui_tools.ImageLabel(self.main_window)
            self.back_main_window.pack()
            self.back_main_window.load('images/main_window.gif')
            self.back_main_window.place(x=0, y=0, relwidth=1, relheight=1)
            image2 = Image.open('images/main_window.gif')
            image1 = ImageTk.PhotoImage(image2)
            self.width_main = image1.width()
            self.height_main = image1.height()
            print("------------" + str(self.width_main) + "----" + str(self.height_main))
            self.main_window.geometry("%dx%d+0+0" % (self.width_main, self.height_main))
            self.main_window.update()
            self.main_button_set()
            # update
            # self.main_window.deiconify()

        def entry_empty(event, entry):
            entry.delete(0, "end")
            return None

        #  -------------------------------------------------------------------- label
        welcome_lbl = Label(self.insert_window, text=" ثبت اطلاعات ",
                            font=('/font/Shabnam-Medium.ttf', 18, 'bold'),
                            fg='white', bg='#0000d8', width=50)
        welcome_lbl.place(x=0, y=20)

        mob_lbl = Label(self.insert_window, text="شماره همراه",
                        font=('/font/Shabnam-Medium.ttf', 15, 'bold'),
                        fg='white', bg='#0000d8', width=10)
        mob_lbl.place(x=260, y=70)

        url_lbl = Label(self.insert_window, text="لینک سایت",
                        font=('/font/Shabnam-Medium.ttf', 15, 'bold'),
                        fg='white', bg='#0000d8', width=10)
        # url_lbl.configure(anchor="e")
        url_lbl.place(x=260, y=140)

        user_lbl = Label(self.insert_window, text="نام کاربری",
                         font=('/font/Shabnam-Medium.ttf', 15, 'bold'),
                         fg='white', bg='#0000d8', width=10)
        user_lbl.place(x=260, y=210)

        pass_lbl = Label(self.insert_window, text="پسورد",
                         font=('/font/Shabnam-Medium.ttf', 15, 'bold'),
                         fg='white', bg='#0000d8', width=10)
        pass_lbl.place(x=260, y=280)
        #  -------------------------------------------------------------------- entry

        entry_mob = Entry(self.insert_window,
                          font=('irans-sans', 15, 'bold'),
                          bd=3, bg="white", fg="#2196f3",
                          selectbackground="red",
                          width=25, justify=CENTER)
        entry_mob.insert(0, '09100000000')
        entry_mob.bind("<Button-1>", functools.partial(entry_empty, entry=entry_mob))
        entry_mob.place(x=100, y=100)

        entry_url = Entry(self.insert_window,
                          font=('irans-sans', 15, 'bold'),
                          bd=3, bg="white", fg="#2196f3",
                          selectbackground="red",
                          width=25, justify=CENTER)
        entry_url.insert(0, 'http://example.ir')
        entry_url.bind("<Button-1>", functools.partial(entry_empty, entry=entry_url))
        entry_url.place(x=100, y=170)

        entry_user = Entry(self.insert_window,
                           font=('irans-sans', 15, 'bold'),
                           bd=3, bg="white", fg="#2196f3",
                           selectbackground="red",
                           width=25, justify=CENTER)
        entry_user.insert(0, 'username')
        entry_user.bind("<Button-1>", functools.partial(entry_empty, entry=entry_user))
        entry_user.place(x=100, y=240)

        entry_pass = Entry(self.insert_window,
                           font=('irans-sans', 15, 'bold'),
                           bd=3, bg="white", fg="#87CEFA",
                           selectbackground="red", show="*",
                           width=25, justify=CENTER)
        entry_pass.insert(0, 'password')
        entry_pass.bind("<ButtonPress-1>", functools.partial(entry_empty, entry=entry_pass))
        entry_pass.place(x=100, y=310)
        # TODO icon for insert button
        exit_btn = Button(self.insert_window, text="بازگشت", command=back_btn_click,
                          activeforeground="white",
                          activebackground="blue",
                          font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
                          pady=10, bg="white",
                          fg="#0000d8", padx=60).place(x=145, y=430)

        insert_btn = Button(self.insert_window, text="درج اطلاعات", command=insert_btn_click,
                            activeforeground="white",
                            activebackground="white", font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
                            pady=10, bg="#0000d8",
                            fg="white", padx=80).place(x=120, y=370)

        # run_photo = PhotoImage(file='images/run.png')
        #
        # exit_image = exit_photo.subsample(2, 2)
        # start_btn = Button(self.main_window, text="  شروع به کار ", command=start_btn_click,
        #                    image=run_image, pady=2, compound=LEFT,
        #                    activeforeground="white",
        #                    activebackground="blue",
        #                    font=('/font/Shabnam-Medium.ttf', 14, 'bold'),
        #                    bg="white", fg="#0000D8").place(x=30, y=150)

    def main_window_show(self):
        self.main_window = Tk()
        self.main_window.title("! شرکت در کلاس مجازی خودکار  ")
        # gif set
        self.back_main_window = gui_tools.ImageLabel(self.main_window)
        self.back_main_window.pack()
        self.back_main_window.load('images/main_window.gif')
        self.back_main_window.place(x=0, y=0, relwidth=1, relheight=1)
        image2 = Image.open('images/main_window.gif')
        image1 = ImageTk.PhotoImage(image2)
        self.width_main = image1.width()
        self.height_main = image1.height()
        # print("------------" + str(self.width_main) + "----" + str(self.height_main))
        self.main_window.geometry("%dx%d+0+0" % (self.width_main, self.height_main))

        # #center window
        # gui_tools.center_window(self.width_main, self.height_main, self.main_window)
        # # digit clock
        # label = Label(self.main_window, text="", font=('arial', 40, 'bold'), fg='blue', bg='white')
        # label.pack()
        # gui_tools.Clock(self.main_window, label)
        # # button set
        self.main_button_set()
        # self.main_window.mainloop()

    def insert_window_show(self):
        self.main_window.update()
        self.main_window.withdraw()
        w = 480
        h = 520
        self.insert_window = Toplevel()
        self.insert_window.geometry("400x300")
        self.insert_window.title("ثبت اطلاعات و دریافت سریال  ")
        back_insert = gui_tools.ImageLabel(self.insert_window)
        back_insert.pack()
        gui_tools.center_window(w, h, self.insert_window)
        self.insert_window.update()

        # ---------------------button insert window
        self.insert_button_set()

        # -----------------------digit clock run window
        # label = Label(self.insert_window, text="", font=('arial', 25, 'bold'), fg='blue', bg='white')
        # label.pack()
        # gui_tools.Clock(self.insert_window, label)
        self.insert_window.mainloop()

    def run_window_show(self, username, password, url):
        # TODO run attendSession.py
        self.main_window.update()
        self.main_window.withdraw()

        run_window = Toplevel()
        run_window.geometry("400x300")
        run_window.title("! شرکت در کلاس مجازی خودکار  ")
        # login("9618143113", "saeed2402", url)
        # login("9618143106", "9618143106", url)
        back_run_window = gui_tools.ImageLabel(run_window)
        back_run_window.pack()
        back_run_window.load('images/run_window.gif')
        back_run_window.place(x=0, y=0, relwidth=1, relheight=1)
        image2 = Image.open('images/run_window.gif')
        image1 = ImageTk.PhotoImage(image2)
        w = image1.width()
        h = image1.height()

        login_in_main_page_thread = threading.Thread(target=login_function, args=(username, password, url))
        login_in_main_page_thread.start()

        def end():
            time.sleep(2)
            run_window.destroy()
            self.main_window.deiconify()
            self.back_main_window = gui_tools.ImageLabel(self.main_window)
            self.back_main_window.pack()
            self.back_main_window.load('images/main_window.gif')
            self.back_main_window.place(x=0, y=0, relwidth=1, relheight=1)
            image2 = Image.open('images/main_window.gif')
            image1 = ImageTk.PhotoImage(image2)
            w = image1.width()
            h = image1.height()
            self.main_window.geometry("%dx%d+0+0" % (w, h))
            self.main_window.update()
            self.main_button_set()
            # stop all tasks
            utils.in_class_task_runner.stop()
            attendSession.find_class_task.stop()
            exit(0)

        exit_btn = Button(run_window, text="    Back    ", command=end, activeforeground="white",
                          activebackground="blue",
                          pady=10, bg="white", fg="blue")
        exit_btn.pack(side=BOTTOM)

        # digit clock run window

        label = Label(run_window, text="", font=('arial', 25, 'bold'), fg='blue', bg='white')
        label.pack()
        gui_tools.Clock(run_window, label)

        gui_tools.down_window(width=w, height=h, window=run_window)
        run_window.mainloop()


def login_function(username, password, url):
    print('I send your data to Google Chrome ->->')
    attendSession.Login_in_main_page(username, password, url)
