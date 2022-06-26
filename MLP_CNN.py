# -*- coding: utf-8 -*-
"""Proyecto_Final_SML_MLP_CNN

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11ssBJiLi76po2mR20ulB2UbsJsGfyy6x

# Librerias Utilizadas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import Input

from tensorflow.keras import regularizers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD
from sklearn.metrics import classification_report, confusion_matrix

# Impoorting data from drive
from google.colab import drive

# Conectar con google drive (Es necesario tener la carpeta compartida)
from google.colab import drive
drive.mount('/content/drive')

"""# MINST: Datos"""

# Upload data
csv = ["MNISTtest_9000.csv", "MNISTtrain_40000.csv", "MNISTvalidate_11000.csv"]
carpet = "/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/"
MNISTtest_9000, MNISTtrain_40000, MNISTvalidate_11000 = [pd.read_csv(carpet + i) for i in csv]

def PrePross(df):
  '''
  Separa los dataframes en inputs y outputs
  '''
  input = np.array([np.array(i[1] / 255).reshape(28*28,)   for i in df.iloc[:,:-1].iterrows()])
  output = to_categorical(pd.Categorical(df.iloc[:,-1]))
  output_lab = np.array(df.iloc[:,-1]).reshape(len(df.iloc[:,-1]), 1)

  return input, output, output_lab

input_train, output_train, lab_train = PrePross(MNISTtrain_40000)
input_test, output_test, lab_test = PrePross(MNISTtest_9000)
validate = MNISTvalidate_11000

n_rows = 2
n_cols = 15

class_names = [i for i in range(10)]
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))

for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols*row + col
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(input_train[index].reshape(28,28), cmap="binary")
        plt.axis('off')
        plt.title(lab_train[index].squeeze(), fontsize=12)

plt.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()

print(input_train.shape, output_train.shape, lab_train.shape)
print(input_test.shape, output_test.shape, lab_test.shape)

# Función que grafica la matriz de confusión
import itertools

#Note, this code is taken straight from the SKLEARN website, an nice way of viewing confusion matrix.
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues, ):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure(figsize=(5.5, 5.5))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar(shrink = 0.6)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Funcion que te devuelve los errores
def Errores(model,y_train, y_test, lab_test , X_train, X_test):

  score = model.evaluate(y_train, y_test, verbose=0)
  print('Test loss:', score[0])
  print('Test accuracy:', score[1])
  print('Test error:', 1-score[1])
  print('\n')
  scoret = model.evaluate(X_train, X_test, verbose=0)
  print('Loss:', scoret[0])
  print('Accuracy:', scoret[1])
  print('Error:', 1 - scoret[1])
  #Classification report
  LR_pred = model.predict(y_train)
  LR_pred_c = np.argmax(LR_pred, axis=1).reshape(lab_test.shape)
  target_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  print('Classification Report')
  report = classification_report(lab_test, LR_pred_c, target_names=target_names,output_dict = False)
  print(report)
  """
  error_per_class = list()
  for k,v in report.items():
    try:
      error_per_class.append(v['precision'])
    except TypeError:
      break
  error_per_class = np.array(error_per_class)
  error_per_class = np.around(error_per_class,2)
  """
  cm = confusion_matrix(lab_test, LR_pred_c)
  plot_confusion_matrix(cm, target_names, normalize=False, title='Confusion Matrix')

"""# MNIST: Logistic Regression"""

LR = Sequential()
LR.add(Input(shape=784))
LR.add(Dense(units = 10, kernel_regularizer= regularizers.L1(0.001),activation="softmax"))

LR.compile(loss="sparse_categorical_crossentropy",
              optimizer="rmsprop",
              metrics=["accuracy"])

LR.h = LR.fit(input_train.reshape(40000, 784), lab_train,
              epochs=30, validation_data=(input_test, lab_test))

