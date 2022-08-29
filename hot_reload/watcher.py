import asyncio
import importlib
from pathlib import Path
import debugpy

import xloil as xlo
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


@xlo.func
async def Watcher():
    debugpy.debug_this_thread()
    current_path = Path(__file__).parent

    # Initial load
    yield "Starting to load modules..."
    p = current_path.iterdir()
    for f in p:
        if f.is_file():
            reload_module(f)

    # Watch file changes
    obs = Observer()
    obs.schedule(Handler(), path=current_path, recursive=False)
    obs.start()

    # Watch loop
    try:
        while True:
            await asyncio.sleep(1)
            yield "Watching for file changes..."
    except KeyboardInterrupt:
        obs.stop()
    obs.join()


class Handler(FileSystemEventHandler):
    def on_any_event(self, event):
        reload_module(event.src_path)


def reload_module(path):
    debugpy.debug_this_thread()
    filename = Path(path).name

    if ".py" not in filename or ".tmp" in filename or filename in Path(__file__).name:
        return

    filename = filename.replace(".py", "")

    print(f"Trying to load {filename}")
    try:
        m = importlib.import_module(filename)
        importlib.reload(m)
        print(f"Loaded {filename}")
    except Exception as e:
        print(f"Error: {str(e)} on {filename}")


# Start debug server
debugpy.listen(("localhost", 5678))
