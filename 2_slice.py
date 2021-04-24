#!bin/python3
# Copyright 2021 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Slice an audio file on silence parts"""

import argparse
import os.path
import sys

import pydub


def main():
  # https://ffmpeg.org/ffmpeg-filters.html#silencedetect
  # ffmpeg -hide_banner -i input.mp3 -af silencedetect=n=-50dB:d=0.1 -f null - |& awk '/silencedetect/ {print $4,$5}' | awk '{S=$2;printf "%d:%02d:%02d\n",S/(60*60),S%(60*60)/60,S%60}'

  parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--outdir', default='out')
  parser.add_argument(
      '-c', '--chunk_length', type=int, default=100,
      help='silence chunk in ms')
  parser.add_argument(
      '-d', '--db', type=int, default=-50,
      help='How quiet should the sound be to be considered silent in dBFS')
  args = parser.parse_args()

  if not os.path.isdir(args.outdir):
    os.makedirs(args.outdir)

  song = pydub.AudioSegment.from_file(args.input)

  chunks = pydub.silence.split_on_silence(
    song, min_silence_len=args.chunk_length, silence_thresh=args.db,
  )
  print('Found %d chunks' % len(chunks))
  for i, c in enumerate(chunks):
    c.export(os.path.join(args.outdir, '%d.ogg' % i), format='ogg')
  return 0


if __name__ == '__main__':
  sys.exit(main())