# Errores de la regresión logística, la función Errores no funciona en este modelo
  score = LR.evaluate(input_test, lab_test, verbose=0)
  print('Test loss:', score[0])
  print('Test accuracy:', score[1])
  print('Test error:', 1-score[1])
  print('\n')
  scoret = LR.evaluate(input_train, lab_train, verbose=0)
  print('Loss:', scoret[0])
  print('Accuracy:', scoret[1])
  print('Error:', 1 - scoret[1])
  LR_pre = LR.predict(input_test)
  LR_pre_c = np.argmax(LR_pre, axis=1).reshape(lab_test.shape)
  target_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  print('Classification Report')
  report = classification_report(lab_test, LR_pre_c, target_names=target_names,output_dict = False)
  print(report)

"""# MINST: MLP's Models (Activation Functions)"""

np.random.seed(1997)

"""## MLP_relu"""

# Instantiate a sequential model
MLP_1 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_1.add(Dense(100, input_shape=(28*28,), activation='relu'))
MLP_1.add(Dropout(0.2))
MLP_1.add(Dense(50, activation='relu'))
MLP_1.add(Dropout(0.2))  
MLP_1.add(Dense(25, activation='relu'))
MLP_1.add(Dropout(0.2))

# Add a dense layer with as many neurons as competitors
MLP_1.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_1.compile(loss="categorical_crossentropy",
              optimizer="sgd",
              metrics=['accuracy'])

monitor_val_acc = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint = ModelCheckpoint("MLP_1.hdf5", save_best_only = True)

model = MLP_1.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc, modelCheckpoint])

Errores(MLP_1, input_test, output_test, lab_test, input_train, output_train)

"""## MLP_selu"""

# Instantiate a sequential model
MLP_2 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_2.add(Dense(100, input_shape=(28*28,), activation='selu'))
MLP_2.add(Dropout(0.2))
MLP_2.add(Dense(50, activation='selu'))
MLP_2.add(Dropout(0.2))  
MLP_2.add(Dense(25, activation='selu'))
MLP_2.add(Dropout(0.2))

# Add a dense layer with as many neurons as competitors
MLP_2.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_2.compile(loss="categorical_crossentropy",
              optimizer="sgd",
              metrics=['accuracy'])

monitor_val_acc_2 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_2 = ModelCheckpoint("MLP_2.hdf5", save_best_only = True)

model_2 = MLP_2.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_2, modelCheckpoint_2])

Errores(MLP_2, input_test, output_test, lab_test, input_train, output_train)

"""## MLP_tanh"""

# Instantiate a sequential model
MLP_3 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_3.add(Dense(100, input_shape=(28*28,), activation='tanh'))
MLP_3.add(Dropout(0.2))
MLP_3.add(Dense(50, activation='tanh'))
MLP_3.add(Dropout(0.2))  
MLP_3.add(Dense(25, activation='tanh'))
MLP_3.add(Dropout(0.2))

# Add a dense layer with as many neurons as competitors
MLP_3.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_3.compile(loss="categorical_crossentropy",
              optimizer="sgd",
              metrics=['accuracy'])

monitor_val_acc_3 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_3 = ModelCheckpoint("MLP_3.hdf5", save_best_only = True)

model_3 = MLP_3.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_3, modelCheckpoint_3])

Errores(MLP_3, input_test, output_test, lab_test, input_train, output_train)

"""## MLP_sigmoid"""

# Instantiate a sequential model
MLP_4 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_4.add(Dense(100, input_shape=(28*28,), activation='sigmoid'))
MLP_4.add(Dropout(0.2))
MLP_4.add(Dense(50, activation='sigmoid'))
MLP_4.add(Dropout(0.2))  
MLP_4.add(Dense(25, activation='sigmoid'))
MLP_4.add(Dropout(0.2))

# Add a dense layer with as many neurons as competitors
MLP_4.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_4.compile(loss="categorical_crossentropy",
              optimizer="sgd",
              metrics=['accuracy'])

monitor_val_acc_4 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_4 = ModelCheckpoint("MLP_4.hdf5", save_best_only = True)

model_4 = MLP_4.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_4, modelCheckpoint_4])

Errores(MLP_4, input_test, output_test, lab_test, input_train, output_train)

"""## Visualization"""

fig, ax = plt.subplots(2,3, figsize = (15,15))

