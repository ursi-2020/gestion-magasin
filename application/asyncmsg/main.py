import sys
import os
sys.dont_write_bytecode = True

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from application.djangoapp.models import *


def main():
    return


if __name__ == '__main__':
    main()
