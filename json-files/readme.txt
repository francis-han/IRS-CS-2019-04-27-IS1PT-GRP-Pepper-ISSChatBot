This folder includes all structured json files related to different programmes:

1. datautil.py
   - Used to access json data file
   - In other python application, add following
     import datautil
     
   - Then create DataInfo to use
     dataInfo = datautil.DataInfo()

     graduateInfo = dataInfo.get_graduate_info()
     executiveInfo = dataInfo.get_executive_info()
     stackableInfo = dataInfo.get_stackable_info()
     staffInfo = info.get_staff_info()

     contextInfo = dataInfo.get_context_info()
     
2. testapp.py
   - Test application script
   
3. testapp.bat
   - Test application
