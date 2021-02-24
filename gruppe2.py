from story import Story, StoryUnit, SoundEvents, Channel, Trigger
import time
import threading


class Gruppe2(Story):

    def __init__(self, binsim):
        super().__init__()
        self.binsim = binsim

        self.buddy_alive = True
        self.bats = False
        self.waiting_for_door = False
        self.waiting_for_window = False
        self.waiting_for_locked_window = False
        self.hint = None

    def start(self):
        s = SoundEvents(
            self.binsim,
            POS6='001',
            POS1='002'
        )
        s.play()

        self.hint = self.hint_window(parallel=True)
        self.window_locked(parallel=True)

    def hint_window(self):
        self.waiting_for_locked_window = True
        time.sleep(5)
        if self.waiting_for_locked_window:
            # play sound
            pass

    def window_locked(self):
        """
        Locked window
        """
        self.waiting_for_locked_window = False
        if self.hint:
            self.hint.join()

        # play sounds and wait to finish

        self.wait_for_door(parallel=True)
        self.wait_for_window(parallel=True)

    def wait_for_door():
        self.waiting_for_door = True
        trigger = Trigger(self.binsim, ([], []), 'listener')
        trigger.wait()
        if not self.waiting_for_door:
            return
        self.door()

    def wait_for_window():
        self.waiting_for_window = True
        trigger = Trigger(self.binsim, ([], []), 'listener')
        trigger.wait()
        if not self.waiting_for_window:
            return
        self.window_bats()

    def door(self):
        self.waiting_for_door = False
        self.waiting_for_window = False
        self.buddy_alive = False

    def window_bats(self):
        self.waiting_for_door = False
        self.waiting_for_window = False
        self.bats = True

    def radio(self):
        pass

    def transition(self):
        pass

    def ending(self):
        pass
