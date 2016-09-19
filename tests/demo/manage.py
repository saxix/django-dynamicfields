#!/usr/bin/env PYTHONWARNINGS=ignore python
import os
import sys

ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, ROOT)

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoproject.settings')
    import logging

    l = logging.getLogger('raven.contrib.django.client.DjangoClient')

    from django.core.management import execute_from_command_line

    debug_on_error = '--pdb' in sys.argv
    args = [a for a in sys.argv if a != '--pdb']

    try:
        execute_from_command_line(args)
    except:
        if debug_on_error:
            import pdb, traceback
            type, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
        else:
            raise
