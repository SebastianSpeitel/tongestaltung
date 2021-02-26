from enum import Enum
import threading
import time


class Channel(Enum):
    POS1 = '4'
    POS2 = '3'
    POS3 = '2'
    POS4 = '5'
    POS5 = '1'
    POS6 = '0'
    C = '4'
    L = '0'
    R = '3'
    Ls = '2'
    Rs = '1'
    LFE = '5'
    INTERN = 'internm'


def tracker_in_area(binsim, minVals, maxVals):
    """
    Check whether the tracker is located inside a rectangular area defined by lower and upper edges in terms of
    a column and row identifier. These numerical identifiers relate to the QualiSys tracking data.
    See "Tracking data" comment in line 38.

    :param minVals: tuple or list of lower edge of area -> (column, row)
    :param maxVals: tuple or list of upper edge of area -> (column, row)
    :return: boolean (True -> tracker is in area, False -> tracker is not in area)
    """

    # get tracking data for channel '0' -> except for the channel id tracking data is the same for all channels
    data = binsim.oscReceiver.valueList[0]

    # organize into column and row according to filtermap quadrants (A01...Q17)
    col = data[1]
    row = data[2]

    # compare if  tracker is inside defined area
    if col >= minVals[0] and col <= maxVals[0]:
        if row >= minVals[1] and row <= maxVals[1]:
            print('\n TRIGGERED \n')  # mainly for debug purposes
            return True
    return False


class Event:
    def __init__(self, poll_interval: float = 10e-6, *args, **kwargs):
        self._poll_interval = poll_interval
        self._polling = threading.Event()
        threading.Thread(target=self._poll, daemon=True).start()

    def _poll(self):
        while True:
            if not self._polling.is_set():
                self._polling.wait()
            self.poll()
            time.sleep(self._poll_interval)

    def start_polling(self):
        self._polling.set()

    def stop_polling(self):
        self._polling.clear()

    def poll(self):
        raise NotImplementedError('poll needs to be implemented')


class Trigger(Event):

    def __init__(self, binsim, area=None, rotation=None, tracker: str = 'listener', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.binsim = binsim
        self.area = area
        self.rotation = rotation
        self.tracker = tracker
        self.triggered = threading.Event()

    def poll(self):
        # TODO get trigger_in_are from script
        if trigger_in_area(self.binsim, *self.area, self.tracker):
            self.triggered.set()
        else:
            self.triggered.clear()

    def wait(self):
        self.triggered.wait()


class SoundEvent(Event):

    def __init__(self, binsim, file: str, channel: Channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.binsim = binsim
        self.file = file
        self.channel = channel

        self.playing = threading.Event()
        self.stopped = threading.Event()

    def __repr__(self):
        return "<SoundEvent (channel={channel}, file={file})>".format(channel=self.channel, file=self.file)

    @property
    def event(self):
        return self.binsim.sceneHandler.sound_events[self.file]

    @property
    def is_running(self):
        return self.event and self.event.is_running

    def poll(self):

        playing = self.playing.is_set()
        running = self.is_running

        # Sound just started running
        if running and not playing:
            self.playing.set()

        # Sound just stopped running
        if playing and not running:
            self.playing.clear()
            # TODO: check if paused
            self.stopped.set()
            self.stop_polling()

    def play(self, wait: bool = True):
        self.binsim.oscReceiver.handle_soundevent(
            [[self.file, 'start', self.channel.value]]
        )
        self.start_polling()
        if wait:
            self.playing.wait()

    def stop(self, wait: bool = True):
        self.binsim.oscReceiver.handle_soundevent(
            [[self.file, 'stop']]
        )
        self.stopped.set()
        if wait:
            self.stopped.wait()
        self.stop_polling()


class SoundEvents:
    def __init__(self, binsim, **kwargs):
        self.binsim = binsim

        self.sounds = list()
        self.events = list()
        for ch, id in kwargs.items():
            channel = getattr(Channel, ch, None)
            if channel is None:
                continue
            self.sounds.append((channel, id))

    def play(self, wait: bool = True):
        self.events = [SoundEvent(self.binsim, id, ch)
                       for ch, id in self.sounds]

        for evt in self.events:
            evt.play()

        if wait:
            for evt in self.events:
                evt.playing.wait()

    def stop(self, wait: bool = True):
        for evt in self.events:
            evt.stop()

        if wait:
            for evt in self.events:
                evt.stopped.wait()

    def wait(self):
        for evt in self.events:
            evt.stopped.wait()
