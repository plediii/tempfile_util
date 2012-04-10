# tempfile_util

## Example

This repository contains a utility for cleaning up intermediate files.


Here is an example involving several ways to communicate temporary resources to `tempfile_util`.

```python
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
```


After the above `with` block closes, the files, `foo`, the randomly
named .txt file, and `goodbye` will have been removed.

For debugging purposes, if the the environment variable DELETE=FALSE
is set, the intermediate files will be created and used as normal, but
will not be deleted.


## Installation

Clone `tempfile_util` into your python `site-packages` directory.

```bash
      cd your_python_site-packages
      git clone git://github.com/plediii/tempfile_util
```
