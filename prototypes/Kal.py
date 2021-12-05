#!/usr/bin/env python3

import cbpro
import pandas as pd
import numpy as np

class Kal:
    
    @classmethod
    def predict(cls, X, F, P, Q):
        #prediction state update
        X1 = np.matmul(F, X)

        #P1 = F*P*F' + Q
        P1 = np.matmul(np.matmul(F, P), np.transpose(F)) + Q
        return X1, P1
    
    @classmethod
    def update(cls, obs, X, P, R):
        KalGain = np.matmul(P, np.linalg.inv(P + R))
        XU = X + np.matmul(KalGain, (obs - X))
        PU = P + np.matmul(KalGain, P)
        return XU, PU
    
    @staticmethod
    def createPred(X, F, P, Q):
        pred = [None]
        for num in range(len(candles.index) - 1):
            X, P = Kal.predict(X, F, P, Q)
            #print('X: ' + str(X))
            #print(num)
            #print(X)
            pred.append(X[0])
            #print('P: ' + str(P))

            #observation
            obs = np.array([candles['close'][num + 1], (candles['close'][num] - candles['close'][num + 1])])
            X, P = Kal.update(obs, X, P, R)
        return pred

if __name__ == '__main__':
    from CBData import CBData
    import matplotlib.pyplot as plt
    
    #load finacial price data
    candles = CBData.load()
    
    #INITIALIZE KALMAN VALUES#
    #velocity of price
    startVel = 0
    startPrice = candles['close'][0]
    
    #X Systen state 
    # x = [p, dp] x is state vector, p is price, dp is change in price or 
    X = np.array([startPrice, startVel])

    #Q system uncertainty
    uncerPos = 10
    uncerVel = .1 #change per second
    Q = np.array([[uncerPos, 0],[0, uncerVel]])

    #P Initial Cov 
    varVel = 1
    varPos = 1
    P = [[varPos, 0], [0, varVel]]

    #F transformation matrix from time time t-1 to t
    delT = 60 #time in seconds
    F = np.array([[1, delT],[0, 1]])
    
    #measurement uncertainty
    uncerPos = 10
    uncerVel = .1 #change per second
    R = np.array([[uncerPos, 0],[0, uncerVel]])

    #get predicted values
    candles['pred'] = Kal.createPred(X, F, P, Q)
    
    #PLOT
    candles[80:90].plot(x = 'time', y = ['close','pred'])
    candles[80:90].head
    plt.show()
    print('done')