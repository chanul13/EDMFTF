#!/usr/bin/env python
from scipy import *
import utils, indmffile
import sys, os

def FindLatticeNd(case, m_extn, siginds,icols_ind,fh_info, scf_name='scf2', cmplx=False):
    "Finds occupation from scf2"
    def Read_scf2(dat,siginds,cmplx):
        nd={}
        nl={}
        colm=1
        if cmplx: colm=2
        for l in range(len(dat)):
            if dat[l][:5]==':NCOR':
                dd = dat[l].split()  # should contain nf, icix, cixdm
                icix = int(dd[2])
                dim = int(dd[3])
                nd[icix] = float(dd[1])
                mm = zeros((dim,dim))   # Density matrix dim x dim
                for i in range(dim):
                    mm[i,:]=[float((dat[l+1+i].split())[j*colm]) for j in range(dim)]

                Sigind = siginds[icix]  # correlated index
    
                diag_Sigind = filter(lambda x: x!=0, [Sigind[i,i] for i in range(len(Sigind))]) # all diagonal entries except 0
                imin = min(abs(array(diag_Sigind)))  # index of the first entry
                imax = max(abs(array(diag_Sigind)))  # index of the last entry
                nl[icix] = zeros(imax-imin+1)  # for each cix we have compressed density matrix
                for i in range(dim):
                    if Sigind[i,i]>0:
                        j=Sigind[i,i]-imin
                        nl[icix][j] += mm[i,i]
        return (nd,nl)
    
    fileup = case+'.'+scf_name
    if not( os.path.exists(fileup) and os.path.getsize(fileup)>0 ): 
        return (None, None)
    fsc = open(fileup,'r')
    dat = fsc.readlines()
    (nd, nl) = Read_scf2(dat, siginds,cmplx)
    if not nl: 
        return (None, None)
    
    #print 'nl=', nl
    #print 'nd=', nd
    
    if m_extn:
        fsc = open(case+'.'+scf_name+m_extn,'r')
        dat = fsc.readlines()
        (nd_, nl_) = Read_scf2(dat, siginds,cmplx)
        for icix in nl.keys():
            nl[icix] = 0.5*(nl[icix] + nl_[icix])
            nd[icix] = 0.5*(nd[icix] + nd_[icix])

    # Now converting from atom index to impurity, i.e., there are many 
    # correlated atoms that correspond to the same impurity
    nl_imp={}
    nd_imp={}
    for i in icols_ind.keys():
        nl_all=[]
        nd_all=[]
        for icix in icols_ind[i]:
            nl_all.append( nl[icix] )
            nd_all.append( nd[icix] )
        nl_imp[i] = reduce(lambda x,y: x+y, nl_all)/len(nl_all)
        nd_imp[i] = reduce(lambda x,y: x+y, nd_all)/len(nd_all)
    
    print >> fh_info, 'nl_imp=', nl_imp
    print >> fh_info, 'nd_imp=', nd_imp
    
    return (nl_imp,nd_imp)


if __name__ == '__main__':
     w2k = utils.W2kEnvironment()    # W2k filenames and paths
     m_extn='dn'
     inl = indmffile.Indmfl(w2k.case) # case.indmfl file
     inl.read()                       # case.indmfl read
     icols_ind={0: [1]}
     (nl_imp, nd_imp) = FindLatticeNd(w2k.case, m_extn, inl.siginds, icols_ind, sys.stdout, 'scfdmft1', cmplx=True)
     print nl_imp, nd_imp
