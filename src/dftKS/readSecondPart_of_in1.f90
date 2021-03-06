SUBROUTINE ReadSecondPart_of_in1(El,Elo,lapw,loor,ilo,nlo, Vr,ZZ,jri,mult,dx,r0,Efermi,aname,REL,fh_in1,fh_cout,fh_scf,nat,nrad,nloat,lmax,lomax,Qprint)
  IMPLICIT NONE
  REAL*8,  intent(out) :: El(1:lmax,nat), Elo(0:lomax,1:nloat,nat)
  LOGICAL, intent(out) :: lapw(0:lmax-1,nat), loor(0:lomax,nat)
  INTEGER, intent(out) :: ilo(0:lomax,nat)
  INTEGER, intent(out) :: nlo
  REAL*8,  intent(in)  :: Vr(nrad,nat), ZZ(nat)
  INTEGER, intent(in)  :: jri(nat), mult(nat)
  REAL*8,  intent(in)  :: dx(nat), r0(nat), Efermi
  CHARACTER*10, intent(in) :: aname(nat)
  LOGICAL, intent(in)  :: REL    ! relativistic Dirac or no
  INTEGER, intent(in)  :: fh_in1, fh_cout, fh_scf
  INTEGER, intent(in)  :: nat, nrad, nloat, lmax, lomax
  LOGICAL, intent(in)  :: Qprint
  ! locals
  INTEGER :: jatom, i, j, iapw, NL_read, L, L_previous
  REAL*8  :: RNET(nrad), Ei, dE
  CHARACTER*4 ::  EMAIN
  CHARACTER*67:: ERRMSG
  
  NLO = 0
  DO jatom = 1, NAT
     do i=1,jri(jatom)  ! Radial mesh created just once at the beginning
        RNET(i)=r0(jatom)*exp(dx(jatom)*(i-1.d0))
     enddo
     ! Reads the default setting from case.in1
     iapw=0
     READ (fh_in1,*,err=41) Ei, NL_read,iapw              ! EI==Global E par; NL_read==N cases; iapw=APW/LAPW
     if(abs(EI-0.3d0).lt.1.d-6) EI=Efermi-0.2d0  ! if EI is 0.3 than we set it to EF-0.2
     if(iapw.eq.1) then
        lapw(0:lmax-1,jatom)=.false.  ! all l's for this atom have apw+lo (if not changed below)
     else
        lapw(0:lmax-1,jatom)=.true.   ! all l's for this atom have lapw  (if not changed below)
     endif
41   continue

     if (Qprint) then
        if(iapw.eq.1) then
           WRITE (fh_scf,6000) ANAME(JATOM), jatom, Ei,'  APW'
        else
           WRITE (fh_scf,6000) ANAME(JATOM), jatom, Ei,' LAPW'
        endif
     endif
     ! initialization 
     loor(0:lomax,jatom) = .false.
     ilo(0:lomax,jatom) = 0
     El(1:lmax,jatom) = EI
     if (nloat.gt.3) then ! LO type local orbitals possible
        ! for apw+lo (lapw+lo) we set to 99997.0 (99999.0)
        Elo(0:lomax,1:nloat,jatom) = 99997.0D+0    ! set to large number, so we know it is not present
        DO l=0,lomax
           if(lapw(l,jatom)) Elo(l,1:nloat,JATOM) = 99999.0D+0  ! large number, hence LO is not present
        ENDDO
     else                 ! LO type local orbitals not possible, just apw+lo might still be there
        ! for apw+lo (lapw+lo) we set to 997.0 (999.0)
        Elo(0:lomax,1:nloat,jatom) = 997.0D+0      ! set to large number, so we know it is not present
        DO l=0,lomax
           if(lapw(l,jatom)) Elo(l,1:nloat,JATOM) = 999.0D+0    ! large number, hence LO is not present
        ENDDO
     endif
     
     L = -1
     DO j=1,NL_read
        L_previous = L   ! previous L
        iapw=0
        READ (fh_in1,'(1X,I1,2F10.5,A4,i2)',err=42) L, EI, dE, EMAIN, iapw  ! 
        if (dE.lt.-1.0d-8) dE=-dE/10000.d0           ! if de<0 than de is really small positive, namely 1e4-times smaller than written
        if(abs(Ei-0.3d0).lt.1.d-6.and.L.ne.L_previous) Ei=Efermi - 0.2d0 ! if Ei=0.3 and not LO   => Ei=EF-0.2
        if(abs(Ei-0.3d0).lt.1.d-6.and.L.eq.L_previous) Ei=Efermi + 0.2d0 ! if Ei=0.3 and it is LO => Ei=EF+0.2
