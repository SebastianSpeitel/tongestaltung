from story import Story, StoryUnit, SoundEvents, Channel, Trigger
import time
import threading


class Gruppe2(Story):

    def __init__(self, binsim):
        super().__init__()
        self.binsim = binsim

        self.s_loop_bats_window = SoundEvents(
            self.binsim,
            R='001'  # TODO
        )
        self.s_loop_rain = SoundEvents(
            self.binsim,
            C='002'  # TODO
        )
        self.s_loop_zombie_front = SoundEvents(
            self.binsim,
            L='003'  # TODO
        )
        self.s_loop_bats_corner = SoundEvents(
            self.binsim,
            Rs='016',  # TODO
        )
        self.s_loop_radio = SoundEvents(
            self.binsim,
            LFE='019'  # TODO
        )
        self.s_loop_radio_noise1 = SoundEvents(
            self.binsim,
            LFE='021'  # TODO
        )
        self.s_loop_radio_noise2 = SoundEvents(
            self.binsim,
            LFE='022'  # TODO
        )
        self.s_loop_radio_noise3 = SoundEvents(
            self.binsim,
            LFE='023'  # TODO
        )

        self.var_bats_inside = False
        self.var_buddy_alive = True

    def start(self):
        self.s_loop_bats_window.play()
        self.s_loop_rain.play()
        self.s_loop_zombie_front.play()

        self.flight()

    def flight(self):
        # ANU1
        ankunft = SoundEvents(
            self.binsim,
            L='004',  # TODO
            Ls='005'  # TODO
        )
        ankunft.play()
        ankunft.wait()

        trigger = Trigger(self.binsim, [[], []])

        hint_at = time.perf_counter() + 3
        fallback_at = time.perf_counter() + 9
        hinted = False
        while True:
            if trigger.triggered.is_set() or time.perf_counter() > fallback_at:
                self.window_locked()
                break

            if not hinted and time.perf_counter() > hint_at:
                hinted = True
                self.hint1()

            time.sleep(10e-6)

    def hint1(self):
        hint = SoundEvents(
            self.binsim,
            Ls='006'  # TODO
        )
        hint.play()
        hint.wait()

    def window_locked(self):
        # ANU3
        window = SoundEvents(
            self.binsim,
            C='007',  # TODO
            L='008',  # TODO
            Ls='009'  # TODO
        )
        window.play()
        window.wait()

        to_window = Trigger(self.binsim, [[], []])
        to_door = Trigger(self.binsim, [[], []])

        while True:
            if to_window.triggered.is_set():
                self.window_bats()
                break

            if to_door.triggered.is_set():
                self.door_zombie()
                break

            time.sleep(10e-6)

    def window_bats(self):
        # ANU5
        bats = SoundEvents(
            self.binsim,
            C='010',  # TODO
            L='011',  # TODO
            LFE='012',  # TODO
            Ls='013',  # TODO
            R='014',  # TODO
            Rs='015',  # TODO
        )
        bats.play()
        self.s_loop_bats_corner.play()

        self.s_loop_radio.play()
        self.s_loop_radio_noise1.play()
        self.s_loop_radio_noise2.play()
        self.s_loop_radio_noise3.play()
        bats.wait()
        self.var_bats_inside = True

        self.radio()

    def door_zombie(self):
        # ANU6

        door = SoundEvents(
            self.binsim,
            C='017',  # TODO
            L='018'  # TODO
        )
        door.play()
        self.s_loop_radio.play()
        self.s_loop_radio_noise1.play()
        self.s_loop_radio_noise2.play()
        self.s_loop_radio_noise3.play()
        door.wait()
        self.var_buddy_alive = False
        self.radio()

    def radio(self):
        # ANU7

        if self.var_buddy_alive:
            hint1_at = time.perf_counter()+3
            hinted1 = False
            hint2_at = time.perf_counter()+6
            hinted2 = False

        radio_rotated1 = Trigger(self.binsim, rotation=(0, 360))
        radio_rotated2 = Trigger(self.binsim, rotation=(90, 180))
        radio_rotated3 = Trigger(self.binsim, rotation=(100, 120))

        while True:
            if self.var_buddy_alive and not hinted1 and time.perf_counter() > hint1_at:
                hint1 = SoundEvents(
                    self.binsim,
                    C='020'  # TODO hinweis_radio
                )
                hint1.play()
                hint1.wait()

            if self.var_buddy_alive and not hinted2 and time.perf_counter() > hint2_at:
                hint2 = SoundEvents(
                    self.binsim,
                    C='021'  # TODO hinweis_radio2
                )
                hint2.play()
                hint2.wait()

            if radio_rotated1.triggered.is_set():
                hinted1 = True
                hinted2 = True
                self.s_loop_radio_noise1.stop()

            if radio_rotated2.triggered.is_set():
                hinted1 = True
                hinted2 = True
                self.s_loop_radio_noise2.stop()

            if radio_rotated3.triggered.is_set():
                hinted1 = True
                hinted2 = True
                self.s_loop_radio_noise3.stop()

            time.sleep(10e-6)

        # def start(self):
        #     s = SoundEvents(
        #         self.binsim,
        #         POS6='001',
        #         POS1='002'
        #     )
        #     s.play()
        #     s.wait()

        #     self.hint = self.hint_window(parallel=True)
        #     self.window_locked(parallel=True)

        # def hint_window(self):
        #     self.waiting_for_locked_window = True
        #     time.sleep(5)
        #     if self.waiting_for_locked_window:
        #         # play sound
        #         pass

        # def window_locked(self):
        #     """
        #     Locked window
        #     """
        #     self.waiting_for_locked_window = False
        #     if self.hint:
        #         self.hint.join()

        #     # play sounds and wait to finish

        #     self.wait_for_door(parallel=True)
        #     self.wait_for_window(parallel=True)

        # def wait_for_door(self):
        #     self.waiting_for_door = True
        #     trigger = Trigger(self.binsim, ([], []), 'listener')
        #     trigger.wait()
        #     if not self.waiting_for_door:
        #         return
        #     self.door()

        # def wait_for_window(self):
        #     self.waiting_for_window = True
        #     trigger = Trigger(self.binsim, ([], []), 'listener')
        #     trigger.wait()
        #     if not self.waiting_for_window:
        #         return
        #     self.window_bats()

        # def door(self):
        #     self.waiting_for_door = False
        #     self.waiting_for_window = False
        #     self.buddy_alive = False

        # def window_bats(self):
        #     self.waiting_for_door = False
        #     self.waiting_for_window = False
        #     self.bats = True

        # def radio(self):
        #     pass

        # def transition(self):
        #     pass

        # def ending(self):
        #     pass
