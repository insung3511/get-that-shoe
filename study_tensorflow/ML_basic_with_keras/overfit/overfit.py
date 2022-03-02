from codecs import ignore_errors
from msilib.schema import Feature
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import regularizers

# pip install git+https://github.com/tensorflow/docs
import tensorflow_docs as tfdocs
import tensorflow_docs.modeling
import tensorflow_docs.plots
from IPython import display
from matplotlib import pyplot as plt

import numpy as np
import pathlib
import shutil
import tempfile

logdir = pathlib.Path(tempfile.mkdtemp())/"tensorboard_logs"
shutil.rmtree(logdir, ignore_errors=True)

gz = tf.keras.utils.get_file('HIGGS.csv.gz', 'http://mlphysics.ics.uci.edu/data/higgs/HIGGS.csv.gz')

def pack_row(*row):
    label = row[0]
    features = tf.stack(row[1:], 1)
    return features, label

FEATURES = 28
ds = tf.data.experimental.CsvDataset(gz, [float(),  ])