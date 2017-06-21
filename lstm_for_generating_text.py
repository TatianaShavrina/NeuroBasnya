
# coding: utf-8

# In[33]:

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.layers.wrappers import TimeDistributed
#import argparse
#from RNN_utils import *

#original architecture written by Trung Tran github.com/ChunML
#https://chunml.github.io/ChunML.github.io/project/Creating-Text-Generator-Using-Recurrent-Neural-Network/

"""# Parsing arguments for Network definition
ap = argparse.ArgumentParser()
ap.add_argument('-data_dir', default='./data/test.txt')
ap.add_argument('-batch_size', type=int, default=50)
ap.add_argument('-layer_num', type=int, default=2)
ap.add_argument('-seq_length', type=int, default=50)
ap.add_argument('-hidden_dim', type=int, default=500)
ap.add_argument('-generate_length', type=int, default=500)
ap.add_argument('-nb_epoch', type=int, default=20)
ap.add_argument('-mode', default='train')
ap.add_argument('-weights', default='')
args = vars(ap.parse_args())"""



# In[40]:

from __future__ import print_function
import numpy as np

# method for generating text
def generate_text(model, length, vocab_size, ix_to_char):
	# starting with random character
	ix = [np.random.randint(vocab_size)]
	y_char = [ix_to_char[ix[-1]]]
	X = np.zeros((1, length, vocab_size))
	for i in range(length):
		# appending the last predicted character to sequence
		X[0, i, :][ix[-1]] = 1
		print(ix_to_char[ix[-1]], end="")
		ix = np.argmax(model.predict(X[:, :i+1, :])[0], 1)
		y_char.append(ix_to_char[ix[-1]])
	return ('').join(y_char)

# method for preparing the training data
def load_data(data_dir, seq_length):
	data = open(data_dir, 'r').read()
	chars = list(set(data))
	VOCAB_SIZE = len(chars)

	print('Data length: {} characters'.format(len(data)))
	print('Vocabulary size: {} characters'.format(VOCAB_SIZE))
	ix_to_char = {ix:char for ix, char in enumerate(chars)}
	char_to_ix = {char:ix for ix, char in enumerate(chars)}
	a = len(data)//seq_length
	X = np.zeros((a, int(seq_length), int(VOCAB_SIZE)), dtype=np.int)
	y = np.zeros((a, int(seq_length), int(VOCAB_SIZE)), dtype=np.int)
	for i in range(0, a):
		X_sequence = data[i*seq_length:(i+1)*seq_length]
		X_sequence_ix = [char_to_ix[value] for value in X_sequence]
		input_sequence = np.zeros((seq_length, VOCAB_SIZE))
		for j in range(seq_length):
			input_sequence[j][X_sequence_ix[j]] = 1.
			X[i] = input_sequence

		y_sequence = data[i*seq_length+1:(i+1)*seq_length+1]
		y_sequence_ix = [char_to_ix[value] for value in y_sequence]
		target_sequence = np.zeros((seq_length, VOCAB_SIZE))
		for j in range(seq_length):
			target_sequence[j][y_sequence_ix[j]] = 1.
			y[i] = target_sequence
	return X, y, VOCAB_SIZE, ix_to_char


# In[41]:

DATA_DIR ="/home/mi_air/Desktop/progr/bot/jew.txt"
BATCH_SIZE = 32
HIDDEN_DIM = 500
SEQ_LENGTH = 80
WEIGHTS = ""
MODE = 'train'

GENERATE_LENGTH = 500
LAYER_NUM = 2

# Creating training data
X, y, VOCAB_SIZE, ix_to_char = load_data(DATA_DIR, SEQ_LENGTH)


# In[45]:

# Creating and compiling the Network
model = Sequential()
model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
for i in range(LAYER_NUM - 1):
    model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    model.add(TimeDistributed(Dense(VOCAB_SIZE)))
    model.add(Activation('softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

# Generate some sample before training to know how bad it is!
generate_text(model, 15, VOCAB_SIZE, ix_to_char)

if not WEIGHTS == '':
    model.load_weights(WEIGHTS)
    nb_epoch = int(WEIGHTS[WEIGHTS.rfind('_') + 1:WEIGHTS.find('.')])
else:
    nb_epoch = 0


# In[ ]:

# Training if there is no trained weights specified
if MODE == 'train' or WEIGHTS == '':
    while True:
        print('\n\nEpoch: {}\n'.format(nb_epoch))
        model.fit(X, y, batch_size=BATCH_SIZE, verbose=1, nb_epoch=1)
        nb_epoch += 1
        generate_text(model, 20, VOCAB_SIZE, ix_to_char)
        if nb_epoch % 10 == 0:
            model.save_weights('/home/mi_air/Desktop/progr/bot/models/jew_checkpoint_layer_{}_hidden_{}_epoch_{}.hdf5'.format(LAYER_NUM, HIDDEN_DIM, nb_epoch))
            json_string = model.to_json()
            with open(r"/home/mi_air/Desktop/progr/bot/models/jew_model.json", "w") as text_file:
                text_file.write(json_string)

# Else, loading the trained weights and performing generation only
elif WEIGHTS == '':
  # Loading the trained weights
    model.load_weights(WEIGHTS)
    generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
    print('\n\n')
else:
    print('\n\nNothing to do!')


# In[ ]:

# Generate some sample  to know how bad it is!
generate_text(model, 15, VOCAB_SIZE, ix_to_char)

