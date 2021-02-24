from enum import Enum
import threading


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

    def __init__(self, binsim, area, tracker: str = 'listener', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.binsim = binsim
        self.area = area
        self.tracker = tracker
        self.triggered = threading.Event()

    def poll(self):
        if trigger_in_area(*self.area, self.tracker):
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

    @property
    def event(self):
        return binsim.sceneHandler.sound_events[self.file]

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
            self.sounds.append((channel, pos))

    def play(self, wait: bool = True):
        self.events = [SoundEvent(self.binsim, id, ch)
                       for id, ch in self.sounds]

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
