"""Main Executor for python -m TEx."""

import sys
import os

# If we are running from a wheel, add the wheel to sys.path
if __package__ == "TEx":

    # __file__ is OSIx/__main__.py
    # first dirname call strips of '/__main__.py'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import pip
    path = os.path.dirname(__file__)
    sys.path.insert(0, path)
    os.chdir(os.path.dirname(__file__))

if __name__ == "__main__":
    # Work around the error reported in #9540, pending a proper fix.
    # Note: It is essential the warning filter is set *before* importing
    #       pip, as the deprecation happens at import time, not runtime.
    from TEx.runner import TelegramMonitorRunner
    sys.exit(TelegramMonitorRunner().main())
