# https://www.tensorflow.org/tutorials/keras/regression
from os import sep
from pickletools import optimize
from tabnanny import verbose
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
import pandas as pd
import numpy as np

# Get datasets from url and manufactorying dataset by columns
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight', 'Acceleration',
                'Model Year', 'Origin']

raw_dataset = pd.read_csv(url, names=column_names,
                          na_values='?', comment='\t',
                          sep=' ', skipinitialspace=True)
dataset = raw_dataset.copy()
print(dataset.all())

print(dataset.isna().sum())
dataset = dataset.dropna()

# encoding columns by in categorical.
dataset['Origin'] = dataset['Origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
dataset = pd.get_dummies(dataset, columns=['Origin'], prefix_sep='')
dataset.tail()

# Split training data and testing data
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# and visualizing train datasets
sns.pairplot(train_dataset[['MPG', 'Cylinders', 'Displacement', 'Weight']], diag_kind='kde')
train_dataset.describe().transpose()

# Split feature form labels
# first of all, copy whole dataset from test dataset to test feature,
# and train dataset to train feature. Lastly, split labels by features
train_feature = train_dataset.copy()
test_feature = test_dataset.copy()

train_label = train_feature.pop('MPG')
test_label = test_feature.pop('MPG')

# normalization on each features.
train_dataset.describe().transpose()[['mean', 'std']]

# normalization layer
normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.array(train_feature))
print(normalizer.mean.numpy())

first_layer = np.array(train_feature[:1])
with np.printoptions(precision=2, suppress=True):
    print("First Example: ", first_layer)
    print()
    print('Normalized :', normalizer(first_layer).numpy())

## https://www.tensorflow.org/tutorials/keras/regression#linear_regression 
horsepower = np.array(train_feature['Horsepower'])

horsepower_normalized = layers.Normalization(input_shape=[1,], axis=None)
horsepower_normalized.adapt(horsepower)

horsepower_model = tf.keras.Sequential([
    horsepower_normalized,
    layers.Dense(units=1)
])

horsepower_model.summary()
horsepower_model.predict(horsepower[:10])

# Model setting up by Adam
horsepower_model.compile(
    optimizer=tf.optimizers.Adam(learning_rate=0.1), 
    loss='mean_absolute_error'
)

# and execute training for 100 epochs
history = horsepower_model.fit(
    train_feature['Horsepower'],
    train_label,
    epochs=100,
    verbose=0,
    validation_split=0.2
)

# training progress using by history object
hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print("###### hist Tail print ######")
print(hist.tail())

def plot_loss(history):
    plt.plot(history.history['loss'], label='loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.ylim([0, 10])
    plt.xlabel('Epoch')
    plt.ylabel('error [MPG]')
    plt.legend()
    plt.grid(True)

plot_loss(history)

test_result = {}
test_result['horsepower_model'] = horsepower_model.evaluate(
    test_feature['Horsepower'],
    test_label, verbose=0
)

x = tf.linspace(0.0, 250, 251)
y = horsepower_model.predict(x)

def plot_horsepower(x, y):
    plt.scatter(train_feature['Horsepower'], train_label, label='Data')
    plt.plot(x, y, color='k', label='Predictions')
    plt.xlabel('Horsepower')
    plt.ylabel('MPG')
    plt.legend()

plot_horsepower(x, y)