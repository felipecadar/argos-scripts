#!/usr/bin/env python3
import subprocess
import shlex

def show(v):
    color = '#cc575d' if v > 75 else '#d19a66' if v > 50 else '#68b382'
    return "<span color='%s'>%3d%%</span>" % (color, v)


def getAvg():
    p = subprocess.Popen(shlex.split("sh -c \"nvidia-smi | grep Default\""), stdout=subprocess.PIPE)
    p.wait()
    l = p.communicate()[0].decode("utf-8")
    avg = int(l.strip().split("|")[-2].strip().split("%")[0])
    return avg

def MoreInfo():
    p = subprocess.Popen(shlex.split("sh -c \"nvidia-smi | grep MiB\""), stdout=subprocess.PIPE)
    p.wait()
    l = p.communicate()[0].decode("utf-8").split("\n")[1:]
    pids = []
    mems = []
    for proc in l:
        info = [x for x in proc.strip().split(" ") if len(x) > 0]
        if len(info) > 0:
            pids.append(info[4])
            mems.append(info[-2])

    return pids, mems

pids, mems = MoreInfo()

print("GPU: %s" % show(getAvg()))
print("---")

for pid, m in zip(pids, mems):
    print("%s / %s" % (pid, m))
