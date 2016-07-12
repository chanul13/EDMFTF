from scipy import *

class Momentd:
    """ Defines Lx,Ly,Lz , Sigx, Sigy, Sigz, Mx, My, Mz
        where Sig==2*S, and M = L + 2*S
        basis is:
        [-2up,-1up,0up,1up,2up,-2dn,-1dn,0dn,1d,2dn]
    """
    def __init__(self):
        Sgx = [[ 0,  0,  0,  0,  0,  1,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  1,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  1,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  0,  1,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1],
               [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  1,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  1,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  1,  0,  0,  0,  0,  0]]
        self.Sgx = matrix(Sgx)
        Sgy = [[ 0,  0,  0,  0,  0,-1j,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,-1j,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0,-1j,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  0,-1j,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  0,  0,-1j],
               [1j,  0,  0,  0,  0,  0,  0,  0,  0,  0],
               [ 0, 1j,  0,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  0, 1j,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0, 1j,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0, 1j,  0,  0,  0,  0,  0]]
        self.Sgy = matrix(Sgy)
        Sgz = [[ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  1,  0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  1,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  1,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0, -1,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0, -1,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0, -1,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  0, -1,  0],
               [ 0,  0,  0,  0,  0,  0,  0,  0,  0, -1]]
        self.Sgz = matrix(Sgz)
        
        s6=sqrt(6.)
        Lp = [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  #-2
              [ 2,  0,  0,  0,  0,  0,  0,  0,  0,  0],  #-1
              [ 0, s6,  0,  0,  0,  0,  0,  0,  0,  0],  # 0
              [ 0,  0, s6,  0,  0,  0,  0,  0,  0,  0],  # 1
              [ 0,  0,  0,  2,  0,  0,  0,  0,  0,  0],  # 2
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  #-2
              [ 0,  0,  0,  0,  0,  2,  0,  0,  0,  0],  #-1
              [ 0,  0,  0,  0,  0,  0, s6,  0,  0,  0],  # 0
              [ 0,  0,  0,  0,  0,  0,  0, s6,  0,  0],  # 1
              [ 0,  0,  0,  0,  0,  0,  0,  0,  2,  0]]  # 2
        Lp=matrix(Lp)
        Lm = [[ 0,  2,  0,  0,  0,  0,  0,  0,  0,  0],  #-2
              [ 0,  0, s6,  0,  0,  0,  0,  0,  0,  0],  #-1
              [ 0,  0,  0, s6,  0,  0,  0,  0,  0,  0],  # 0
              [ 0,  0,  0,  0,  2,  0,  0,  0,  0,  0],  # 1
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # 2
              [ 0,  0,  0,  0,  0,  0,  2,  0,  0,  0],  #-2
              [ 0,  0,  0,  0,  0,  0,  0, s6,  0,  0],  #-1
              [ 0,  0,  0,  0,  0,  0,  0,  0, s6,  0],  # 0
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  2],  # 1
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]  # 2
        Lm=matrix(Lm)
        Lz = [[-2,  0,  0,  0,  0,  0,  0,  0,  0,  0],
              [ 0, -1,  0,  0,  0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  1,  0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  2,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0, -2,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0, -1,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
              [ 0,  0,  0,  0,  0,  0,  0,  0,  1,  0],
              [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  2]]
        self.Lz=matrix(Lz)
        
        self.Lx = (Lp+Lm)/2.
        self.Ly = (Lp-Lm)/(2.*1j)
        self.Mx = -(self.Lx+self.Sgx)
        self.My = -(self.Ly+self.Sgy)
        self.Mz = -(self.Lz+self.Sgz)


def Mix2Eigenvectors(TT,c):
    """
    T[0,:] = c[0,0]*TT[0,:]+c[0,1]*TT[1,:]
    T[1,:] = c[1,0]*TT[0,:]+c[1,1]*TT[1,:]
    T[2,:] = c[0,0]*TT[2,:]+c[0,1]*TT[3,:]
    T[3,:] = c[1,0]*TT[2,:]+c[1,1]*TT[3,:]
    T[4,:] = c[0,0]*TT[4,:]+c[0,1]*TT[5,:]
    T[5,:] = c[1,0]*TT[4,:]+c[1,1]*TT[5,:]
    T[6,:] = c[0,0]*TT[6,:]+c[0,1]*TT[7,:]
    T[7,:] = c[1,0]*TT[6,:]+c[1,1]*TT[7,:]
    T[8,:] = c[0,0]*TT[8,:]+c[0,1]*TT[9,:]
    T[9,:] = c[1,0]*TT[8,:]+c[1,1]*TT[9,:]
    """
    T = zeros(shape(TT),dtype=complex)
    for n in range(len(TT)/2):
        for i in range(2):
            T[2*n+i,:] = c[i,0]*TT[2*n+0,:]+c[i,1]*TT[2*n+1,:]
    T = matrix(T)
    return T
    
def mprint(Us):
    Qcomplex =  type(Us[0,0])==complex or type(Us[0,0])==complex128
    for i in range(shape(Us)[0]):
        for j in range(shape(Us)[1]):
            if Qcomplex:
                print "%11.8f %11.8f  " % (real(Us[i,j]), imag(Us[i,j])),
            else:
                print "%11.8f  " % Us[i,j],
        print

def StringToMatrix(cfstr,stype='complex'):
    mm=[]
    for line in cfstr.split('\n'):
        line = line.strip()
        if line:
            data = array(map(float,line.split()))
            if stype=='complex':
                mm.append( data[0::2]+data[1::2]*1j )
            else:
                mm.append( data )
                
    mm=matrix(mm)
    return mm

if __name__ == '__main__':
    sTT="""
     0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.72097658  0.00000000    0.00000000  0.00000000    0.35236224 -0.34049559    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000   -0.35236224  0.34049559
    -0.35236224 -0.34049559    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.35236224  0.34049559    0.00000000 -0.00000000    0.72097658  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000
     0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    1.00000000  0.00000000    0.00000000  0.00000000
     0.00000000  0.00000000    1.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000
     0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.69295944  0.00000000    0.00000000  0.00000000   -0.36660865  0.35426221    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.36660865 -0.35426221
     0.36660865  0.35426221    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000   -0.36660865 -0.35426221    0.00000000  0.00000000    0.69295944  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000 -0.00000000
     0.00000000  0.00000000    0.00000000  0.00000000    1.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000
     0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    1.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000
     0.70710679  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.70710679  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000
     0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.70710679  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.00000000  0.00000000    0.70710679  0.00000000
    """	 
    TT = StringToMatrix(sTT)

    M = Momentd()
    
    T = TT
    print 'cfx transformation matrix:'
    mprint(T)
    print 'Mx='
    mprint(T * M.Mx * T.H)
    print 'My='
    mprint(T * M.My * T.H)
    print 'Mz='
    mprint(T * M.Mz * T.H)
    print
    
    s2 = sqrt(2.)
    c=array([[ (1+1j)/2.,1/sqrt(2.)],[-(1+1j)/2.,1/sqrt(2.)]])
    T = Mix2Eigenvectors(TT,c)

    print 'cfx transformation matrix:'
    mprint(T)
    print 'Mx='
    mprint(T * M.Mx * T.H)
    print 'My='
    mprint(T * M.My * T.H)
    print 'Mz='
    mprint(T * M.Mz * T.H)
    print

    c = array([[ (1-1j)/2.,1/sqrt(2.)],[-(1-1j)/2.,1/sqrt(2.)]])
    T = Mix2Eigenvectors(TT,c)
    
    print 'cfx transformation matrix:'
    mprint(T)
    print 'Mx='
    mprint(T * M.Mx * T.H)
    print 'My='
    mprint(T * M.My * T.H)
    print 'Mz='
    mprint(T * M.Mz * T.H)
    print