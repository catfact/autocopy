
import shlex
import sys
import os
from datetime import datetime, timedelta
from subprocess import Popen, PIPE, CalledProcessError

now = datetime.now()
thresh = timedelta(seconds=2)

infile = sys.argv[1]
infile_name, infile_ext = os.path.splitext(infile)
cmd = f"fswatch -x --event Updated --event Removed --event Renamed {infile}"

def make_copy():
    datestr = datetime.now().strftime("%Y%m%d_%H%M%S")
    cpcmd = f"cp {infile} {infile_name}_{datestr}{infile_ext}"
    print(f"copying: {cpcmd}")
    Popen(shlex.split(cpcmd))

def process_event(event_string):
    # ignore everything about the event!
    # print(line, end='') # process line here
    global now
    then = now
    now = datetime.now()
    delta = now - then
    print(delta)
    if delta > thresh:
        make_copy()


with Popen(shlex.split(cmd), stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
        process_event(line)

if p.returncode != 0:
    raise CalledProcessError(p.returncode, p.args)