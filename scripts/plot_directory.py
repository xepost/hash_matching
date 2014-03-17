#!/usr/bin/env python
import sys
import pylab
import math
import os
import numpy as np
import string
import matplotlib.pyplot as plt


class Error(Exception):
  """ Base class for exceptions in this module. """
  pass


def normalize_vector(v):
  """ Normalizes the vector v """
  v_max = np.amax(v)
  if v_max == 0.0:
    return v

  v_n = v/np.amax(v);
  return v_n


def calc_match_percentage(h, matches, thresh, size):
  """ Compute the match percentage per hash """
  
  # Sort the hash
  idx = np.argsort(h)
  h = h[idx]
  matches = matches[idx]

  matches_percentage = []
  sum_c_matches = 0
  sum_g_matches = 0
  c = 0
  n = 0
  for i in range(len(matches)):
    sum_c_matches = sum_c_matches + 1
    if (matches[i] >= thresh):
      sum_g_matches = sum_g_matches + 1

    # Reset the counter if needed
    if (c >= args.size):
      matches_percentage.append(100*sum_g_matches/sum_c_matches)
      sum_c_matches = 0
      sum_g_matches = 0
      c = 0;
      n = n + 1

    # Increase the counter
    c = c + 1

  # Convert to numpy and return
  return np.array(matches_percentage)


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(
          description='Show the correspondences between hash and descriptors.',
          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('dir', 
          help='Directory where the user has saved several output files of the hash_matching node.')
  parser.add_argument('-s', '--size', type=int, default=40, 
          help='How many images per bucket.')
  parser.add_argument('-t', '--thresh', type=int, default=300, 
          help='The matching threshold to considerate an image as a success or not.')
  
  args = parser.parse_args()

  # Log
  print "Directory: ", args.dir
  print "Bucket Size: ", args.size
  print "Descriptor Matching Threshold: ", args.thresh

  files_dir = args.dir
  if (files_dir[-1] != "/"):
    files_dir = files_dir + "/"

  # Loop dir
  matches = np.array([])
  h1 = np.array([])
  h2 = np.array([])
  h3 = np.array([])
  for subdir, dirs, files in os.walk(args.dir):
    for file in files:
      data = pylab.loadtxt(files_dir+file, delimiter=',', usecols=(2,3,4,5,6,7,8,9))
      matches = np.concatenate([matches, data[:,0]])
      h1 = np.concatenate([h1, data[:,1]])
      h2 = np.concatenate([h2, data[:,2]])
      h3 = np.concatenate([h3, data[:,3]])

  # Compute the matches percentage
  mp_1 = calc_match_percentage(h1, matches, args.thresh, args.size)
  mp_2 = calc_match_percentage(h2, matches, args.thresh, args.size)
  mp_3 = calc_match_percentage(h3, matches, args.thresh, args.size)

  # Generate the histogram bins
  bins = np.arange(0, len(matches), args.size);
  width = 0.7 * (bins[1] - bins[0])
  center = (bins[:-1] + bins[1:]) / 2

  # Figure
  f1, (ax11, ax12, ax13) = plt.subplots(1, 3, sharey=True)

  # Hash 1
  ax11.plot(np.log(1 + h1), matches, marker='o', ls='')
  ax11.set_title(str(len(matches)) + " Samples (Hash Hyperplanes)")
  ax11.set_xlabel("Hash Matching")
  ax11.set_ylabel("Descriptor Matches")
  ax11.grid(True)

  # Hash 2
  ax12.plot(np.log(1 + h2), matches, marker='o', ls='')
  ax12.set_title(str(len(matches)) + " Samples (Hash Hystogram)")
  ax12.set_xlabel("Hash Matching")
  ax12.grid(True)

  # Hash 3
  ax13.plot(np.log(1 + h3), matches, marker='o', ls='')
  ax13.set_title(str(len(matches)) + " Samples (Hash Projections)")
  ax13.set_xlabel("Hash Matching")
  ax13.grid(True)


  # Figure
  f2, (ax21, ax22, ax23) = plt.subplots(1, 3, sharey=True)

  # Hash 1
  ax21.bar(center, mp_1, align='center', width=width)
  ax21.set_title(str(len(matches)) + " Samples (Hash Hyperplanes)")
  ax21.set_xlabel("Hash Matching")
  ax21.set_ylabel("Success percentage (%)")
  ax21.grid(True)

  # Hash 2
  ax22.bar(center, mp_2, align='center', width=width)
  ax22.set_title(str(len(matches)) + " Samples (Hash Hystogram)")
  ax22.set_xlabel("Hash Matching")
  ax22.grid(True)

  # Hash 3
  ax23.bar(center, mp_3, align='center', width=width)
  ax23.set_title(str(len(matches)) + " Samples (Hash Projections)")
  ax23.set_xlabel("Hash Matching")
  ax23.grid(True)

  plt.show()
