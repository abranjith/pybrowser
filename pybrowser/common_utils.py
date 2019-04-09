import os
import platform
import glob
import sys
import shutil
import json
import hashlib
import re
import uuid
try:
    from urllib.parse import urlparse, unquote
except ImportError:
    from urlparse import urlparse, unquote

try:
    import winreg
except ImportError:
    print("IE not available")

from .constants import CONSTANTS

def get_user_home_dir(user=None):
    home_dir = CONSTANTS.DIR_PATH
    if home_dir and os.path.isdir(home_dir):
        return os.path.abspath(home_dir)
    if user:
        home_dir = os.path.expanduser(f"~{user}")
        if os.path.isdir(home_dir):
            return home_dir
    home_dir = os.getenv('HOME') or os.path.expanduser(os.getenv('USERPROFILE'))
    return home_dir

#Ripped from pipenv
def is_valid_url(url):
    if not url:
        return False
    """Checks if a given string is an url"""
    try:
        pieces = urlparse(url)
        return all([pieces.scheme, pieces.netloc])
    except Exception as e:
        return False

#TODO : also handle src is directory
def copy_file(src, dst, overwrite=True):
    if not os.path.isfile(src):
        return
    if overwrite:
        shutil.copy2(src, dst)
    else:
        if os.path.isfile(dst):
            return
        elif os.path.isdir(dst):
            f = os.path.basename(src)
            if os.path.isfile(os.path.join(dst, f)):
                return
        shutil.copy2(src, dst)

def rm_files(files):
    if not isinstance(files, list):
        files = [files]
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

#returns the SHA256 hash
def hash_(data):
    if not data:
        return
    content = data
    #handle filenames
    try:
        if os.path.isfile(data):
            with open(data, "rb") as fd:
                content = fd.read()
    except:
        pass
    #handle json, dicts etc
    if isinstance(data, dict):
        content = json.dumps(data, sort_keys=True, separators=(",", ":"))
    if isinstance(content, bytes):
        return hashlib.sha256(content).hexdigest()
    return hashlib.sha256(content.encode("utf8")).hexdigest()

def guess_filename_from_url(url, has_ext=True):
    if not url:
        return
    s = url.rsplit("/")
    if s and len(s) > 0:
        filename = s[-1]
        filename = unquote(filename)
        filename = "_".join(filename.split())
        if not has_ext:
            return filename
        #return filename only if it is of the format #.#
        ws = [w for w in filename.split(".") if w.strip()]
        if len(ws) > 1:
            return filename

def add_to_osenv(name, path, overwrite=True):
    if (not overwrite) and in_osenv(name):
        return
    try:
        os.environ[name] = path
    except (OSError, KeyError) as e:
        pass

#Adds a given path to the PATH if not already present
def add_to_path(p):
    if in_path(p):
        return
    try:
        os.environ['PATH'] = f"{p}{os.pathsep}{os.environ.get('PATH', '')}"
    except (OSError, KeyError) as e:
        pass

def in_path(p):
    return p in os.environ.get('PATH', '').split(os.pathsep)

def in_osenv(name):
    return True if os.environ.get(name, None) else False

def path_exists(p):
    if not p:
        return False
    if os.path.isdir(p):
        return True
    return file_exists(p)

def file_exists(f):
    if not f:
        return False
    if os.path.isfile(f):
        return True
    #handle filename without extensions
    d = os.path.dirname(f)
    b = os.path.basename(f)
    if not(d and b):
        return False
    for fname in serve_files_in_dir(d, ext=False):
        if fname == b:
            return True
    return False

def dir_filename(p, default_ext=None):
    if not p:
        return
    d = os.path.dirname(p) or ""
    b = os.path.basename(p) or ""
    if b:
        b = os.path.splitext(b)
        if default_ext and not b[1]:
            b = (b[0], default_ext)
        if len(b) == 2:
            b = f"{b[0]}.{b[1].strip('.')}"
        else:
            b = b[0]
    return d, b

def serve_files_in_dir(p, ext=True):
    if not os.path.isdir(p):
        return
    for f in os.listdir(p):
        if os.path.isfile(os.path.join(p, f)):
            if ext:
                yield f
            else:
                yield os.path.splitext(f)[0]

def file_exists_in_path(directory, filename):
    if in_path(directory) and path_exists(os.path.join(directory, filename)):
        return True
    return False

def file_exists_but_not_in_path(directory, filename):
    if not in_path(directory) and path_exists(os.path.join(directory, filename)):
        return True
    return False

def find_patterns_in_str(p, s, first=False):
    empty = lambda : "" if first else []
    if not isinstance(p, str) or not isinstance(s, str):
        return empty()
    pc = re.compile(p)
    l = re.findall(pc, s)
    if not l:
        return empty()
    if first:
        return l[0]
    return l

def os_name():
    if os.name.lower() == "nt":
        return "windows"
    elif os.name.lower() == "posix":
        return "mac"
    else:
        return "linux"

def os_bits():
    #might not work in all OSes
    machine = platform.machine()
    return 64 if machine.endswith("64") else 32

def set_winreg_fromlocalmachine(path, name, value, overwrite=False, dword=True):
    key_type = winreg.REG_DWORD if dword else winreg.REG_SZ
    try:
        current_value = get_winreg_fromlocalmachine(path, name)
        if current_value and (not overwrite):
            return current_value
        k = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_CREATE_SUB_KEY | winreg.KEY_WOW64_64KEY)
        winreg.CloseKey(k)
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_WRITE) as registry_entry:
            winreg.SetValueEx(registry_entry, name, 0, key_type, value)
        return value
    except (WindowsError, OSError) as e:
        #print(str(e))
        return None

def get_winreg_fromlocalmachine(path, name):
    value = None
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ) as registry_entry:
            value, type_id = winreg.QueryValueEx(registry_entry, name)
    except (WindowsError, OSError):
        pass
    return value

def make_dir(name, mode=0o777):
    if not os.path.exists(name):
        os.makedirs(name, mode=mode)
    
def uuid1_as_str():
    return str(uuid.uuid1()).replace("-","_")

def get_unique_filename_from_url(url, ext=None, length_limit=100):
    if not url:
        return
    pieces = urlparse(url)
    parts = []
    if pieces.netloc:
        host = [n for n in pieces.netloc.split(".") 
                if n and n.strip() and (not n.lower().startswith("ww"))]
        parts.append(host[0])
    if pieces.path:
        paths = "_".join([p for p in pieces.path.split("/") if p and p.strip()])
        parts.append(paths)
    filename = "_".join(parts) + "_" + uuid1_as_str()
    filename = unquote(filename)
    filename = "_".join(filename.split())
    #limit filename
    filename = filename[:length_limit]
    if ext:
        return f"{filename}.{ext}"
    else:
        return filename