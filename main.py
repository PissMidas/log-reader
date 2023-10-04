from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import pygetwindow

def is_omega_strikers_window_open():
    game_title = "OmegaStrikers"
    windows = pygetwindow.getAllWindows()
    for window in windows:
        if game_title in window.title:
            return True
    return False

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)

class LogEventHandler(FileSystemEventHandler):
    def __init__(self, log_file_path):
        super().__init__()
        self.log_file_path = log_file_path
        self.file_size = 0

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.log_file_path:
            # Get the size of the modified file
            current_size = os.path.getsize(self.log_file_path)

            # Read only the newly added content since the last modification
            with open(self.log_file_path, "r") as file:
                file.seek(self.file_size)
                new_content = file.read()

            # Update the file size
            self.file_size = current_size

            # Process the new log messages
            log_lines = new_content.splitlines()
            for line in log_lines:
                #if 'Training Class' in line or 'Application Will Terminate' in line or 'PostGameCelebration' in line:
                    #this if statement acts as a whitelister. add more to let more messages from the .log file through.

                print(line) #USED FOR DEBUGGING, OR CALL SOME OTHER FUNCTION HERE, SUCH AS MESSAGING WITH A PIPE OR SOCKET.
                if 'Application Will Terminate' in line:
                    print("Omega Strikers is shutting down. also shutting down this observer program")
                    print("this code is being terminated with os._exit(0). please consider changing this in a production setting!")
                    os._exit(0)  # Terminates the program without cleanup. TODO please change this!

if __name__ == "__main__":

    if is_omega_strikers_window_open()== False:
        print("terminating this program because game is not open. try again once you have omega strikers open!")
        sys.exit()
    # Creates the file path to the logs. functionally equivalent to "%LOCALAPPDATA%/OmegaStrikers/Saved/Logs/OmegaStrikers.log"
    log_file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'OmegaStrikers', 'Saved', 'Logs', 'OmegaStrikers.log')

    # Create an instance of LogEventHandler
    log_handler = LogEventHandler(log_file_path)
    time.sleep(1)
    # Create the watchdog observer and start monitoring
    observer = Observer()
    time.sleep(1)
    observer.schedule(log_handler, os.path.dirname(log_file_path), recursive=False)
    time.sleep(1)
    observer.start()

    print("press Control + C to terminate")
    try:
        while True:
            # Keep the script running indefinitely
            time.sleep(1)
    except:
        # Stop the observer when the user presses Ctrl+C
        observer.stop()


    observer.join()  # Wait for the observer thread to finish gracefully
