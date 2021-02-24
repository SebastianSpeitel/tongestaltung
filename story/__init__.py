
import time
import threading
from .pybinsim import BinSim
from .story import Story, StoryUnit
from .event import SoundEvent, SoundEvents, Channel, Trigger

if __name__ == "__main__":
    class MyStory(Story):

        def __init__(self, binsim: BinSim):
            super().__init__()
            self.binsim = binsim

        def anu1(self):
            sound = SoundEvent(self.binsim, '', Channel.POS1)
            print('anu1')
            self.anu2(parallel=True)
            print('before anu2')

        def anu2(self):
            print('anu2-1')
            time.sleep(1)
            print('anu2-2')

    CONFIG_PATH = 'config/config_' + 'Gruppe2' + '.cfg'
    with BinSim(CONFIG_PATH) as binsim:
        stream_thread = threading.Thread(
            target=binsim.stream_start,
            daemon=True
        )
        stream_thread.start()

        # wait binsim to be initialized completely
        while not binsim.initialized:
            time.sleep(1)

        story = MyStory(binsim)

        anu1 = story.anu1(parallel=True)
        print(anu1)
        anu1.join()
        print(anu1)
