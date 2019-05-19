import json
import os
import re


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

class ExecutiveEducationInfo:
    def __init__(self):
        self.info_objs = self.read_objs('ExecutiveEducation/ExecutiveCourses.json')
        self.info_categories = [
            'Artificial Intelligence', 'CyberSecurity', 'Data Science', 'Digital Agility',
            'Digital Innovation & Design', 'Digital Products & Platforms', 'Digital Strategy & Leadership',
            'Software Systems', 'StackUp - Startup Tech Talent Development'
        ]
        self.course_data = {}
        for cat_name in self.info_categories:
            self.course_data[cat_name.lower()] = self.init_category_objs(cat_name)

    ## Read objects from json file
    def read_objs(self, json_file):
        with open(json_file, mode="r", encoding="UTF-8") as json_file:
            data_objs = json.loads(json_file.read())
        return data_objs

    ## Read course info into different category
    def init_category_objs(self, category_name):
        cat_info_objs = []
        category_name_check = category_name.lower()
        for info_obj in self.info_objs:
            if info_obj['category'].lower() == category_name_check:
                cat_info_objs.append(info_obj)
        return cat_info_objs

    ## Read course info into different category
    def read_category_objs(self, category_name):
        if category_name is None:
            return None
        if category_name.lower() in self.course_data:
            return self.course_data[category_name.lower()]
        return None

    ## Partial Match to Read course by name
    ## Course info contains: code, category, name, days, price, course_link,
    ## overview (full_name, Reference No, Duration, Course Time, Enquiry, description),
    ## takeaway, whoattend, whatcovered
    def read_course_info_by_name(self, course_name, category_name=None):
        course_name_check = course_name.lower()
        course_info_found = None
        search_in_all_objs = False
        course_list = self.read_category_objs(category_name)
        if course_list is None:
            course_list = self.info_objs
            search_in_all_objs = True
        for course_info in course_list:
            #print("check name at course_info: {}, with name: {}".format(course_info['name'], course_name_check))
            if course_info['name'].lower().find(course_name_check) >= 0:
                course_info_found = course_info
                break
        # Search again using all course list
        if course_info_found is None and not search_in_all_objs:
            course_list = self.info_objs
            for course_info in course_list:
                # print("check name at course_info: {}, with name: {}".format(course_info['name'], course_name_check))
                if course_info['name'].lower().find(course_name_check) >= 0:
                    course_info_found = course_info
                    break
        return course_info_found

    ## Read course by code
    ## Course info contains: code, category, name, days, price, course_link,
    ## overview (full_name, Reference No, Duration, Course Time, Enquiry, description),
    ## takeaway, whoattend, whatcovered
    def read_course_info_by_code(self, course_code, category_name=None):
        course_info_found = None
        course_list = self.read_category_objs(category_name)
        if course_list is None:
            course_list = self.info_objs
        for course_info in course_list:
            #print("check course_info: {}, with code: {}".format(course_info, course_code))
            if course_info['code'] == course_code:
                course_info_found = course_info
                break
        return course_info_found

