import threading


class SoundEvent:
    is_running = False


class SceneHandler:
    def __init__(self):
        self.sound_events = {
            '': SoundEvent()
        }


class OscReceiver:
    def handle_soundevent(self, events):
        pass


class BinSim():

    def __init__(self, path: str = ''):
        self.path = path
        self.sceneHandler = SceneHandler()
        self.oscReceiver = OscReceiver()
        self.initialized = False

    def __enter__(self):
        print('Initializing binsim')

        def init():
            self.initialized = True
            print('Initialized binsim')
        threading.Timer(1, init).start()
        return self

    def __exit__(self, *args):
        print('Closing binsim')

    def stream_start(self):
        pass
