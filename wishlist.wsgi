activate_this = '/home/kenliau/.virtualenvs/wishlist/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/kenliau/dev/wishlist')

from app import app as application


