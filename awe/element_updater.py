import six
import threading
import inspect

if six.PY3:
    import asyncio
else:
    asyncio = None


class Updater(object):

    def __init__(self, element, updater):
        self.element = element
        self.updater = updater


class ElementUpdater(object):

    def __init__(self):
        self.threads = []
        self.started = False
        if six.PY3:
            self.async_thread = threading.Thread(target=self._asyncio_run)
            self.async_thread.daemon = True
            self.async_loop = asyncio.new_event_loop()
        else:
            self.async_thread = None
            self.async_loop = None

    def add(self, updater):
        assert isinstance(updater, Updater)
        fn = updater.updater
        if six.PY3 and inspect.isasyncgenfunction(fn):
            self.async_loop.call_soon_threadsafe(self._add_async_generator_updater, updater)
        elif six.PY3 and inspect.iscoroutinefunction(fn):
            self.async_loop.call_soon_threadsafe(self._add_async_updater, updater)
        elif inspect.isgeneratorfunction(fn):
            self._add_generator_updater(updater)
        elif callable(fn):
            self._add_callable_updater(updater)
        else:
            raise ValueError('Invalid updater: {}'.format(fn))

    def start(self):
        if self.started:
            return
        if self.async_thread:
            self.async_thread.start()
        for thread in self.threads:
            thread.start()
        self.started = True

    def _asyncio_run(self):
        loop = self.async_loop
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    def _add_async_updater(self, updater):
        self.async_loop.create_task(updater.updater(updater.element))

    def _add_async_generator_updater(self, updater):
        generator = updater.updater(updater.element)
        anext = generator.__anext__

        def callback(old_task):
            if old_task and old_task.exception():
                exception = old_task.exception()
                if not isinstance(exception, __builtins__.StopAsyncIteration):
                    raise exception
                return
            t = self.async_loop.create_task(anext())
            t.add_done_callback(callback)
        callback(None)

    def _add_generator_updater(self, updater):
        def updater_wrapper():
            for _ in updater.updater(updater.element):
                pass
        self._add_thread(updater_wrapper)

    def _add_callable_updater(self, updater):
        self._add_thread(lambda: updater.updater(updater.element))

    def _add_thread(self, fn):
        thread = threading.Thread(target=fn)
        thread.daemon = True
        self.threads.append(thread)
        if self.started:
            thread.start()
