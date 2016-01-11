import subprocess
import os
import inspect
import sys

def set_path_if_library_not_available(command,path,message):
    try:
        subprocess.Popen(command)
    except OSError:
        try:
            # Make the path absolute from the caller, if it isn't already
            if not os.path.isabs(path):
                caller_path = os.path.dirname(inspect.getfile(sys._getframe(1)))
                path = os.path.join(caller_path, path)
    
            # Set the path specified for the command into the os path
            os.environ["PATH"] += os.pathsep + path
            
            subprocess.Popen(command)
        except OSError:
            raise EnvironmentError(message)
