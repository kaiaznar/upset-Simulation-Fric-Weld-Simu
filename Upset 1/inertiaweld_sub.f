C     USER FRICTION SUBROUTINE
C     (FRICTION MODEL BASED ON MOAL & MASSONI '95)
C     $Id: inertia_weld.for,v 1.2 2007/09/13 19:43:53 yhn Exp $
C     
      SUBROUTINE FRIC(LM,TAU,DDTDDG,DDTDDP,DSLIP,SED,SPD,
     1     DDTDDT,PNEWDT,STATEV,DGAM,TAULM,PRESS,DPRESS,DDPDDH,SLIP,
     2     KSTEP,KINC,TIME,DTIME,NOEL,CINAME,SLNAME,MSNAME,NPT,NODE,
     3     NPATCH,COORDS,RCOORD,DROT,TEMP,PREDEF,NFDIR,MCRD,NPRED,
     4     NSTATV,CHRLNGTH,PROPS,NPROPS)
C     
      INCLUDE 'ABA_PARAM.INC'
      COMMON/SPIN/SPINRATE
C     
      CHARACTER*8 CINAME,SLNAME,MSNAME
      CHARACTER*80 CPNAME
      DIMENSION TAU(NFDIR),DDTDDG(NFDIR,NFDIR),DDTDDP(NFDIR),
     1     DSLIP(NFDIR),DDTDDT(NFDIR,2),STATEV(*),
     2     DGAM(NFDIR),TAULM(NFDIR),SLIP(NFDIR),TIME(2),
     3     COORDS(MCRD),RCOORD(MCRD),DROT(2,2),TEMP(2),
     4     PREDEF(*),PROPS(NPROPS)
C     
      PARAMETER (SCALE=1.D3)
      LOGICAL LOCAL,CONSTANT,DOUBLEMASTER,FLYWHEELRATE,LDEBUG
      PARAMETER (LOCAL        = .FALSE. )
      PARAMETER (DOUBLEMASTER = .TRUE. )
      PARAMETER (CONSTANT     = .FALSE. )
      PARAMETER (FLYWHEELRATE = .TRUE. )
      PARAMETER (LDEBUG       = .FALSE. )
      PARAMETER(ZERO=0.0D0,ONE=1.0D0,TWO=2.0D0)
C     
C     FRICTION MODEL PARAMETERS
C     
C     CONSTANT-COEFFICIENT VALUE
      PARAMETER(CFRIC=0.03D0)
C     CONSTANT-COEFFICIENT TRANSITION SLIP RATE
      PARAMETER(CTRANS=1.0D-2)
C     
      PARAMETER (
     $     C0L = 0.000000E+00,
     $     C1L = 0.132578E+01,
     $     C2L = -.410902E+01,
     $     C3L = 0.289328E+01,
     $     C4L = 0.100344E+01,
     $     C0M = 0.152835E+00,
     $     C1M = -.270046E+00,
     $     C2M = 0.189367E+00,
     $     C3M = -.412224E-01,
     $     C4M = 0.000000E+00)
C     
C     LOW-MEDIUM TRANSITION SLIP RATE
      PARAMETER(RTRANS=0.5D0)
C     
C     MEDIUM-HIGH TRANSITION SLIP RATE
      PARAMETER(RCRIT=1.13D0)
C     
C     HIGH SPEED FRICTION COEFFICIENT
      PARAMETER(HFRIC=0.030D0)
C     
      IF (LDEBUG) THEN
         write (7,*)  'Weld pressure = ',PROPS(1)
      END IF
C     APPLIED PRESSURE
      IF (LOCAL) THEN
         APRESS = PRESS
      ELSE
         IF (DOUBLEMASTER) THEN
            APRESS = PROPS(1) / TWO
         ELSE
            APRESS = PROPS(1)
         END IF
      END IF
      SPRESS = APRESS
C     
      LOCNUM = 0
      JRCD   = 0
      JTYP   = 0
      CALL GETPARTINFO(NODE, JTYP, CPNAME, LOCNUM, JRCD)
C     
      IF (LM .EQ. 2) RETURN
C     
C     SLIP RATE IN ROTATION DIRECTION
C     
      SDIR = SIGN(ONE,DGAM(2))
      IF (KINC.LT.1.OR.(.NOT.FLYWHEELRATE)) THEN
         SRATE = ABS(DGAM(2)/DTIME)
      ELSE
         SRATE = SPINRATE * COORDS(1)
         IF (LDEBUG) THEN
            write (7,*)  'Slip rate based on UEL = ',SRATE*SDIR
            write (7,*)  'Instead of ',DGAM(2)/DTIME
         END IF
      END IF
C     SLIP RATE IN METERS/S
      SRATEM = SRATE/SCALE
      LM=0
C     
      IF ((DSLIP(2)*DGAM(2)).lt.0.0) THEN
         write (7,*) '*** WARNING.  SLIP REVERSAL AT NODE ',LOCNUM
         write (7,*) '                      PART INSTANCE ',CPNAME
         IF (FLYWHEELRATE) THEN
            write (7,*) '       FLYWHEEL-PREDICTED SLIP RATE ',
     $           -SRATE*SDIR
            write (7,*) '                           MEASURED ',
     $           DGAM(2)/DTIME
         END IF
         write (7,*) ' '
      END IF
C     
      IF (CONSTANT) THEN
C        CONSTANT FRICTION COEFFICIENT
C        
         LM = 0
         IF (SRATEM.GT.CTRANS) THEN
            TAU(1)=ZERO
            TAU(2)=CFRIC*APRESS
C           
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)=ZERO
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
C           
            IF (LOCAL) THEN
               DDTDDP(1)=ZERO
               DDTDDP(2)=CFRIC
            ELSE
               DDTDDP(1)=ZERO
               DDTDDP(2)=ZERO
            END IF
         ELSE
            TAU(1)=ZERO
            TAU(2)=CFRIC*APRESS * (SRATEM/CTRANS)
C           
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)=CFRIC * ((APRESS/DTIME) /CTRANS) / SCALE
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
C           
            IF (LOCAL) THEN
               DDTDDP(1)=ZERO
               DDTDDP(2)=CFRIC * (SRATEM/CTRANS)
            ELSE
               DDTDDP(1)=ZERO
               DDTDDP(2)=ZERO
            END IF
         END IF
C        
      ELSE
         IF (SRATEM.GT.RCRIT) THEN
C           
C           HIGH SPEED BEHAVIOR
C           
            LM=0
            TAU(1)=ZERO
            TAU(2)=HFRIC*APRESS
C           
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)=ZERO
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
C           
            IF (LOCAL) THEN
               DDTDDP(1)=ZERO
               DDTDDP(2)=HFRIC
            ELSE
               DDTDDP(1)=ZERO
               DDTDDP(2)=ZERO
            END IF
C           
         ELSE IF (SRATEM.GT.RTRANS) THEN
C           
C           MEDIUM SPEED BEHAVIOR
C           
            TAU(1)=ZERO
            TAU(2)= APRESS *
     $           (C0M          +
     $           C1M*SRATEM    +
     $           C2M*SRATEM**2 +
     $           C3M*SRATEM**3 +
     $           C4M*SRATEM**4)
C           
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)= (SPRESS/DTIME) *
     $           (C1M                +
     $           2.0D0*C2M*SRATEM    +
     $           3.0D0*C3M*SRATEM**2 +
     $           4.0D0*C4M*SRATEM**3) / SCALE
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
C           
            IF (LOCAL) THEN
               DDTDDP(1)=ZERO
               DDTDDP(2)=
     $              (C0M          +
     $              C1M*SRATEM    +
     $              C2M*SRATEM**2 +
     $              C3M*SRATEM**3 +
     $              C4M*SRATEM**4)
            ELSE
               DDTDDP(1)=ZERO
               DDTDDP(2)=ZERO
            END IF
C           
         ELSE
C           
C           LOW SPEED BEHAVIOR
C           
            TAU(1)=ZERO
            TAU(2)= APRESS *
     $           (C0L          +
     $           C1L*SRATEM    +
     $           C2L*SRATEM**2 +
     $           C3L*SRATEM**3 +
     $           C4L*SRATEM**4)
C           
            DDTDDG(1,1)=ZERO
            DDTDDG(2,2)= (SPRESS/DTIME) *
     $           (C1L                +
     $           2.0D0*C2L*SRATEM    +
     $           3.0D0*C3L*SRATEM**2 +
     $           4.0D0*C4L*SRATEM**3) / SCALE
            DDTDDG(1,2)=ZERO
            DDTDDG(2,1)=ZERO
C           
            IF (LOCAL) THEN
               DDTDDP(1)=ZERO
               DDTDDP(2)=
     $              (C0L          +
     $              C1L*SRATEM    +
     $              C2L*SRATEM**2 +
     $              C3L*SRATEM**3 +
     $              C4L*SRATEM**4)
            ELSE
               DDTDDP(1)=ZERO
               DDTDDP(2)=ZERO
            END IF
C           
         END IF
      END IF
C     
      IF ((DSLIP(2)*DGAM(2)).ge.0.0) THEN
         DSLIP(1)=DGAM(1)
         DSLIP(2)=DGAM(2)
      END IF
C     
C     SET SIGN OF ROTATION-DIRECTION SHEAR TERMS
C     
      TAU(2)      = SDIR * TAU(2)
      DDTDDP(2)   = SDIR * DDTDDP(2)
      IF (FLYWHEELRATE) DDTDDG(2,2) = ZERO
      IF (LDEBUG) THEN
         write (7,*)  'FRIC: KINC = ',KINC
         write (7,*)  'NODE  = ',LOCNUM
         write (7,*)  'INSTANCE  = ',CPNAME
         write (7,*)  'SRATE = ',SRATEM
         write (7,*)  'TAU   = ',TAU(2)
         write (7,*)  'SDIR  = ',SDIR
         write (7,*)  'COEFF = ',DDTDDP(2)
         write (7,*)  'PRESSURE = ',APRESS
         write (7,*)  'DDTDDG = ',DDTDDG(2,2)
         write (7,*)  ' '
      END IF
C     
      RETURN
      END
C*********************************************
C     
C     Rolls-Royce Plc Norton-Hoff UHARD subroutine collection
C
C     FLYWHEEL USER SUBROUTINE
C     $Id: inertia_weld.for,v 1.2 2007/09/13 19:43:53 yhn Exp $
C     
      SUBROUTINE UEL(RHS,AMATRX,SVARS,ENERGY,NDOFEL,NRHS,NSVARS,
     1     PROPS,NPROPS,COORDS,MCRD,NNODE,U,DU,V,A,JTYPE,TIME,DTIME,
     2     KSTEP,KINC,JELEM,PARAMS,NDLOAD,JDLTYP,ADLMAG,PREDEF,
     3     NPREDF,LFLAGS,MLVARX,DDLMAG,MDLOAD,PNEWDT,JPROPS,NJPROP,
     4     PERIOD)
C     
C     $Revision: 1.2 $ 
C     $Date: 2007/09/13 19:43:53 $ 
C     
C*********************************************
C     
      INCLUDE 'ABA_PARAM.INC'
C
      COMMON/SPIN/SPINRATE
C     
      DIMENSION RHS(MLVARX,*),AMATRX(NDOFEL,NDOFEL),
     1     SVARS(NSVARS),ENERGY(8),PROPS(*),COORDS(MCRD,NNODE),
     2     U(NDOFEL),DU(MLVARX,*),V(NDOFEL),A(NDOFEL),TIME(2),
     3     PARAMS(3),JDLTYP(MDLOAD,*),ADLMAG(MDLOAD,*),
     4     DDLMAG(MDLOAD,*),PREDEF(2,NPREDF,NNODE),LFLAGS(*),
     5     JPROPS(*)
C
      PARAMETER (ZERO=0.0D0,HALF=0.5D0,ONE=1.0D0)
C     
      if (lflags(3).eq.4) return ! No mass matrix for this element
      IF (JTYPE.GE.1.AND.JTYPE.LE.10) THEN
