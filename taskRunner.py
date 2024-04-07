import sched
import time


class BackService:
    # t args
    def __init__(self):
        # print("start service")
        self.event_schedule = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action, actionargs=()):
        # interval s run again
        print("  setup service")
        action(*actionargs)
        self.event = self.event_schedule.enter(interval, 1, self.setup, (interval, action, actionargs))

    def run(self):
        print("     run service")
        self.event_schedule.run()

    def stop(self):
        print("stop service")
        print(str(self.event_schedule.empty()))
        try:
            for event in self.event_schedule.queue:
                print("every event stop")
                self.event_schedule.cancel(event)
            if self.event_schedule and self.event:
                print("a event here")
                self.event_schedule.cancel(self.event)
            else:
                print("not process")
        except Exception as e:
            print("stop error is : " + str(e))
            print(str(self.event_schedule.empty()))

    def showState(self):
        for event in self.event_schedule.queue:
            print(str(event))
        print(str(self.event_schedule.empty()))
