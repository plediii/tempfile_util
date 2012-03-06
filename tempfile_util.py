"""Utilities for working with tempfiles.

The purpose of this module is to provide unique file names which are
often deleted immediately after use.  I use this module instead of the
standard tempfile, because I don't like the semantics of that module,
particularly the inability to let a third party process use the
temporary files. """

from __future__ import with_statement

import contextlib
import tempfile
import os
import os.path
import stat
import uuid

dir = tempfile.gettempdir()

def temp_file_name(suffix, local=False, small=False):
    """Return a new temporary file name."""
    global dir
    name = str(uuid.uuid4())
    if small:
        name = name.split('-')[0]
    if local:
        return 'tmp%s%s' % (name, suffix)
    else:
        return '%s/tmp%s%s' % (dir, name, suffix)

class TempfileSession():

    # There is probably no reason to maintain the list of tentative file names
    def __init__(self, tentative_file_names=[], local=False, delete=True, small=False,
		 delete_on_exception=False):
        self.tentative_file_names=tentative_file_names
        self.__temp_file_names = []
        if os.getenv('DELETE') == 'FALSE':
            self._local = True
            self._delete = False
            self._small = True
        else:
            self._local = local
            self._delete = delete
            self._small = small

	self.delete_on_exception = delete_on_exception

    def __enter__(self):
        return self

    def __exit__(self, *args):
	no_exception_occured = all(arg is None for arg in args)

	if self.delete_on_exception or no_exception_occured:
	    self.__temp_file_names.extend(self.tentative_file_names)
	    self.close()
        elif not no_exception_occured:
            print 'Not deleting temporary files because of exception.'
            

	return False
	

    def close(self):
        for filename in self.__temp_file_names:
            if os.path.exists(filename):
                os.remove(filename)

    def new_name(self, suffix, keep=None, local=None, small=None):
        is_local = (local == None and self._local) or local
        small = (small == None and self._small) or small
        new_temp_file_name = temp_file_name(suffix, local=is_local, small=small)
        if (keep == None and self._delete) or (keep != None and not keep):
            self.__temp_file_names.append(new_temp_file_name)
        return new_temp_file_name

    def add_name(self, name):
        self.__temp_file_names.append(name)

    def temp_file(self, suffix, mode='w+b', keep=None, local=None, small=None):
        new_temp_file_name = self.new_name(suffix, keep, local, small)
        new_temp_file = open(new_temp_file_name, mode)
        return new_temp_file
    
    def temp_file_name(self, suffix, contents=None, keep=None, local=None, small=None):
        new_temp_file = self.temp_file(suffix, keep=keep, local=local, small=small)
        if contents:
            new_temp_file.write(str(contents))
        new_temp_file.close()
        return new_temp_file.name

    def temp_script_name(self, suffix, contents=None, keep=None, local=None, small=None):
        script_file_name = self.temp_file_name(suffix, contents=contents, keep=keep, local=local)
        os.chmod(os.path.realpath(script_file_name), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        return script_file_name        

    def run_script(self, contents, suffix='script', keep=None, local=None, small=None):
        script_file_name = self.temp_script_name(suffix, contents=contents, keep=keep, local=local, small=small)
        os.system(os.path.realpath(script_file_name))

    def keep_name(self, file_name):
        if file_name in self.__temp_file_names:
            self.__temp_file_names.remove(file_name)
        if file_name in self.tentative_file_names:
            self.tenative_file_names.remove(file_name)

    def keep_file(self, file):
        self.keep_name(file.name)

    def keep_all(self):
        self.tenative_file_names = []
        self.__temp_file_names = []

    def tentative_file_name(self, file_name):
        self.tentative_file_names.append(file_name)


Session=TempfileSession

def run_script(contents, suffix='', keep=None, local=None):
    """Dump the contents to a temp file and execute."""
    with contextlib.closing(TempfileSession()) as temp_file_session:
        temp_file_session.run_script(contents, suffix, keep, local=local)


class TempFileCase(object):
    """A mixin for unittests."""

    def setUp(self):
        super(TempFileCase, self).setUp()
        self.tfs = TempfileSession(local=True, small=True)
        
    def tearDown(self):
        self.tfs.close()
        super(TempFileCase, self).setUp()
