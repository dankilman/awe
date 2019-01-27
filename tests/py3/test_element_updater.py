import pytest
from six.moves.queue import Queue

from awe import element_updater


@pytest.mark.parametrize('add_after_start, generator', [
    (False, False),
    (True, False),
    (False, True),
    (True, True),
])
def test(add_after_start, generator):
    queue = Queue()
    e = {}
    em = element_updater.ElementUpdater()

    async def fn(element):
        element.setdefault('called', []).append(True)
        queue.put(True)
    count = 1

    if generator:
        count = 2
        old_fn = fn

        async def fn(element):
            for _ in range(2):
                await old_fn(element)
                yield

    updater = element_updater.Updater(element=e, updater=fn)
    if add_after_start:
        em.start()
        em.add(updater)
    else:
        em.add(updater)
        em.start()

    for _ in range(count):
        queue.get(timeout=3)
    assert e['called'] == [True] * count
