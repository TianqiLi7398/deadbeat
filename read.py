import numpy as np
from numpy import linalg as LA

def read_from_csv(X,Y,T):
    # This function is to read csv data#
    
    length = len(X);
    x,y,t = np.zeros((length,3)), np.zeros((length,3)), np.zeros((length,1));
    for i in range(length):
        x_line = X[i].replace("[","");
        y_line = Y[i].replace("[","");
        #time_line = T[i].replace("[","");
        trans_x = x_line.replace("]","");
        trans_y = y_line.replace("]","");
        #trans_time = time_line.replace("]","");
        for j in range(3):
            x[i,j] = int(trans_x.split(" ")[j])
            y[i,j] = int(trans_y.split(" ")[j])
        t[i] = int(T[i])
            
    return x, y, t

def jump_from_csv(X,Y,T):
    # This function is to read csv data#
    
    length = len(X);
    x,y,t = np.zeros((length,4)), np.zeros((length,4)), np.zeros((length,1));
    for i in range(length):
        x_line = X[i].replace("[","");
        y_line = Y[i].replace("[",""); 
        trans_x = x_line.replace("]","");
        trans_y = y_line.replace("]","");
        if (len(trans_x.split(" ")) == 4):
            for j in range(4):
                x[i,j] = float(trans_x.split(" ")[j])
                y[i,j] = float(trans_y.split(" ")[j])
                t[i] = float(T[i])
        else:
            pass
               
    return x, y, t

def arrange_coordinate(x, y):
    p1, p2, p3 = np.zeros((len(x),2)), np.zeros((len(x),2)), np.zeros((len(x),2));
    for i in range(len(x)):
        po1_idx=np.argmin(y[i]);
        po2_idx=np.argmax(x[i]);
        po3_idx=[element for j, element in enumerate([0,1,2]) if j not in {po1_idx, po2_idx}];
        p1[i]=[x[i, po1_idx],y[i, po1_idx]];
        p2[i]=[x[i, po2_idx],y[i, po2_idx]];
        #p3[i]=[x[i, po3_idx[0]],y[i, po3_idx[0]]];
        p3[i]=[x[i, po3_idx[0]],y[i, po3_idx[0]]];
    return p1, p2, p3

def jump_coordinate(x, y, t):
    p1, p2, p3, p4 = np.zeros((len(x),3)), np.zeros((len(x),3)), np.zeros((len(x),3)), np.zeros((len(x),3));
    for i in range(len(x)):
        po1_idx=np.argmax(x[i]);
        po2_idx=np.argmin(y[i]);
        po3_idx=np.argmin(x[i]);
        po4_idx=np.argmax(y[i]);
        p1[i]=[x[i, po1_idx],y[i, po1_idx], t[i]];
        p2[i]=[x[i, po2_idx],y[i, po2_idx], t[i]];
        p3[i]=[x[i, po3_idx],y[i, po3_idx], t[i]];
        p4[i]=[x[i, po4_idx],y[i, po4_idx], t[i]];
    return p1, p2, p3, p4

def calibration(p, P1, P2, P3):
    v1 = P1 - P3; # x coordinate, actual length is 10 cm.
    v2 = P2 - P3; # y coordinate
    pcal = np.zeros((len(p),2));
    for i in range(len(p)):
        pcal[i, 0]= (100 / LA.norm(v1)) * np.dot(v1, [p[i, 0], p[i, 1]] - P3)/(LA.norm(v1)); # unit is mm
        pcal[i, 1]= (100 / LA.norm(v2)) * np.dot(v2, [p[i, 0], p[i, 1]] - P3)/(LA.norm(v2));
    return pcal

def cut(top_cal, foot_cal, t):
    # this function is to cut the data into single jumping periods
    # by finding the maxium point and get the data from before and after
    # the apex height
#     A: top point coordinate
#     B: foot point coordinate
#     j: total jumping period found
        
    A = np.zeros((1,195));
    B = np.zeros((1,195));
    j = 0;
    for i in range(int(round(len(t)/195))):
        if (i*195 < len(t) + 1):
            idx = np.where(top_cal[:,1] == top_cal[:,1][195 * (i-1) : 195*i -1].max())
            a = (idx[0] < len(t) - 153)[0];
            b = (idx[0] >= 40)[0];
            #print idx[0], len(t) - 153
            #print idx
            if (a and b):
                A = np.vstack((A, top_cal[:,1][ idx[0][0] - 40 : idx[0][0] + 155 ]));
                B = np.vstack((B, foot_cal[:,1][ idx[0][0] - 40 : idx[0][0] + 155 ]));
                #print ('found ', j)
                j += 1;
    return A[1:j], B[1:j], j