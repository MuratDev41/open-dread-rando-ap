import asyncio
import sys
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, logger
try:
    from CommonClient import gui_loop
except ImportError:
    try:
        from kvui import gui_loop
    except ImportError:
        gui_loop = None
from .Data import ITEM_MAPPING, LOCATION_MAPPING

# Inject an extreme debug hook into Python's asyncio to catch silently swallowed fatal crashes
import asyncio
import traceback
import os

try:
    if not hasattr(asyncio, "_is_md_patched"):
        orig_create_task = asyncio.create_task

        def _debug_create_task(coro, *args, **kwargs):
            task = orig_create_task(coro, *args, **kwargs)
            def _done_callback(t):
                try:
                    err = t.exception()
                    if err:
                        with open("metroid_dread_debug.log", "a") as f:
                            f.write(f"Task crashed containing: {str(coro)}\n")
                            f.write("".join(traceback.format_exception(type(err), err, err.__traceback__)))
                            f.write("-" * 50 + "\n")
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass
            task.add_done_callback(_done_callback)
            return task
        
        asyncio.create_task = _debug_create_task
        asyncio._is_md_patched = True
except Exception:
    pass

class MetroidDreadContext(CommonContext):
    command_processor = ClientCommandProcessor
    game = "Metroid Dread"
    items_handling = 0b111  # All items

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gui_enabled = True # Default to True
        self.game_socket = None
        self.game_host = "127.0.0.1"
        self.game_port = 43000  # Default port for open-dread-rando-exlaunch

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game_host = args.get("game_host", "127.0.0.1")
            self.game_port = args.get("game_port", 43000)
            if hasattr(self, "game_watcher_task") and self.game_watcher_task:
                self.game_watcher_task.cancel()
            self.game_watcher_task = asyncio.create_task(self.game_watcher())
        elif cmd == "ReceivedItems":
            for item in args["items"]:
                self.queue_item_grant(item.item)

    async def game_watcher(self):
        while not self.exit_event.is_set():
            if self.game_socket is None:
                try:
                    self.game_socket, self.writer = await asyncio.open_connection(self.game_host, self.game_port)
                    logger.info(f"Connected to Metroid Dread at {self.game_host}:{self.game_port}")
                    # Request initial state if needed
                except Exception as e:
                    logger.debug(f"Failed to connect to game: {e}")
                    await asyncio.sleep(5)
                    continue

            try:
                data = await self.game_socket.read(4096)
                if not data:
                    self.game_socket = None
                    continue
                
                message = data.decode("utf-8").strip()
                if "LOCATION_CHECKED:" in message:
                    location_key = message.split("LOCATION_CHECKED:")[1]
                    location_id = LOCATION_MAPPING.get(location_key)
                    if location_id:
                        logger.info(f"Location checked: {location_key} (ID: {location_id})")
                        self.locations_checked.add(location_id)
                        await self.send_msgs([{"cmd": "LocationChecks", "locations": [location_id]}])
                    else:
                        logger.warning(f"Unknown location checked in game: {location_key}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Game socket error: {e}")
                self.game_socket = None
        
        if self.game_socket:
            self.game_socket.close()
            self.game_socket = None

    def queue_item_grant(self, ap_item_id):
        item_id = ITEM_MAPPING.get(str(ap_item_id))
        if item_id:
            lua_command = f"RandomizerPowerup.ReceiveItemFromAP('{item_id}', 1)"
            if self.game_socket:
                logger.info(f"Granting item to Samus: {item_id}")
                self.writer.write(lua_command.encode("utf-8") + b"\n")
                asyncio.create_task(self.writer.drain())
        else:
            logger.warning(f"Received unknown Item ID from AP: {ap_item_id}")

async def main(args):
    from CommonClient import get_base_parser, handle_url_arg
    parser = get_base_parser()
    parser.add_argument('url', nargs='?', help='Archipelago binary patch or connection URL')
    args = parser.parse_args(args)

    ctx = MetroidDreadContext(args.connect, args.password)
    ctx.gui_enabled = not getattr(args, 'headless', False)
    ctx.auth = getattr(args, 'name', None)
    
    if args.url:
        url = handle_url_arg(args.url)
        if url:
             ctx.server_address = url

    import colorama
    colorama.init()

    # Fix missing font issues in Kivy
    if ctx.gui_enabled:
        try:
            from kivy.resources import resource_add_path
            import os
            launcher_dir = os.path.dirname(sys.executable)
            data_dir = os.path.join(launcher_dir, "data")
            if os.path.exists(data_dir):
                resource_add_path(data_dir)
        except ImportError:
            pass
    
    # Run the loops
    loop_tasks = [asyncio.create_task(server_loop(ctx))]
    
    if ctx.gui_enabled:
        if hasattr(ctx, "run_gui"):
            loop_tasks.append(asyncio.create_task(ctx.run_gui()))
        elif gui_loop:
            loop_tasks.append(asyncio.create_task(gui_loop(ctx)))
        else:
            logger.error("Could not find GUI loop on context or in CommonClient. Falling back to console.")
            ctx.gui_enabled = False

    if not ctx.gui_enabled:
        if hasattr(ctx, "run_cli"):
            loop_tasks.append(asyncio.create_task(ctx.run_cli()))
        elif hasattr(ctx, "console_loop"):
            loop_tasks.append(asyncio.create_task(ctx.console_loop()))
        elif hasattr(ctx, "input_loop"):
            loop_tasks.append(asyncio.create_task(ctx.input_loop()))
        else:
            logger.warning("No console loop found on context, running in headless mode.")
    
    try:
        await asyncio.wait(loop_tasks, return_when=asyncio.FIRST_COMPLETED)
    except (asyncio.CancelledError, Exception):
        pass
    finally:
        ctx.exit_event.set()

        if ctx.gui_enabled:
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app:
                    app.stop()
                    await asyncio.sleep(0.1) # Let Kivy shutdown gracefully before we cancel its task
            except Exception:
                pass
        
        # Suppress Uncaught Exception noise logged by Archipelago Exception handlers during task cancellation
        import logging
        logging.disable(logging.CRITICAL)

        # Collect any extra tasks created during runtime
        extra_tasks = [t for t in asyncio.all_tasks() if t not in loop_tasks and t is not asyncio.current_task()]
        
        for task in loop_tasks + extra_tasks:
            if not task.done():
                task.cancel()
        
        results = await asyncio.gather(*(loop_tasks + extra_tasks), return_exceptions=True)
        
        logging.disable(logging.NOTSET)
        
        # Expose ANY fatal exceptions that were swallowed during application execution
        for task, result in zip(loop_tasks + extra_tasks, results):
            if isinstance(result, Exception) and not isinstance(result, asyncio.CancelledError):
                name = task.get_name() if hasattr(task, 'get_name') else str(task)
                logging.error(f"Fatal error in task {name}:", exc_info=result)

def launch(args=None):
    if args is None:
        args = []
    try:
        asyncio.run(main(args))
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass

if __name__ == "__main__":
    launch(sys.argv[1:])
