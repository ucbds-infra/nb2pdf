"""
Adapted to python 3.6 by Rokas Kupstys.
Based on code from http://bugs.python.org/issue22239 by Daniel Arbuckle.
License: PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2 (i am sure Daniel Arbuckle will agree).
"""
import sys
import asyncio
import asyncio.tasks
import asyncio.futures

__task_step = None

def run_nested_until_complete(future, loop=None):
    """Run an event loop from within an executing task.

    This method will execute a nested event loop, and will not
    return until the passed future has completed execution. The
    nested loop shares the data structures of the main event loop,
    so tasks and events scheduled on the main loop will still
    execute while the nested loop is running.

    Semantically, this method is very similar to `yield from
    asyncio.wait_for(future)`, and where possible, that is the
    preferred way to block until a future is complete. The
    difference is that this method can be called from a
    non-coroutine function, even if that function was itself
    invoked from within a coroutine.
    """
    if loop is None:
        loop = asyncio.get_event_loop()

    loop._check_closed()
    if not loop.is_running():
        raise RuntimeError('Event loop is not running.')
    new_task = not isinstance(future, asyncio.futures.Future)
    task = asyncio.tasks.ensure_future(future, loop=loop)
    if new_task:
        # An exception is raised if the future didn't complete, so there
        # is no need to log the "destroy pending task" message
        task._log_destroy_pending = False
    while not task.done():
        try:
            loop._run_once()
        except:
            if new_task and future.done() and not future.cancelled():
                # The coroutine raised a BaseException. Consume the exception
                # to not log a warning, the caller doesn't have access to the
                # local task.
                future.exception()
            raise
    return task.result()


def __reentrant_step(self, exc=None):
    containing_task = self.__class__._current_tasks.get(self._loop, None)
    try:
        __task_step(self, exc)
    finally:
        if containing_task:
            self.__class__._current_tasks[self._loop] = containing_task


def monkeypatch():
    global __task_step
    # Replace native Task, Future and _asyncio module implementations with pure-python ones. This is required in order
    # to access internal data structures of these classes.
    sys.modules['_asyncio'] = sys.modules['asyncio']
    asyncio.Task = asyncio.tasks._CTask = asyncio.tasks.Task = asyncio.tasks._PyTask
    asyncio.Future = asyncio.futures._CFuture = asyncio.futures.Future = asyncio.futures._PyFuture

    # Replace Task._step with reentrant version.
    __task_step = asyncio.tasks.Task._step
    asyncio.tasks.Task._step = __reentrant_step


# if __name__ == '__main__':
#     async def other_asynchronous_code():
#         for i in range(5):
#             print(i)
#             await asyncio.sleep(1)

#     async def asynchronous_code():
#         await asyncio.sleep(2)
#         return 42

#     def synchronous_code():
#         return run_nested_until_complete(asynchronous_code())

#     async def coroutine():
#         print(synchronous_code())

#     monkeypatch()
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(other_asynchronous_code(), coroutine()))
#     loop.close()