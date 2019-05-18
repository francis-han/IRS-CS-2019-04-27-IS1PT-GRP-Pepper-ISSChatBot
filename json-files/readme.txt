This folder includes all structured json files related to different programmes:

1. datautil.py
   - Used to access json data file
   - In other python application, add following
     import datautil
     
   - Then:
     1) create GraduateProgrammeInfo to access Graduate Programmes json data 
		graduateInfo = datautil.GraduateProgrammeInfo() 
	 2) create ExecutiveEducationInfo to access Executive Education json data
		executiveInfo = ExecutiveEducationInfo() 
	 3) create StackableProgrammeInfo to access Stackable Programmes json data
		stackableInfo = StackableProgrammeInfo() 
     
2. testapp.py
   - Test application script
   
3. testapp.bat
   - Test application
