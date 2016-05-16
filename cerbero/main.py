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

# hacks -> ./cerbero/cerbero/hacks.py
from cerbero import hacks

try:
# argparse - Parser for command-line options, arguments and sub-commands
# Makes it easy to write user-friendly command-line interfaces. 
# The program defines what arguments it requires, and argparse will figure out how # to parse those out of sys.argv.
# When users give the invalid arguments, it will also automatically generates help # , usage messages and issues errors
    import argparse
except ImportError, e:
    print "Could not import argparse. Try installing it with "\
          "'sudo easy_install argparse"
# @Sniper who will catch this exception?
    raise e

import sys

# errno - Standara errno system symbols
# Makes available standard errno system symbols. The value of each symbol is the 
# corresponding integer value. The names and descriptions are borrowed from 
# linux/include/errno.h, which should be pretty all-inclusive.
import errno

# logging - Logging facility for Python
# Defines functions and classes which implement a flexible event logging system
# for applications and libraries. With logging module, all Python modules can 
# participate in logging
import logging

# traceback - Print or retrieve a stack traceback
# Provides a standard interface to extract, format and print stack traces of 
# Python programs. It exactly mimics the behavior of the Python interpreter when 
# it prints a stack trace.
import traceback
import os

# @Sniper where is the config and commands modules ?
from cerbero import config, commands

# errors -> ./cerbero/cerbero/errors.py
# Each error have one string for description when error occurs
from cerbero.errors import UsageError, FatalError, BuildStepError, \
    ConfigurationError, CerberoException, AbortedError
	
# @Sniper _ N_ user_is_root means what?
from cerbero.utils import _, N_, user_is_root

# @Sniper what does the import as mean?
from cerbero.utils import messages as m

description = N_('Build and package a set of modules to distribute them in '
                 'a SDK')

class Main(object):

	# @Sniper when and where called this __init__
    def __init__(self, args):
        if user_is_root():
            m.warning(_("Running as root"))

        self.check_in_cerbero_shell()
        self.init_logging()
		
		# Create a argument parser with none config .cbc base module argparse
        self.create_parser()
		
		# 
        self.load_commands()
        self.parse_arguments(args)
        self.load_config()
        self.run_command()

    def check_in_cerbero_shell(self):
        if os.environ.get('CERBERO_PREFIX', '') != '':
            self.log_error(_("ERROR: cerbero can't be run "
                             "from a cerbero shell"))

    def log_error(self, msg, print_usage=False, command=None):
        ''' Log an error and exit '''
        if command is not None:
            m.error("***** Error running '%s' command:" % command)
        m.error('%s' % msg)
        if print_usage:
            self.parser.print_usage()
        sys.exit(1)

    def init_logging(self):
        ''' Initialize logging '''
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler())

    def create_parser(self):
        ''' Creates the arguments parser '''
		# argparse.ArgumentParser()
		# Create a new ArgumentParser object, with description init https://docs.python.org/2/library/argparse.html?highlight=argparse.argumentparser#argparse.ArgumentParser.add_argument
        self.parser = argparse.ArgumentParser(description=_(description))

		# Define how a single comand-line argument should be parsed.
        self.parser.add_argument('-c', '--config', action='append', type=str, default=None,
                help=_('Configuration file used for the build'))

    def parse_arguments(self, args):
        ''' Parse the command line arguments '''
        # If no commands, make it show the help by default
        if len(args) == 0:
            args = ["-h"]
        self.args = self.parser.parse_args(args)

    def load_commands(self):
		# Split up functionality into a number of sub-commands, for example, 
		# the svn program can invoke sub-commands like svn checkout, svn update...
        subparsers = self.parser.add_subparsers(help=_('sub-command help'),
                                                dest='command')
												
		# @Sniper where is the commands module ?
        commands.load_commands(subparsers)

    def load_config(self):
        ''' Load the configuration '''
        try:
            self.config = config.Config()
            self.config.load(self.args.config)
        except ConfigurationError, exc:
            self.log_error(exc, False)

    def run_command(self):
        command = self.args.command
        try:
            res = commands.run(command, self.config, self.args)
        except UsageError, exc:
            self.log_error(exc, True, command)
            sys.exit(1)
        except FatalError, exc:
            traceback.print_exc()
            self.log_error(exc, True, command)
        except BuildStepError, exc:
            self.log_error(exc.msg, False, command)
        except AbortedError, exc:
            self.log_error('', False, command)
        except CerberoException, exc:
            self.log_error(exc, False, command)
        except KeyboardInterrupt:
            self.log_error(_('Interrupted'))
        except IOError, e:
            if e.errno != errno.EPIPE:
                raise
            sys.exit(0)

        if res:
            sys.exit(res)


def main():
    Main(sys.argv[1:])


if __name__ == "__main__":
    main()