## PAIRS
# 
ax[0,0].plot(model.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
ax[0,0].plot(model.history["val_loss"], color = "black", linestyle = "--", alpha = 0.5)
ax[0,0].plot(model.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
ax[0,0].plot(model.history["val_accuracy"], color = "red", linestyle = "--", alpha = 0.5)
ax[0,0].legend(['loss_Train', 'loss_Test',"accuracy_Train", "val_accuracy_Test"], loc='upper right')
ax[0,0].set_title('ReLu')

#
ax[1,0].plot(model_2.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
ax[1,0].plot(model_2.history["val_loss"], color = "black", linestyle = "--", alpha = 0.5)
ax[1,0].plot(model_2.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
ax[1,0].plot(model_2.history["val_accuracy"], color = "red", linestyle = "--", alpha = 0.5)
ax[1,0].legend(['loss_Train', 'loss_Test',"accuracy_Train", "val_accuracy_Test"], loc='center')
ax[1,0].set_title('SeLu')

#
ax[1,2].plot(model_3.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
ax[1,2].plot(model_3.history["val_loss"], color = "black", linestyle = "--", alpha = 0.5)
ax[1,2].plot(model_3.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
ax[1,2].plot(model_3.history["val_accuracy"], color = "red", linestyle = "--", alpha = 0.5)
ax[1,2].legend(['loss_Train', 'loss_Test',"accuracy_Train", "val_accuracy_Test"], loc='center')
ax[1,2].set_title('tanh')

#
ax[0,2].plot(model_4.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
ax[0,2].plot(model_4.history["val_loss"], color = "black", linestyle = "--", alpha = 0.5)
ax[0,2].plot(model_4.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
ax[0,2].plot(model_4.history["val_accuracy"], color = "red", linestyle = "--", alpha = 0.5)
ax[0,2].legend(['loss_Train', 'loss_Test',"accuracy_Train", "val_accuracy_Test"], loc='upper right')
ax[0,2].set_title('sigmoid')

## Compare
#
ax[0,1].plot(model.history["val_loss"], color = "green", linestyle = "--", alpha = 0.5)
ax[0,1].plot(model_2.history["val_loss"], color = "blue", linestyle = "--", alpha = 0.5)
ax[0,1].plot(model_3.history["val_loss"], color = "grey", linestyle = "--", alpha = 0.5)
ax[0,1].plot(model_4.history["val_loss"], color = "purple", linestyle = "--", alpha = 0.5)
ax[0,1].legend(['Relu', 'SeLu',"TanH", "Sigmoid"], loc='upper right')
ax[0,1].set_title('Comparacion val_loss')
#
ax[1,1].plot(model.history["val_accuracy"], color = "green", linestyle = "--", alpha = 0.5)
ax[1,1].plot(model_2.history["val_accuracy"], color = "blue", linestyle = "--", alpha = 0.5)
ax[1,1].plot(model_3.history["val_accuracy"], color = "grey", linestyle = "--", alpha = 0.5)
ax[1,1].plot(model_4.history["val_accuracy"], color = "purple", linestyle = "--", alpha = 0.5)
ax[1,1].legend(['Relu', 'SeLu',"TanH", "Sigmoid"], loc='upper right')
ax[1,1].set_title('Comparacion val_accuracy')


plt.show()

"""# MINST: MLP's Models (Architecture)

## DNN1
"""

# Instantiate a sequential model
MLP_5 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_5.add(Dense(200, input_shape=(28*28,), activation='relu'))
MLP_5.add(Dropout(0.4))
MLP_5.add(Dense(100, activation='relu'))
MLP_5.add(Dropout(0.4))
MLP_5.add(Dense(50, activation='relu'))
MLP_5.add(Dropout(0.4))  
# Add a dense layer with as many neurons as competitors
MLP_5.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_5.compile(loss="categorical_crossentropy",
              optimizer="sgd",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_5.hdf5", save_best_only = True)

model_5 = MLP_5.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_5, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_5.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_5.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_5.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_5.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN2

"""

# Instantiate a sequential model
MLP_6 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_6.add(Dense(200, input_shape=(28*28,), activation='relu'))
MLP_6.add(Dropout(0.4))
MLP_6.add(Dense(40, activation='relu'))
MLP_6.add(Dropout(0.4))
MLP_6.add(Dense(40, activation='selu'))
MLP_6.add(Dropout(0.4))
MLP_6.add(Dense(40, activation='tanh'))
MLP_6.add(Dropout(0.4))  
# Add a dense layer with as many neurons as competitors
MLP_6.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_6.compile(loss="categorical_crossentropy",
              optimizer="sgd",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_6.hdf5", save_best_only = True)

model_6 = MLP_6.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_6, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_6.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_6.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_6.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_6.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN3

"""

# Instantiate a sequential model
MLP_7 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_7.add(Dense(120, input_shape=(28*28,), activation='relu'))
MLP_7.add(Dropout(0.45))
MLP_7.add(Dense(50, activation='selu'))
MLP_7.add(Dropout(0.35))
MLP_7.add(Dense(50, activation='relu'))
MLP_7.add(Dropout(0.25)) 
# Add a dense layer with as many neurons as competitors
MLP_7.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_7.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_7.hdf5", save_best_only = True)

model_7 = MLP_7.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_7, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_7.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_7.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_7.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_7.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN4

"""

# Instantiate a sequential model
MLP_8 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_8.add(Dense(180, input_shape=(28*28,), activation='relu'))
MLP_8.add(Dropout(0.45))
MLP_8.add(Dense(60, activation='tanh'))
MLP_8.add(Dropout(0.35))
MLP_8.add(Dense(60, activation='relu'))
MLP_8.add(Dropout(0.25)) 
# Add a dense layer with as many neurons as competitors
MLP_8.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_8.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_8.hdf5", save_best_only = True)

model_8 = MLP_8.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_8, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_8.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_8.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_8.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_8.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN5

"""

# Instantiate a sequential model
MLP_9 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_9.add(Dense(170, input_shape=(28*28,), activation='relu'))
MLP_9.add(Dropout(0.45))
MLP_9.add(Dense(40, activation='relu'))
MLP_9.add(Dropout(0.20))
MLP_9.add(Dense(40, activation='relu'))
MLP_9.add(Dropout(0.20)) 
MLP_9.add(Dense(20, activation='sigmoid'))
MLP_9.add(Dropout(0.15)) 
# Add a dense layer with as many neurons as competitors
MLP_9.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_9.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_9.hdf5", save_best_only = True)

model_9 = MLP_9.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_9, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_7.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_7.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_7.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_7.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN6

"""

# Instantiate a sequential model
MLP_10 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_10.add(Dense(190, input_shape=(28*28,), activation='relu'))
MLP_10.add(Dropout(0.40))
MLP_10.add(Dense(60, activation='selu'))
MLP_10.add(Dropout(0.25))
MLP_10.add(Dense(30, activation='sigmoid'))
MLP_10.add(Dropout(0.20)) 

# Add a dense layer with as many neurons as competitors
MLP_10.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_10.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_10.hdf5", save_best_only = True)

model_10 = MLP_10.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_10, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_10.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_10.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_10.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_10.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN7

"""

# Instantiate a sequential model
MLP_11 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_11.add(Dense(110, input_shape=(28*28,), activation='relu'))
MLP_11.add(Dropout(0.40))
MLP_11.add(Dense(55, activation='relu'))
MLP_11.add(Dropout(0.35))
# Add a dense layer with as many neurons as competitors
MLP_11.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_11.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_11.hdf5", save_best_only = True)

model_11 = MLP_11.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_11, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_11.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_11.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_11.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_11.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## DNN8

"""

# Instantiate a sequential model
MLP_12 = Sequential()
  
# Add 3 dense layers of 128, 64 and 32 neurons each
MLP_12.add(Dense(200, input_shape=(28*28,), activation='relu'))
MLP_12.add(Dropout(0.40))
MLP_12.add(Dense(100, activation='relu'))
MLP_12.add(Dropout(0.35))
MLP_12.add(Dense(50, activation='relu'))
MLP_12.add(Dropout(0.30))
MLP_12.add(Dense(25, activation='tanh'))
MLP_12.add(Dropout(0.30))
# Add a dense layer with as many neurons as competitors
MLP_12.add(Dense(10, activation="softmax"))
  
# Compile your model using categorical_crossentropy loss
MLP_12.compile(loss="categorical_crossentropy",
              optimizer="adam",
              metrics=['accuracy'])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("MLP_12.hdf5", save_best_only = True)

model_12 = MLP_12.fit(input_train, output_train, 
           epochs=500, validation_data=(input_test, output_test), 
          callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(MLP_12, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_12.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_12.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_12.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_12.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

"""## ¿Que salio mal?"""

pred = [i.argmax() for i in MLP_12.predict(input_test)]
compare = lab_test.squeeze() != np.array(pred)
index_error = np.where(compare)[0]
hard_prediction = [input_test[i] for i in index_error]

n_rows = 2
n_cols = 21

class_names = [i for i in range(10)]
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))

for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols*row + col
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(hard_prediction[index].reshape(28,28), cmap="binary")
        plt.axis('off')
        plt.title(lab_test[index_error][index].squeeze(), fontsize=12)

plt.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()

"""# MNIST: CNN Models

## PreProcess
"""

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Para estas arquitecturas es necesario redimensionar el train a (28, 28, 1) 
def PreProssConv(df):
  '''
  Separa los dataframes en inputs y outputs
  '''
  input = np.array([np.array(i[1] / 255).reshape(28,28)   for i in df.iloc[:,:-1].iterrows()])
  output = to_categorical(pd.Categorical(df.iloc[:,-1]))
  output_lab = np.array(df.iloc[:,-1]).reshape(len(df.iloc[:,-1]), 1)
  
  return input, output, output_lab

input_train, output_train, lab_train = PreProssConv(MNISTtrain_40000)
input_test, output_test, lab_test = PreProssConv(MNISTtest_9000)

# No correr más de una vez
input_train = np.expand_dims(input_train, -1)
input_test = np.expand_dims(input_test, -1)
print("input_train shape:", input_train.shape)
print("input_test shape:", input_test.shape)
print(input_train.shape[0], "train samples")
print('output_train shape:', output_train.shape)
print('output_test shape:', output_test.shape)
print(input_test.shape[0], "test samples")

"""## CNN_1"""

CNN1 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(10, activation="softmax"),
    ]
)

CNN1.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=5)
modelCheckpoint_0 = ModelCheckpoint("CNN1.hdf5", save_best_only = True)

model_13 = CNN1.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN1, input_test, output_test, lab_test, input_train, output_train)

model_13 = model_12
fig, ax = plt.subplots( figsize = (8,8))

plt.plot(model_13.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_13.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_13.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_13.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

CNN1.summary()

"""## CNN_2"""

CNN2 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(10, activation="softmax"),
    ]
)
CNN2.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=4)
modelCheckpoint_0 = ModelCheckpoint("CNN2.hdf5", save_best_only = True)

model_14 = CNN2.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN2, input_test, output_test, lab_test, input_train, output_train)

fig, ax = plt.subplots( figsize = (6,6))

plt.plot(model_14.history["val_accuracy"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_14.history["accuracy"], color = "red", linestyle = "-", alpha = 0.5)
plt.plot(model_14.history["loss"], color = "black", linestyle = "-", alpha = 0.5)
plt.plot(model_14.history["val_loss"], color = "red", linestyle = "-", alpha = 0.5)

CNN2.summary()

"""## CNN_3"""

CNN3 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dense(10, activation="softmax"),
    ]
)

CNN3.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=4)
modelCheckpoint_0 = ModelCheckpoint("CNN3.hdf5", save_best_only = True)

model_15 = CNN3.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN3, input_test, output_test, lab_test, input_train, output_train)

CNN3.summary()

"""## CNN_4"""

CNN4 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax"),
    ]
)

CNN4.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=4)
modelCheckpoint_0 = ModelCheckpoint("CNN4.hdf5", save_best_only = True)

model_16 = CNN4.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN4, input_test, output_test, lab_test, input_train, output_train)

pd.DataFrame(model_16.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

CNN4.summary()

"""## CNN_5"""

CNN5 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.2),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax"),
    ]
)

CNN5.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=4)
modelCheckpoint_0 = ModelCheckpoint("CNN5.hdf5", save_best_only = True)

model_17 = CNN5.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN5, input_test, output_test, lab_test, input_train, output_train)

pd.DataFrame(model_17.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

CNN5.summary()

# This one seems to be the best model so far

"""## CNN_6"""

CNN6 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.2),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.3),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax"),
    ]
)

CNN6.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=4)
modelCheckpoint_0 = ModelCheckpoint("CNN6.hdf5", save_best_only = True)

model_18 = CNN6.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN6, input_test, output_test, lab_test, input_train, output_train)

pd.DataFrame(model_18.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

CNN6.summary()

"""## CNN_7"""

CNN7 = keras.Sequential(
    [
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.2),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.3),
        layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
        layers.Dropout(0.3),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax"),
    ]
)

CNN7.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

monitor_val_acc_0 = EarlyStopping(monitor='val_accuracy', 
                       patience=4)
modelCheckpoint_0 = ModelCheckpoint("CNN7.hdf5", save_best_only = True)

model_19 = CNN7.fit(input_train, output_train, batch_size=128, epochs=200, validation_split=0.1
                    ,callbacks = [monitor_val_acc_0, modelCheckpoint_0])

Errores(CNN7, input_test, output_test, lab_test, input_train, output_train)

pd.DataFrame(model_19.history).plot(figsize=(8, 5))
plt.grid(True)
plt.gca().set_ylim(0, 1)
plt.show()

