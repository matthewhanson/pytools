
import os
import fnmatch

def find_files(path, pattern='*'):
    """ Recursive find all files in path with pattern """
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches
