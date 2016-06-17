
import os
import re
import urllib
import fnmatch
import numpy


# functions for parsing apache HTML dir listings

def list_files(url, pattern=''):
    """ Read html of directory listing, return files as (fname, date, size) """
    line_pattern = re.compile('href="([^"]*)".*(....-..-.. ..:..).*?(\d+[^\s<]*|-)')
    #               look for          a link    +  a timestamp  + a size ('-' for dir)
    try:
        html = urllib.urlopen(url).read()
    except IOError, e:
        print 'error fetching %s: %s' % (url, e)
        return
    if not url.endswith('/'):
        url += '/'
    files = line_pattern.findall(html)
    if pattern != '':
        files = [f for f in files if fnmatch.fnmatch(f[0], pattern)]
    files2 = []
    for fname, date, size in files:
        if size.strip() == '-':
            size = 0
        elif size[-1:] == 'K':
            size = float(size[:-1])
        elif size[-1:] == 'M':
            size = float(size[:-1]) * 1024.0
        files2.append((fname, date, size))
    return files2


def list_dirs(url):
    """ List directories in html dir listing """
    files = list_files(url)
    dirs = []
    for name, date, size in files:
        if name.endswith('/'):
            dirs += [name]
    return dirs


def list_dir_sizes(url, pattern=''):
    """ Get sizes of all directories at this URL """
    dirs = list_dirs(url)
    data = []
    for d in dirs:
        urld = os.path.join(url, d)
        files = list_files(urld, pattern='*.hdf')
        totalsz = numpy.array([f[2] for f in files]).sum()/1024.0/1024.0
        data.append((d, totalsz))
    return data