CNN7.summary()

"""##¿Que salio mal?"""

pred = [i.argmax() for i in CNN5.predict(input_test)]
compare = lab_test.squeeze() != np.array(pred)
index_error = np.where(compare)[0]
hard_prediction = [input_test[i] for i in index_error]

n_rows = 5
n_cols = 15

class_names = [i for i in range(10)]
plt.figure(figsize=(n_cols * 1.2, n_rows * 1.2))

for row in range(n_rows):
    for col in range(n_cols):
        index = n_cols*row + col
        plt.subplot(n_rows, n_cols, index + 1)
        plt.imshow(hard_prediction[index].reshape(28,28), cmap="binary")
        plt.axis('off')
        plt.title(lab_test[index_error][index].squeeze(), fontsize=12)

plt.subplots_adjust(wspace=0.2, hspace=0.5)
plt.show()

len(index_error)

"""# Best Model Predictions"""

val_data = np.array([np.array(i[1] / 255).reshape(28*28,)   for i in validate.iterrows()])

"""## Logistic Regression Pred"""

LR_pred = LR.predict(val_data.reshape(11000,784))
LR_pred = np.argmax(LR_pred, axis=1)
LR_pred = pd.DataFrame(LR_pred).transpose()
LR_pred.to_csv("/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/LR_pred.csv")

"""## MLP Pred"""

MLP8_pred = MLP_8.predict(val_data.reshape(11000,784))
MLP8_pred = np.argmax(MLP8_pred, axis=1)
MLP8_pred = pd.DataFrame(MLP8_pred).transpose()
MLP8_pred.to_csv("/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/MLP8_pred.csv")

"""## CNN Pred"""

CNN4_pred = CNN4.predict(val_data.reshape(11000,28,28))
CNN4_pred = np.argmax(CNN4_pred, axis=1)
CNN4_pred = pd.DataFrame(CNN4_pred).transpose()
CNN4_pred.to_csv("/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/CNN4_pred.csv")

CNN5_pred = CNN5.predict(val_data.reshape(11000,28,28))
CNN5_pred = np.argmax(CNN5_pred, axis=1)
CNN5_pred = pd.DataFrame(CNN5_pred).transpose()
CNN5_pred.to_csv("/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/CNN5_pred.csv")

CNN6_pred = CNN6.predict(val_data.reshape(11000,28,28))
CNN6_pred = np.argmax(CNN6_pred, axis=1)
CNN6_pred = pd.DataFrame(CNN6_pred).transpose()
CNN6_pred.to_csv("/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/CNN6_pred.csv")

CNN7_pred = CNN7.predict(val_data.reshape(11000,28,28))
CNN7_pred = np.argmax(CNN7_pred, axis=1)
CNN7_pred = pd.DataFrame(CNN7_pred).transpose()
CNN7_pred.to_csv("/content/drive/Shareddrives/SMLE: Guzmán-Santoscoy-Robles/data/CNN7_pred.csv")

#---END---

#--- The .ipynb file contains the outputs by chunk of code in addition to the views ---