42      continue
        
        IF (dE .GT. 1.0D-5) THEN  ! finite de>1e-5 =>  we can search for the center of the band
           CALL SELECT(L,Ei,dE,EMAIN,REL,VR(1,JATOM),R0(jatom),dx(jatom),jri(jatom),ZZ(JATOM),jatom,Efermi)
        ELSE
           if (Qprint) then
              WRITE (fh_cout,6010)  L,jatom, L, Ei
              WRITE (fh_scf,6010) L,jatom, L, Ei
           endif
        ENDIF

        IF (L.NE.L_previous) THEN                ! the first n of certain l => must be apw or lapw
           El(l+1,jatom) = Ei                     ! Remember linearization energy for this apw/lapw
           if(iapw.eq.1) then                    ! this is apw+lo
              lapw(l,jatom)=.false.
              NLO = NLO + ((2*L+1))*MULT(JATOM)  ! we have apw+lo, constructued from u and dotu, hence many local orbitals in the ham.
              if (Qprint) then
                 write(fh_cout,*) '            APW+lo'
                 write(fh_scf,*) '            APW+lo'
              endif
              ilo(l,jatom)=1                     ! since this is the first for this l, we can set ilo to 1.
              Elo(l,1,jatom)=Ei                  ! Linearization energy for APW+lo is the same. We just date dotu.
              if(nloat.gt.3) then                ! real local orbitals are present
                 Elo(l,2,jatom)=99997.0D+0       ! next one is set to large number, so that we know when to stop
              else
                 Elo(l,2,jatom)=997.0D+0         ! next one is set to large number, hence it does not exist
              endif
           else                                  ! regular lapw
              if (Qprint) then
                 write(fh_cout,*) '            LAPW'
                 write(fh_scf,*) '            LAPW'
              endif
           endif
        ELSE ! not the first n of certain l => must be extra local orbital (not apw+lo but LO)
           ilo(l,jatom)=ilo(l,jatom)+1      ! yes, increase number of local orbitals
           if (ilo(l,jatom).gt.nloat) then  ! should not happen, as nloat should be larger than any number of LO's
              goto 902
           endif
           Elo(L,ilo(l,jatom),jatom) = Ei    ! remember this linearization energy for local orbital
           NLO = NLO + ((2*L+1))*MULT(JATOM) ! many local orbitals need to be added, namely, one for each equivalent atom and for each m.
           if (Qprint) then
              write(fh_cout,*)  '            LOCAL ORBITAL'
              write(fh_scf,*) '            LOCAL ORBITAL'
           endif
           loor(l,jatom)=.true.
        ENDIF
     ENDDO
  END DO


  !WRITE(6,*) 'loor,ilo='
  !DO jatom=1,NAT
  !   do l=0,2
  !      WRITE(6,*) l,jatom,loor(l,jatom), ilo(l,jatom)
  !   enddo
  !ENDDO
  
  return
902 CONTINUE
  WRITE (ERRMSG,9002) 'NLOAT too small', NLOAT,l,jatom
  CALL OUTERR('ATPAR',ERRMSG)
  STOP 'readSecondPart_of_in1 - Error'
  !
6000 FORMAT (/,10X,'ATOMIC SPHERE DEPENDENT PARAMETERS FOR ATOM  ',A10,/,':e__',i4.4,':',1X,'OVERALL ENERGY PARAMETER IS',F10.4/,10X,'OVERALL BASIS SET ON ATOM IS',A5)
6010 FORMAT (':E',i1,'_',i4.4,':',1X,'E(',I2,2H)=,F10.4)
9002 FORMAT (A,' (NLOAT =',I3,', L =',I3,' JATOM =',i3,')')
END SUBROUTINE ReadSecondPart_of_in1
