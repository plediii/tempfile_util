This repository contains a utility for cleaning up intermediate files.
The basic pattern captured by this module is to create multiple
temporary files, perform some external operations, and then remove the
temporary files.  This pattern is used so pervasively in my work, that
it's worthwhile to maintain it in a dedicated module.  As such, it is
a dependency for nearly all my other packages.

I developed this module during my PhD in applied physics at Rice
University.  A common example of its use is when working with
molecular dynamics programs.  In these cases I will create a temporary
file containing an initial molecular geometry, and input files
describing the kind of simulation I want run.  Often, the external
program will create a file containing a molecular dynamics trajectory.
After reading from the output trajectory, all the files output from
the external program are deleted by tempfile_util.

Frequently during debugging sessions, I would like intermediate files
to NOT be deleted.  This is accomplieshed with tempfile_util by
setting the environment variable DELETE=FALSE.  When this environment
variable is set, intermediate files will be created and used as
normal, but not deleted afterward.


For a purely demonstrative and trivial example:


    with open('foo', 'w') as foo_file:
    	 foo_file.write('foo this world')


     with TempfileSession(['foo']) as tfs:
     
          # this creates a random unique file name with suffix 'txt', in /tmp or wherever appropriate.
     	  hello_txt_name = tfs.temp_file_name('.txt') 

	  with open(hello_txt_name, 'w') as hello_file:
     	       hello_file.write('hello world')


     	  with open('goodbye', 'w') as goodbye_file:
     	       hello_file.write('goodbye world')

	  tfs.add_name('goodbye')


After the above ``with'' block closes, the files, 'foo', the randomly
named .txt file, and 'goodbye' will have been removed.

	 

