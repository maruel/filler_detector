#!bin/python3
# Copyright 2021 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import argparse
import sys

import tensorflow as tf


def load_graph(filename):
  with tf.io.gfile.GFile(filename, 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


def load_labels(filename):
  return [line.rstrip() for line in tf.io.gfile.GFile(filename)]


def run_graph(wav_data, labels, input_layer_name, output_layer_name,
              num_top_predictions):
  with tf.compat.v1.Session() as sess:
    # Feed the audio data as input to the graph.
    #   predictions  will contain a two-dimensional array, where one
    #   dimension represents the input image count, and the other has
    #   predictions per class
    softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
    predictions, = sess.run(softmax_tensor, {input_layer_name: wav_data})

    # Sort to show labels in order of confidence
    top_k = predictions.argsort()[-num_top_predictions:][::-1]
    # for node_id in top_k:
    #   human_string = labels[node_id]
    #   score = predictions[node_id]
    #   print('%s (score = %.5f)' % (human_string, score))
    return labels[top_k[0]], predictions[top_k[0]]


def generate_model(good, bad, model):
    #wav, labels, graph, input_name, output_name, how_many_labels):
  """Loads the model and labels, and runs the inference to print predictions."""
  if not wav or not tf.io.gfile.exists(wav):
    tf.compat.v1.logging.fatal('Audio file does not exist %s', wav)

  if not labels or not tf.io.gfile.exists(labels):
    tf.compat.v1.logging.fatal('Labels file does not exist %s', labels)

  if not graph or not tf.io.gfile.exists(graph):
    tf.compat.v1.logging.fatal('Graph file does not exist %s', graph)

  labels_list = load_labels(labels)
  load_graph(graph)
  with open(wav, 'rb') as wav_file:
    wav_data = wav_file.read()
  run_graph(wav_data, labels_list, input_name, output_name, how_many_labels)


def main():
  parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
  parser.add_argument('--good', required=True)
  parser.add_argument('--bad', required=True)
  parser.add_argument('--model', required=True)
  #parser.add_argument('--labels')
  #parser.add_argument('--input_name', default='wav_data:0')
  #parser.add_argument('--output_name', default='labels_softmax:0')
  #parser.add_argument('--how_many_labels', type=int, default=3)
  args = parser.parse_args()
  #tf.compat.v1.app.run(main=main, argv=[sys.argv[0]] + unparsed)
  generate_model(args.good, args.bad, args.model)
  label_wav(args.wav, args.labels, args.graph, args.input_name, args.output_name, args.how_many_labels)
  return 0


if __name__ == '__main__':
  sys.exit(main())
