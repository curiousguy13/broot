# Copyright 2013 Daniel Narvaez
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import sys

from broot.root import Root


def create(mirror=None):
    root = Root()
    root.create(mirror)


def update():
    root = Root()
    root.update()


def clean():
    root = Root()
    root.clean()


def run(command, mirror=None, as_root=False):
    root = Root()

    root.activate()
    try:
        root.run(command, as_root=as_root)
    finally:
        root.deactivate()


def main():
    if not os.geteuid() == 0:
        sys.exit("You must run the command as root")

    os.environ["BROOT"] = "yes"

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    shell_parser = subparsers.add_parser("shell")
    shell_parser.add_argument("--root", action="store_true")

    create_parser = subparsers.add_parser("create")
    create_parser.add_argument("--mirror")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--mirror")
    run_parser.add_argument("--root", action="store_true")

    subparsers.add_parser("update")
    subparsers.add_parser("clean")

    options, other_args = parser.parse_known_args()
    if options.command == "create":
        create(options.mirror)
    elif options.command == "run":
        run(" ".join(other_args), options.mirror, as_root=options.root)
    elif options.command == "shell":
        run("/bin/bash", as_root=options.root)
    elif options.command == "update":
        update()
    elif options.command == "clean":
        clean()
