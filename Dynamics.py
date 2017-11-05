import numpy as np
def is_three_point(data):
    '''
    This func is to analyze the size of the imput, in this case
    the input should be 3 points, in the shape of
    [(x,y,xdia,ydia),(5,6,7,8),(9,10,11,12)]
    '''
    if np.shape(data)==(3L,4L):
        return True
    else:
        return False

def arrange_points(data):
    '''
    This func is to aline positions with markers, which should be
    po1: top robot, y max
    po2: robot foot, y mid
    po3: ground, y min
    '''
    #data=np.random.rand(4,4);
    po1_idx=np.argmax(data[:,0]);
    po3_idx=np.argmin(data[:,0]);
    po2_idx=[element for i, element in enumerate([0,1,2]) if i not in {po1_idx, po3_idx}];
    po1=[A[po1_idx,1],A[po1_idx,0]];
    po2=[A[po2_idx[0],1],A[po2_idx[0],0]];
    po3=[A[po3_idx,1],A[po3_idx,0]];
    return po1, po2, po3

#class point_robot(po1):
 #   def __init__(self,po1):
 #       self.y=[po1[1]];
  #      self.ydot=[0];
        
#class point_foot(po2):
#    def __init__(self,po2):
#        self.y=[po2[1]];
 #       self.ydot=[0];
        
#class point_ground(po3):
 #   def __init__(self,po3):
 #       self.x=[po3[0]];
                
def dynamics_air(po1,po2,po3,PO1,PO2,PO3,g,dt):
    '''
    This func is based on the dynamics in air,
    yddot = -g
    ydot = (y_t+1 - y_t)/dt - yddot*dt/2;
    '''
    PO1.ydot.append((po1[1]-PO1.y[-1])/dt-g*dt/2);
    PO2.ydot.append((po2[1]-PO2.y[-1])/dt-g*dt/2);
    
    PO1.y.append(po1[1]);
    PO2.y.append(po2[1]);
    PO3.x.append(po3[0]);    
    Contorl=[0,0];
    return Control;

def dynamics_spring(po1,po2,po3,PO1,PO2,PO3,g,dt,l1,l2):
    '''
    This func is based on the dynamics in stance,
    yddot = -g + K*(L - (PO1.y[-1] - PO2.y[-1]))*(1 + eta*PO1.ydot[-1]) - mu*PO1.ydot[-1]
    ydot_m = (y_t+1 - y_t)/dt
    ydot_p = ydot_m + yddot*dt;
    y_plus = ydot_m*dt + yddot*dt^2/2;
    '''
    yddot=-g+K*(L-(PO1.y[-1]-PO2.y[-1]))*(1+eta*PO1.ydot[-1])-mu*PO1.ydot[-1];
    ydot_m = (po1[1]-PO1.y[-1])/dt;
    PO1.ydot.append(ydot_m);
    PO2.ydot.append(0);
    PO1.y.append(po1[1]);
    PO2.y.append(po2[1]);
    PO3.x.append(po3[0]);
    ydot_p = ydot_m*dt + yddot*(dt**2)/2;
    L_future = ydot_p - po2[1];
    L_past = po1[1] - po2[1];
    delta_theta = return_theta(L_future,l1,l2) - return_theta(L_past,l1,l2);
    Contorl = [delta_theta, delta_theta];
    return Control;

def return_theta(L,l1,l2):
    '''
    With Cosine Rule, we can get the angle theta once we know all sides of a triangle
    '''
    theta = np.arccos((L**2+l1*82-l2**2)/(2*L*l1));
    return theta

