#!bin/python3
# Copyright 2021 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Help speed up categorizing sliced audio files"""

import argparse
import os.path
import sys

import pydub
import pydub.playback

import natsort

try:
  import msvcrt 
except ImportError:
  msvcrt = None
try:
  import tty
except ImportError:
  tty = None
try:
  import termios
except ImportError:
  termios = None


def getch():
  if sys.platform == 'win32':
    return msvcrt.getch()
  fd = sys.stdin.fileno()
  old = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    return sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
  parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
  parser.add_argument('-o', '--outdir', default='out')
  args = parser.parse_args()

  choices = ('1', '2')
  for v in choices:
    p = os.path.join(args.outdir, v)
    if not os.path.isdir(p):
      os.mkdir(p)

  for i in natsort.sorted(os.listdir(args.outdir)):
    if i in choices:
      continue
    p = os.path.join(args.outdir, i)
    s = pydub.AudioSegment.from_file(p)
    while True:
      print('%s: %s? ' % (i, ', '.join(choices)))
      pydub.playback.play(s)
      v = getch()
      print('%c' % v)
      if v not in choices:
        continue
      os.rename(p, os.path.join(args.outdir, v, i))
      break
  return 0


if __name__ == '__main__':
  sys.exit(main())
