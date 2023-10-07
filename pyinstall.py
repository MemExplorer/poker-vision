from subprocess import call
from symbol import except_clause

class CustomError(Exception):
    pass

def installPip(log=print):
    """
    Pip is the standard package manager for Python. Starting with Python 3.4
    it's included in the default installation, but older versions may need to
    download and install it. This code should pretty cleanly do just that.
    """
    log("Installing pip, the standard Python Package Manager, first")
    from os     import remove
    from urllib.request import urlretrieve
    urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
    call(["python", "get-pip.py"])

    # Clean up now...
    remove("get-pip.py")

def getPip(log=print):
    """
    Pip is the standard package manager for Python.
    This returns the path to the pip executable, installing it if necessary.
    """
    from os.path import isfile, join
    from sys     import prefix
    # Generate the path to where pip is or will be installed... this has been
    # tested and works on Windows, but will likely need tweaking for other OS's.
    # On OS X, I seem to have pip at /usr/local/bin/pip?
    pipPath = join(prefix, 'Scripts', 'pip.exe')
    print("PIP PATH:",pipPath)

    # Check if pip is installed, and install it if it isn't.
    if not isfile(pipPath):
        try:
            installPip(log)
        
        except CustomError as e:
            print(f"Failed to find or install pip!: {e}")
    return pipPath

def install_requirements(req_path, log=print):
    call(['pip', "install", "-r",req_path])