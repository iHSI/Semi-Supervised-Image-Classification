import math 
import numpy as np
import numpy.matlib
import scipy.io as sio
from numpy import linalg as LA

def grad(alpha,K,Y,L,J,l,u,gamma_I,gamma_A):
    A=J*K*alpha
    B=gamma_A*l*alpha
    C=(gamma_I/(l+u)**2)*L*K*alpha
    d=A+B+C-Y  
    return(d)

## Load Data
mat1 = sio.loadmat('C:\Users\sandippk\Desktop\Machine Learning\Fifth Feature\smaller\X_train.mat')
mat2 = sio.loadmat('C:\Users\sandippk\Desktop\Machine Learning\Fifth Feature\smaller\Y_train.mat')
mat3 = sio.loadmat('C:\Users\sandippk\Desktop\Machine Learning\Fifth Feature\smaller\X_test.mat')
mat4 = sio.loadmat('C:\Users\sandippk\Desktop\Machine Learning\Fifth Feature\smaller\Y_test.mat')
X=np.asmatrix(mat1['X_final'])
Y_trncomplte=np.asmatrix(mat2['Y_final'])
X_test=np.asmatrix(mat3['X_test'])
Y_tstcomplte=np.asmatrix(mat4['Y_test'])
Y_test=np.transpose(np.asmatrix((-1)*np.ones(len(Y_tstcomplte))))


#X=X[0:1500,:]
#Y_trncomplte=Y_trncomplte[0:1500,:]
Y=np.transpose(np.asmatrix((-1)*np.ones(len(Y_trncomplte))))


label=3
for i in range(0,len(Y_trncomplte)):
    if Y_trncomplte[i]==label:
        Y[i]=1
for i in range(0,len(Y_tstcomplte)):
    if Y_tstcomplte[i]==label:
        Y_test[i]=1
#S1 = [1000000, 100000, 25000, 1e8, 500000 ]
S1 = [.01, 0.03, 0.05, 0.07, 0.09, 0.1]
G = [.005, 0.01, 0.05, 0.075, 0.1]
## Intialize Variables
Per = np.zeros((len(S1),len(G)))
for s1 in range(0,len(S1)):
    for g in range(0,len(G)):
        l=np.count_nonzero(Y)
        u=len(X)-l
        n_crrct=0
        gamma_I = G[g]
        #gamma_I=float(.005)
        gamma_A=float(.5)
        #sigma=float(10)
        sigma = S1[s1]
        itrn=40000
        error=1e-8
        alpha=np.matlib.zeros((l+u,itrn))
        alpha[:,0]=np.asmatrix(np.random.randn(l+u,1))
        a=np.matlib.zeros((l+u,itrn))
        K=np.matlib.zeros((l+u,l+u))
        J=np.matlib.zeros((l+u,l+u))
        L=np.matlib.zeros((l+u,l+u))
        W=np.matlib.zeros((l+u,l+u))
        D=np.matlib.zeros((l+u,l+u))
        I=np.asmatrix(np.identity(l+u))
        fx=np.matlib.zeros((len(X_test),1))
        Y_predcted=np.matlib.zeros((len(X_test),1))
        for i in range(0,l,1):
            J[i,i]=1
        for i in range(0,l,1):
            xi=X[i]
            for j  in range(0,l,1):
                xj=X[j]
                K[i,j]=np.exp(-((xi-xj)*np.transpose(xi-xj))/sigma)
                W[i,j]=np.exp(-(LA.norm(xi-xj))**2)
        d=np.sum(W,axis=1)
        for i in range(0,l+u,1):
            D[i,i]=d[i]
        L=D-W
        ## Accelerated Gradient Decent
        for i in range(0,itrn-1):
             a[:,i]=grad(alpha[:,i],K,Y,L,J,l,u,gamma_I,gamma_A)
             alpha[:,i+1]=alpha[:,i]-(0.001)*a[:,i]
             z1=alpha[:,i+1]-alpha[:,i]
             z2=alpha[:,i]-alpha[:,i-1]
             z1n=LA.norm(z1)
             z2n=LA.norm(z2)
             e=np.abs(z1n-z2n)
             #print(i)
             print(e)
             #print(error)
             if e<=error:
                 break
          
            
        fnl=i+1     
        ## Testing Data
        for i in range(0,len(X_test)):
            f=0
            for j in range(0,l+u):
                Kx=np.exp(-((X_test[i]-X[j])*np.transpose(X_test[i]-X[j]))/sigma)
                f=f + (alpha[j,fnl]*Kx) 
            if f >= 0:
                Y_predcted[i]=1
            else:
                Y_predcted[i]=-1
            if Y_predcted[i]==Y_test[i]:              
                n_crrct=n_crrct+1
        
        Percnt_crrct=100*n_crrct/float(len(X_test))       
        print(Percnt_crrct) 
        Per[s1,g] =Percnt_crrct