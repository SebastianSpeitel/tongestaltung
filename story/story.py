import functools
from threading import Thread


class StoryUnit(Thread):

    @classmethod
    def wrap(self, func):
        story = getattr(func, '__self__', None)

        @functools.wraps(func)
        def wrapped(start=True, parallel=False, *args, **kwargs):
            unit = StoryUnit(func, args, kwargs, story=story)
            if start:
                unit.start()
            if not parallel:
                unit.join()
            return unit

        return wrapped

    def __init__(self, func, args, kwargs, story):
        super().__init__(
            target=func,
            args=args,
            kwargs=kwargs,
            name=func.__name__
        )
        self.story = story


    def start(self):
        print('Starting:', self)
        super().start()


class Story:
    def __init__(self):
        attr_names = set(dir(self)).difference(dir(Story))
        for attr_name in attr_names:
            attr = getattr(self, attr_name)
            if not callable(attr):
                continue

            wrapped = StoryUnit.wrap(attr)
            setattr(self, attr_name, wrapped)
