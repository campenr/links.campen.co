# Copyright 2016 Richard Campen
# All rights reserved
# This software is released under the Modified BSD license
# See LICENSE.txt for the full license documentation

"""Simple Flask application for creating/managing shortened URLs.

# LinkShortener 1.0.0

For complete documentation see README.md.
"""

from LinkShortener import app

if __name__ == '__main__':
    app.run(debug=True)