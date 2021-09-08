import scipy.io
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.externals import joblib
import json
import pickle


data = scipy.io.loadmat('training_data.mat')

keys = []

for i in data:
    if i.startswith("__"):
        continue
    keys.append(str(i))

estimate = np.zeros(len(keys))
dat = np.zeros((len(keys), len(data[keys[0]][0][0][0,:])))

#estimate = np.reshape(estimate, (1, len(estimate)))

for i, key in enumerate(keys):
    estimate[i] = int(data[key][0][1])
    dat[i] = data[key][0][0][0,:]



X_train, X_test, y_train, y_test = train_test_split(abs(dat), estimate)


scaler = StandardScaler()
#scaler.fit(X_train)

#X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)

mlp = MLPClassifier(hidden_layer_sizes=(16,16,16))  
mlp.fit(X_train,y_train)

predictions = mlp.predict(X_test)
print(confusion_matrix(y_test,predictions))

print(classification_report(y_test,predictions))

pickle.dump(mlp, open( "classifier.pkl", "wb" ), protocol=2) 