C        
C        FLYWHEEL INERTIA (USER ELEMENTS U1 .. U10)
C        
C        CHECK THAT PARAMETERS ARE SPECIFIED PROPERLY
C        
         IF (NSVARS.LT.2) THEN
            WRITE (7,1000) JTYPE
 1000       FORMAT ('*ERROR - FLYWHEEL INERTIA USER '//
     $           'ELEMENT, TYPE KEY U',I5,', '//
     $           'REQUIRES SETTING VARIABLES=2 WITH THE *USER '//
     $           'ELEMENT OPTION.')
            CALL STDB_ABQERR(-3,'Incorrect input',0,zero,' ')
         END IF
C        
         IF (NPROPS.LT.1) THEN
            WRITE (7,1001) JTYPE
 1001       FORMAT ('*ERROR - FLYWHEEL INERTIA USER '//
     $           'ELEMENT, TYPE KEY U',I5,', '//
     $           'REQUIRES SETTING PROPERTIES=1 WITH THE *USER '//
     $           'ELEMENT OPTION.')
            CALL STDB_ABQERR(-3,'Incorrect input',0,zero,' ')
         END IF
C        
         IF (NNODE.NE.1) THEN
            WRITE (7,1002)
 1002       FORMAT ('*ERROR - FLYWHEEL INERTIA USER '//
     $           'ELEMENT, TYPE KEY U',I5,', '//
     $           'REQUIRES SETTING NODES=1 WITH THE *USER '//
     $           'ELEMENT OPTION.')
            CALL STDB_ABQERR(-3,'Incorrect input',0,zero,' ')
         END IF
C
         RINERT = PROPS(1)
         UPSETMAX = ZERO
         IF (NPROPS.GT.1) THEN
           UPSETMAX = PROPS(2)
         END IF
         VEL    = DU(1,1)/DTIME
         PV     = SVARS(1)
         ACC    = (VEL-PV)/DTIME
C        
         IF (LFLAGS(3).EQ.1.OR.LFLAGS(3).EQ.2) THEN
C           
C           STIFFNESS
C           
            AMATRX(1,1) = RINERT / (DTIME**2)
C           
         END IF
C        
         IF (LFLAGS(3).EQ.1.OR.LFLAGS(3).EQ.5) THEN
C           
C           RHS
C           
            RHS(1,1) = -ACC*RINERT
C
         END IF
C        
C         
C        FLYWHEEL KINETIC ENERGY
         ENERGY(1) = HALF*RINERT*VEL**2
C
C        UPSET BASED TERMINATION CRITERION
         if (jtype.eq.1.and.UPSETMAX.NE.ZERO) then
           UPSET = ABS(U(2))
            WRITE (7,1006) UPSET
 1006       FORMAT (//,'   UPPER PIPE UPSET = ',1PG12.3)
           if (UPSET.GT.UPSETMAX) THEN
             WRITE (7,1007)
 1007        FORMAT (//,'   TERMINATING ANALYSIS: UPSET LIMIT REACHED')
             CALL XIT()
           END IF
         end if
C        
C        STORE VELOCITY AS SDV1, AND PUT IN COMMON BLOCK
         IF (JTYPE.EQ.1) THEN
            SPINRATE  = SVARS(1)
            WRITE (7,1003) SPINRATE
 1003       FORMAT (//,'   MAIN FLYWHEEL VELOCITY = ',1PG12.3)
            WRITE (7,1004) ENERGY(1)
 1004       FORMAT (//,'   MAIN FLYWHEEL ENERGY = ',1PG12.3)
         END IF
         SVARS(1)  = VEL
C        
C        STORE ACCELERATION AS SDV2
         SVARS(2)  = ACC
C
      ELSE
C        
C        INCLUDE ADDITIONAL USER ELEMENTS HERE
C        WITH APPROPRIATE TESTS ON THE ELEMENT
C        TYPE KEY, JTYPE
C     
         WRITE (7,1005) JTYPE
 1005    FORMAT ('NO USER ELEMENT IS DEFINED FOR '//
     $        'ELEMENT TYPE KEY U',I5,'.')
C        
      END IF
C     
      RETURN
      END         
