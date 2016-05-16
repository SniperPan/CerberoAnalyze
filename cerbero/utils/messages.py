# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

# messages.py - Uploading msgs to stdout window.

import sys


ACTION_TPL = '-----> %s'
STEP_TPL = '[(%s/%s) %s -> %s ]'


def message(msg):
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()


def error(msg):
    sys.stderr.write(msg + '\n')
    sys.stderr.flush()


def warning(msg):
    error("WARNING: %s" % msg)


def action(msg):
    message(ACTION_TPL % msg)


def build_step(count, total, recipe, step):
    message(STEP_TPL % (count, total, recipe, step))