class StackableProgrammeInfo:
    NICF_PREFIX_REGEX = re.compile(r"nicf\s*-\s*", re.IGNORECASE)
    SF_POSTFIX_REGEX = re.compile(r"\s*\(sf\)", re.IGNORECASE)

    def __init__(self):
        self.course_data = {}
        self.info_categories = [
            'Artificial Intelligence', 'Data Science', 'Digital Solutions Development',
            'Smart Systems & Platforms'
        ]

        self.course_data['Artificial Intelligence'.lower()] = self.read_objs('Stackable/ArtificialIntelligenceUpdated.json')['CertificateList']
        self.course_data['Data Science'.lower()] = self.read_objs('Stackable/DataScienceUpadated.json')['CertificateList']
        self.course_data['Digital Solutions Development'.lower()] = self.read_objs('Stackable/DigitalSolutionsDevelopmentUpdated.json')['CertificateList']
        self.course_data['Smart Systems & Platforms'.lower()] = self.read_objs('Stackable/SmartSystemsPlatformsUpdated.json')['CertificateList']

        self.course_cert_list = []
        for cat_name in self.info_categories:
            self.course_cert_list.extend(self.course_data[cat_name.lower()])

    ## Read objects from json file
    def read_objs(self, json_file):
        if not os.path.exists(json_file):
            return {'CertificateList': []}

        with open(json_file, mode="r", encoding="UTF-8") as json_file:
            data_objs = json.loads(json_file.read())
        return data_objs

    ## Write objects to json file
    def write_objs(self, info_obj, json_file):
        with open(json_file, mode="w", encoding="UTF-8") as json_file:
            json.dump(info_obj, json_file, indent=4)

    def read_course_list_info(self, cert_name, category_name=None):
        cert_info = self.read_cert_info(cert_name, category_name)
        if cert_info is None:
            return None
        return cert_info['CourseList']

    ## Partial match course name for particular certificate
    def read_course_in_cert_list(self, course_name, cert_name, category_name=None):
        cert_info = self.read_cert_info(cert_name, category_name)
        course_name_check = course_name.lower().strip()
        if cert_info is None:
            return None
        for course_info in cert_info['CourseList']:
            if course_info['name'].lower().find(course_name_check) >= 0:
                return course_info
        return None

    ## Partial Match to read cert info: CertificateName, Type,
    ##      CourseList (name, duration, code, category, days, price, course_link,
    ##          overview (full_name, Reference_no, Duration, Course Time, Enquiry, description),
    ##          takeaway, whoattend, whatcovered )
    def read_cert_info(self, cert_name, category_name=None):
        cert_list_check = self.read_cert_list_info(category_name)
        if cert_list_check is None:
            return None
        cert_name_check = cert_name.lower().strip()
        for cert_info in cert_list_check:
            #print("Check cert_name: {} with {}".format(cert_info['CertificateName'], cert_name))
            if cert_info['CertificateName'].lower().find(cert_name_check) >= 0:
                return cert_info
        return None

    def read_cert_list_info(self, category_name=None):
        # Read all categories certs be default
        if category_name is None:
           return self.course_cert_list
        return self.read_category_objs(category_name)

    ## Read course info into different category
    def read_category_objs(self, category_name):
        if category_name is None:
            return None
        if category_name.lower() in self.course_data:
            #print("Find cat_name: {} in data".format(category_name))
            return self.course_data[category_name.lower()]
        return None

    def update_course_code(self, executiveCourseInfo):
        self.course_data['Artificial Intelligence'.lower()] = self.read_objs('Stackable/ArtificialIntelligence.json')['CertificateList']
        self.course_data['Data Science'.lower()] = self.read_objs('Stackable/DataScience.json')['CertificateList']
        self.course_data['Digital Solutions Development'.lower()] = self.read_objs('Stackable/DigitalSolutionsDevelopment.json')['CertificateList']
        self.course_data['Smart Systems & Platforms'.lower()] = self.read_objs('Stackable/SmartSystemsPlatforms.json')['CertificateList']

        for cat_name in self.info_categories:
            info_list_in_cat = self.read_category_objs(cat_name)
            for info_item in info_list_in_cat:
                if info_item['CourseList'] is not None:
                    info_found = None
                    for info_item_course in info_item['CourseList']:
                        course_name_check = info_item_course['name'].lower().strip()
                        #print("Check course '{}'".format(course_name_check))
                        course_name_check = StackableProgrammeInfo.NICF_PREFIX_REGEX.sub('nicf- ', course_name_check)
                        #course_name_check = StackableProgrammeInfo.SF_POSTFIX_REGEX.sub('', course_name_check)

                        info_found = executiveCourseInfo.read_course_info_by_name(course_name_check, cat_name)
                        if info_found is None:
                            print("Cannot found course: '{}' (Category: '{}', check: '{}')".format(
                                info_item_course['name'], cat_name, course_name_check))
                        else:
                            ## info_item_course['code'] = info_found['code']
                            ## Add all course details from ExecutiveInfo to StackableInfo
                            for info_item_key in info_found:
                                info_item_course[info_item_key] = info_found[info_item_key]
                            #print("Found course (category: {}) '{}'".format(cat_name, course_name_check))
            info_objs = {'CertificateList': info_list_in_cat}
            out_file_path = ''
            if cat_name.lower() == 'artificial intelligence':
                out_file_path = 'Stackable/ArtificialIntelligenceUpdated.json'
            elif cat_name.lower() == 'data science':
                out_file_path = 'Stackable/DataScienceUpdated.json'
            elif cat_name.lower() == 'digital solutions development':
                out_file_path = 'Stackable/DigitalSolutionsDevelopmentUpdated.json'
            elif cat_name.lower() == 'smart systems & platforms':
                out_file_path = 'Stackable/SmartSystemsPlatformsUpdated.json'

            if out_file_path != '':
                self.write_objs(info_objs, out_file_path)

class StaffInfo:
    def __init__(self):
        self.staff_data = self.read_objs('Staff/TeachingStaff.json')['StaffList']

    ## Read objects from json file
    def read_objs(self, json_file):
        if not os.path.exists(json_file):
            return {'CertificateList': []}

        with open(json_file, mode="r", encoding="UTF-8") as json_file:
            data_objs = json.loads(json_file.read())
        return data_objs

    ## Read staff info which includes: name, title, courseNameList
    ##
    def read_staff_info(self, staff_name):
        staff_name_check = staff_name.lower().strip()
        for staff_info in self.staff_data:
            if staff_info['name'].lower().find(staff_name_check) >= 0:
                return staff_info
        return None


class DataInfo:
    GRADUATE_INFO = GraduateProgrammeInfo()
    EXECUTIVE_INFO = ExecutiveEducationInfo()
    STACKABLE_INFO = StackableProgrammeInfo()
    STAFF_INFO = StaffInfo()
    CONTEXT_INFO = {}

    def __init__(self):
        self.data = ""

    @staticmethod
    def get_graduate_info():
        return DataInfo.GRADUATE_INFO

    @staticmethod
    def get_executive_info():
        return DataInfo.EXECUTIVE_INFO

    @staticmethod
    def get_stackable_info():
        return DataInfo.STACKABLE_INFO

    @staticmethod
    def get_context_info():
        return DataInfo.CONTEXT_INFO

    @staticmethod
    def get_staff_info():
        return DataInfo.STAFF_INFO

if __name__ == '__main__':
   info = DataInfo()
   gradudateInfo = info.get_graduate_info()
   durationInfo = gradudateInfo.read_overview_info("Master of Technology in Intelligent Systems")["Duration"]
   print("durationInfo: {}".format(durationInfo))
   introInfo = gradudateInfo.read_modules_info("Master of Technology in Intelligent Systems")["Introduction"]
   print("introInfo: {}".format(introInfo))
   applyInfo = gradudateInfo.read_admission_info("Master of Technology in Intelligent Systems")["How to apply"]
   print("applyInfo: {}".format(applyInfo))
   executiveInfo = info.get_executive_info()
   dataScienceCourses = executiveInfo.read_category_objs('Data Science')
   print("Date science info found: {}".format(len(dataScienceCourses)))
   aiCourse = executiveInfo.read_course_info_by_code('ISSM', 'Artificial Intelligence')
   print("AI course info found: {}".format(aiCourse['overview']['full_name']))
   mrCourse = executiveInfo.read_course_info_by_name('Machine Reasoning')
   print("MR course info found: {}".format(mrCourse['overview']['full_name']))
   stackableInfo = info.get_stackable_info()
   #stackableInfo.update_course_code(executiveInfo)
   ai_cert_list = stackableInfo.read_cert_list_info("Artificial Intelligence")
   print("AI cert list: {}".format(len(ai_cert_list)))
   ai_cert_info = stackableInfo.read_cert_info("Intelligent Reasoning Systems")
   print("Intelligent Reasoning Systems cert: {}".format(ai_cert_info))
   ai_course_info = stackableInfo.read_course_in_cert_list(
       course_name="Machine Reasoning", cert_name="Intelligent Reasoning Systems",
       category_name="Artificial Intelligence")
   print("Machine Reasoning course: {}".format(ai_course_info))

   staffInfo = info.get_staff_info()
   sam_staff = staffInfo.read_staff_info('Gu')
   print("Staff Gu: {}".format(sam_staff))
   