#!/usr/bin/env python3

import shlex
import argparse

MSG_NA = "n/a"
MSG_NONE = "(none)"
MSG_MAP = {
    "DISTID": ("Distributor ID", "{NAME}", MSG_NA),
    "DISTDESC": ("Description", "{PRETTY_NAME}", MSG_NONE),
    "DISTREL": ("Release", "{VERSION_ID}", MSG_NA),
    "DISTCODE": ("Codename", "{VERSION_CODENAME}", MSG_NA),
}

def read_os_release(os_release_file="/etc/os-release"):
    os_release = {}
    with open(os_release_file, "r") as f:
        for l in shlex.split(f):
            k, _, v = l.partition("=")
            os_release[k] = v
    return os_release

def get_lsb_line(os_release, line_id, short=False):
    msg, osrel_val_tmpl, msg_none = MSG_MAP[line_id]
    try:
        osrel_val = osrel_val_tmpl.format(**os_release)
    except KeyError:
        osrel_val = msg_none
    if short:
        return osrel_val
    else:
        return "{0}:\t{1}".format(msg, osrel_val)

def main():
    lsb_release = argparse.ArgumentParser(description="Distribution information.")
    lsb_release.add_argument("-v", "--version", action="store_true")
    lsb_release.add_argument("-i", "--id", action="append_const", dest="lines", const="DISTID")
    lsb_release.add_argument("-d", "--description", action="append_const", dest="lines", const="DISTDESC")
    lsb_release.add_argument("-r", "--release", action="append_const", dest="lines", const="DISTREL")
    lsb_release.add_argument("-c", "--codename", action="append_const", dest="lines", const="DISTCODE")
    lsb_release.add_argument("-a", "--all", action="store_true", help="Display all of the above information.")
    lsb_release.add_argument("-s", "--short", action="store_true", help="Display all of the above information in short output format.")

    lsb_release_args = lsb_release.parse_args()

    if lsb_release_args.all:
        lsb_lines = MSG_MAP.keys()
    else:
        lsb_lines = lsb_release_args.lines or []

    os_release = read_os_release()

    for i in lsb_lines:
        print(get_lsb_line(os_release, i, lsb_release_args.short))

if __name__ == "__main__":
    main()
