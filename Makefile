#
# Automagically generated by Approximatrix Simply Fortran 3.2
#
FC="C:\Program Files (x86)\Simply Fortran 3\mingw-w64\bin\gfortran.exe"
CC="C:\Program Files (x86)\Simply Fortran 3\mingw-w64\bin\gcc.exe"
AR="C:\Program Files (x86)\Simply Fortran 3\mingw-w64\bin\ar.exe"
WRC="C:\Program Files (x86)\Simply Fortran 3\mingw-w64\bin\windres.exe"
PRJTK="C:\Program Files (x86)\Simply Fortran 3\fwin\sfprjtk.exe"
RM=rm -f

IDIR=

LDIR=


OPTFLAGS= -g

SPECIALFLAGS=$(IDIR)

RCFLAGS=-O coff

PRJ_FFLAGS=

PRJ_CFLAGS=

PRJ_LFLAGS=

FFLAGS=$(SPECIALFLAGS) $(OPTFLAGS) $(PRJ_FFLAGS) -Jmodules 

CFLAGS=$(SPECIALFLAGS) $(OPTFLAGS) $(PRJ_CFLAGS)

"build\av.o": ".\av.f95"
	@echo Compiling .\av.f95
	@$(FC) -c -o "build\av.o" $(FFLAGS) ".\av.f95"

"build\av2.o": ".\av2.f95"
	@echo Compiling .\av2.f95
	@$(FC) -c -o "build\av2.o" $(FFLAGS) ".\av2.f95"

"build\barrier.o": ".\barrier.f95"
	@echo Compiling .\barrier.f95
	@$(FC) -c -o "build\barrier.o" $(FFLAGS) ".\barrier.f95"

"build\bug.o": ".\bug.f95"
	@echo Compiling .\bug.f95
	@$(FC) -c -o "build\bug.o" $(FFLAGS) ".\bug.f95"

"build\check.o": ".\check.f95"
	@echo Compiling .\check.f95
	@$(FC) -c -o "build\check.o" $(FFLAGS) ".\check.f95"

"build\convert.o": ".\convert.f95"
	@echo Compiling .\convert.f95
	@$(FC) -c -o "build\convert.o" $(FFLAGS) ".\convert.f95"

"build\divide.o": ".\divide.f95"
	@echo Compiling .\divide.f95
	@$(FC) -c -o "build\divide.o" $(FFLAGS) ".\divide.f95"

"build\first.o": ".\first.f95"
	@echo Compiling .\first.f95
	@$(FC) -c -o "build\first.o" $(FFLAGS) ".\first.f95"

"build\increm.o": ".\increm.f95"
	@echo Compiling .\increm.f95
	@$(FC) -c -o "build\increm.o" $(FFLAGS) ".\increm.f95"

"build\io.o": ".\io.f95"
	@echo Compiling .\io.f95
	@$(FC) -c -o "build\io.o" $(FFLAGS) ".\io.f95"

"build\io2.o": ".\io2.f95"
	@echo Compiling .\io2.f95
	@$(FC) -c -o "build\io2.o" $(FFLAGS) ".\io2.f95"

"build\loop.o": ".\loop.f95"
	@echo Compiling .\loop.f95
	@$(FC) -c -o "build\loop.o" $(FFLAGS) ".\loop.f95"

"build\nbrs.o": ".\nbrs.f95"
	@echo Compiling .\nbrs.f95
	@$(FC) -c -o "build\nbrs.o" $(FFLAGS) ".\nbrs.f95"

"build\ramagic.o": ".\ramagic.f95"
	@echo Compiling .\ramagic.f95
	@$(FC) -c -o "build\ramagic.o" $(FFLAGS) ".\ramagic.f95"

"build\readdata.o": ".\readdata.f95"
	@echo Compiling .\readdata.f95
	@$(FC) -c -o "build\readdata.o" $(FFLAGS) ".\readdata.f95"

"build\test.o": ".\test.f95"
	@echo Compiling .\test.f95
	@$(FC) -c -o "build\test.o" $(FFLAGS) ".\test.f95"

"build\twodra.o": ".\twodra.f95"
	@echo Compiling .\twodra.f95
	@$(FC) -c -o "build\twodra.o" $(FFLAGS) ".\twodra.f95"

"build\xytab.o": ".\xytab.f95"
	@echo Compiling .\xytab.f95
	@$(FC) -c -o "build\xytab.o" $(FFLAGS) ".\xytab.f95"

clean: .SYMBOLIC
	@echo Deleting build\av.o and related files
	@$(RM) "build\av.o"
	@echo Deleting build\av2.o and related files
	@$(RM) "build\av2.o"
	@echo Deleting build\barrier.o and related files
	@$(RM) "build\barrier.o"
	@echo Deleting build\bug.o and related files
	@$(RM) "build\bug.o"
	@echo Deleting build\check.o and related files
	@$(RM) "build\check.o"
	@echo Deleting build\convert.o and related files
	@$(RM) "build\convert.o"
	@echo Deleting build\divide.o and related files
	@$(RM) "build\divide.o"
	@echo Deleting build\first.o and related files
	@$(RM) "build\first.o"
	@echo Deleting build\increm.o and related files
	@$(RM) "build\increm.o"
	@echo Deleting build\io.o and related files
	@$(RM) "build\io.o"
	@echo Deleting build\io2.o and related files
	@$(RM) "build\io2.o"
	@echo Deleting build\loop.o and related files
	@$(RM) "build\loop.o"
	@echo Deleting build\nbrs.o and related files
	@$(RM) "build\nbrs.o"
	@echo Deleting build\ramagic.o and related files
	@$(RM) "build\ramagic.o"
	@echo Deleting build\readdata.o and related files
	@$(RM) "build\readdata.o"
	@echo Deleting build\test.o and related files
	@$(RM) "build\test.o"
	@echo Deleting build\twodra.o and related files
	@$(RM) "build\twodra.o"
	@echo Deleting build\xytab.o and related files
	@$(RM) "build\xytab.o"
	@echo Deleting target.exe
	@$(RM) "target.exe"

"target.exe":  "build\av.o" "build\av2.o" "build\barrier.o" "build\bug.o" "build\check.o" "build\convert.o" "build\divide.o" "build\first.o" "build\increm.o" "build\io.o" "build\io2.o" "build\loop.o" "build\nbrs.o" "build\ramagic.o" "build\readdata.o" "build\test.o" "build\twodra.o" "build\xytab.o" "build\fortranprograms.prj.target"
	@echo Generating target.exe
	@$(FC) -o "target.exe" -static "build\av.o" "build\av2.o" "build\barrier.o" "build\bug.o" "build\check.o" "build\convert.o" "build\divide.o" "build\first.o" "build\increm.o" "build\io.o" "build\io2.o" "build\loop.o" "build\nbrs.o" "build\ramagic.o" "build\readdata.o" "build\test.o" "build\twodra.o" "build\xytab.o" $(LDIR) $(PRJ_LFLAGS)

all: "target.exe" .SYMBOLIC

