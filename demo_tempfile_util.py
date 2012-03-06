#!/usr/bin/env python
"""A demonstration of tempfile_util.py."""

from __future__ import with_statement
import tempfile_util
import contextlib
import os

def main():
    with contextlib.closing(tempfile_util.TempfileSession(local=True)) as temp_file_session:
        hello_file_name = temp_file_session.temp_file_name('hello', small=False)
        print 'Long temporary name example:', hello_file_name
        hello_file_name = temp_file_session.temp_file_name('hello', small=True)
        print 'Short temporary name example:', hello_file_name
        hello_file = open(hello_file_name, 'w')
        hello_file.write('hello')
        hello_file.close()
        hello_file = open(hello_file_name)
        print hello_file.read()
        hello_file.close()

        hello_file_name = temp_file_session.temp_file_name('hello', contents=1234)
        hello_file = open(hello_file_name)
        print hello_file.read()
        hello_file.close()

    pwd = os.getcwd()
    tempfile_util.run_script("""#!/bin/tcsh
echo hello
echo hello > %(pwd)s/hello.out
touch %(pwd)s/bye.out
""" % locals())
    os.remove('hello.out')
    os.remove('bye.out')



if __name__ == "__main__":
    main()
    
