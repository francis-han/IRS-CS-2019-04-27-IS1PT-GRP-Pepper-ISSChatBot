import json

class GraduateProgrammeInfo:
    def __init__(self):
        self.overview_objs = self.read_objs("GraduateProgrammes/Overview.json")
        self.modules_objs = self.read_objs("GraduateProgrammes/Modules.json")
        self.admission_objs = self.read_objs("GraduateProgrammes/Admission.json")
    
    ## Read objects from json file
    def read_objs(self, json_file):
        with open(json_file, mode="r", encoding="UTF-8") as json_file:
            data_objs = json.loads(json_file.read())
        
        return data_objs

    ## Read Overview Information 
    ## Including: Next Intake, Duration, Application Deadline, Download Brochure, 
    ## Info-session, Overall Description, Learning outcomes, Recognition
    ## E.g. 
    ##        gradudateInfo = GraduateProgrammeInfo()
    ##        durationInfo = gradudateInfo.read_overview_info("Master of Technology in Intelligent Systems")["Duration"]
    ##      
    def read_overview_info(self, programme_name):
        for overview_item in self.overview_objs["Overview List"]:
            if programme_name.lower() == overview_item["name"].lower():
                return overview_item
                
        return None

    ## Read Modules Information
    ## Including: Introduction, Course Components, Focus Areas, Items
    ## and Items contains the module list which includes: name, Course Component, Focus Area, Description, Courses
    ## E.g. 
    ##        gradudateInfo = GraduateProgrammeInfo()
    ##        introInfo = gradudateInfo.read_modules_info("Master of Technology in Intelligent Systems")["Introduction"]
    ##      
    def read_modules_info(self, programme_name):
        for module_item in self.modules_objs:
            if programme_name.lower() == module_item["Graduate Programme"].lower():
                return module_item["Modules"]
                
        return None    
        
    ## Read Admission information
    ## Including: pre-requisites, English Language Proficiency, How to apply
    ## E.g. 
    ##        gradudateInfo = GraduateProgrammeInfo()
    ##        applyInfo = gradudateInfo.read_admission_info("Master of Technology in Intelligent Systems")["How to apply"]
    ##      
    def read_admission_info(self, programme_name):
        for admission_item in self.admission_objs["Admission List"]:
            if programme_name.lower() == admission_item["name"].lower():
                if "English Language Proficiency" not in admission_item:
                    admission_item["English Language Proficiency"] = self.admission_objs["English Language Proficiency"]
                if "How to apply" not in admission_item:
                    admission_item["How to apply"] = self.admission_objs["How to apply"]
                return admission_item
                
        return None        
        
if __name__ == '__main__':
   gradudateInfo = GraduateProgrammeInfo()
   durationInfo = gradudateInfo.read_overview_info("Master of Technology in Intelligent Systems")["Duration"]
   print("durationInfo: {}".format(durationInfo))
   introInfo = gradudateInfo.read_modules_info("Master of Technology in Intelligent Systems")["Introduction"]
   print("introInfo: {}".format(introInfo))
   applyInfo = gradudateInfo.read_admission_info("Master of Technology in Intelligent Systems")["How to apply"]
   print("applyInfo: {}".format(applyInfo))
   
   
