from flask import Flask, request, make_response, jsonify
import requests
import os
import datautil
import re

app = Flask(__name__)

# **********************
# UTIL FUNCTIONS : START
# **********************

#Explaination: The dialogflow is returning the request in json format
def getjson(url):
    resp =requests.get(url)
    print(resp)
    return resp.json()


# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************

#Explaination: The webhook is called in the Flask app. It processes the json format data sent by dialogflow through API commands
@app.route('/', methods=['POST'])
def webhook():
   #Explaination: req is used throughout the function. It is actually now a python dictionary-array structure converted from json.
   req = request.get_json(silent=True, force=True)
   #Explaination: queryResult consists of all the data sent by dialogflow. It consists of intent name. Intent name determines different data processing.
   intent_name = req["queryResult"]["intent"]["displayName"]
   #Explaination: Certain intents require crucial entity for the data processing. Hence, if the crucial entity is missed by user, it is captured by intent_state.txt. "NO999" indicates normal processing based on the intent. However, if it records certain intent name defined in dialogflow, it will replace the "NO999" characters.
   intent_state=open("intent_state.txt","r")
   line=intent_state.readline()
   parsed_param=0
   if line.find("NO999")!=-1:
       print("999")
       #Explaination: process as usual
       intent_name = req["queryResult"]["intent"]["displayName"]
   else:
       print("998")
       #Explaination: continue to process previous query with new inputs. parsed_param=1 is used as flag at intent level
       intent_name = line.replace("\n","")
       parsed_param=1
   intent_state.close()
   print(intent_name)

   #Explaination: This portion process fulfillment webhook from knowledge base. Return immediately. respose_text is the returned text and it will be return as json format.
   if intent_name.find("Knowledge")!=-1:
       respose_text=""
       print(req["queryResult"]['knowledgeAnswers']['answers'])
       elemm=req["queryResult"]['knowledgeAnswers']['answers']
       for ele in elemm:
            if ele['answer'] is not None:
                respose_text=ele['answer']
                print (respose_text)
                #Explaination: return in json format to dialogflow.
                return make_response(jsonify({'fulfillmentText': respose_text}))

   #Explaination: This portion process fulfillment webhook when there is fallback as a result of dialogflow do not understand the query. Return immediately.
   if intent_name == "Default Fallback Intent":
       #Explaination: initial feedback
       respose_text = "Please kindly repeat again. Thanks!"
       #Explaination: try to process what dialogflow model cannot predict by extracting raw query text
       temp_str=req.get("queryResult").get("queryText")     
       #Explaination: covers certificate name that has similarity to postgraduate name.
       #Explaination: search thru all stackable course thru json file that consists of all course info.
       stackableInfo = datautil.DataInfo().get_stackable_info()
       for certtype in ['Artificial Intelligence', 'Data Science', 'Digital Solutions Development', 'Smart Systems & Platforms']:
           for cert in stackableInfo.read_cert_list_info(certtype):
               #print(cert['CertificateName'])
               for cour in cert["CourseList"]:
                   if temp_str.lower().find(cour["name"].lower())!=-1:
                       respose_text=cour["course_link"] 
       executiveInfo = datautil.DataInfo().get_executive_info()   
       #Explaination: search thru all executive course thru json file that consists of all course info.
       try:
           respose_text=executiveInfo.read_course_info_by_name(temp_str)["course_link"]
       except:
           pass
       if respose_text != "Please kindly repeat again. Thanks!":
           return make_response(jsonify({'fulfillmentText': respose_text}))

       staffInfo = datautil.DataInfo().get_staff_info()
       if temp_str.lower().find("gu zhan")!=-1 or temp_str.lower().find("sam gu")!=-1:
           respose_text="Gu Zhan is teaching: "
           for cour in staffInfo.read_staff_info("GU Zhan") ['courseNameList']:
               respose_text+=cour+","
       if temp_str.lower().find("tian jing")!=-1 or temp_str.lower().find("jing tian")!=-1:
           respose_text="Tian Jing is teaching: "
           for cour in staffInfo.read_staff_info("TIAN Jing") ['courseNameList']:
               respose_text+=cour+","
       if temp_str.lower().find("aobo wang")!=-1 or temp_str.lower().find("wang aobo")!=-1:
           respose_text="Wang Aobo is teaching: "
           for cour in staffInfo.read_staff_info("WANG Aobo") ['courseNameList']:
               respose_text+=cour+","
       if temp_str.lower().find("fan zhen zhen")!=-1 or temp_str.lower().find("zhen zhen")!=-1:
           respose_text="Fan Zhen Zhen is teaching: "
           for cour in staffInfo.read_staff_info("FAN Zhen Zhen") ['courseNameList']:
               respose_text+=cour+","
       if temp_str.lower().find("zhu fang ming")!=-1 or temp_str.lower().find("fang ming")!=-1:
           respose_text="Zhu Fang Ming is teaching: "
           for cour in staffInfo.read_staff_info("ZHU Fang Ming") ['courseNameList']:
               respose_text+=cour+","
       if temp_str.lower().find("Barry Adrian SHEPHERD".lower())!=-1:
           respose_text="Barry Adrian SHEPHERD is teaching: "
           for cour in staffInfo.read_staff_info("Barry Adrian SHEPHERD") ['courseNameList']:
               respose_text+=cour+","



       #staffi = staffInfo.read_staff_info(LecturersName) ['courseNameList'] 

       if temp_str.lower().find("Intelligent System".lower())!=-1:
           respose_text="https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-intelligent-systems"
       elif temp_str.lower().find("knowledge engineering".lower())!=-1:
           respose_text="https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-intelligent-systems"
       elif temp_str.lower().find("Business Analytics".lower())!=-1:
           respose_text="https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-enterprise-business-analytics"
       elif temp_str.lower().find("Artificial Intelligence".lower())!=-1:
           respose_text="Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence" 
       elif temp_str.lower().find("Digital Leadership".lower())!=-1:
           respose_text="Go to https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-digital-leadership" 
       elif temp_str.lower().find("software engineering".lower())!=-1:
           respose_text="https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-software-engineering" 
       elif temp_str.lower().find("system analysis".lower())!=-1:
           respose_text="https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/graduate-diploma-in-systems-analysis" 

       elif temp_str.lower().find("Artificial Intelligence".lower())!=-1:
           respose_text="Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence" 
       elif temp_str.lower().find("Reasoning".lower())!=-1:
           respose_text="Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence" 
       elif temp_str.find("Recognition")!=-1:
           respose_text="Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence" 
       elif temp_str.find("Sensing")!=-1:
           respose_text="Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence" 
       return make_response(jsonify({'fulfillmentText': respose_text}))

   #Explaination: This portion process ISS-Organisation intent fulfillment in dialogflow. Return webpage link
   if intent_name == "ISSLecturersIntent" : ##
       LecturersName0=req.get("queryResult").get("parameters").get("LecturersName")
       LecturersName=""
       if type(LecturersName0)==type([]):
           if len(LecturersName0)>=1:
               LecturersName=LecturersName0[0]
       elif type(LecturersName0)==type(""):
           LecturersName=LecturersName0
       staffInfo = datautil.DataInfo().get_staff_info()
       if LecturersName=="" or LecturersName==None:
           respose_text = "Go to https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff" 
       else:
           staffi = staffInfo.read_staff_info(LecturersName) ['courseNameList'] 
           respose_text=LecturersName+" is lecturing on the following courses: "
           for cour in staffi:
               respose_text+=cour+","
           respose_text=respose_text[:-1]    
       return make_response(jsonify({'fulfillmentText': respose_text}))

   #Explaination: This portion process CourseListIntent intent fulfillment in dialogflow. Return webpage link for each program category
   elif intent_name == "CourseListIntent" : ##
       #Explaination: initial response
       respose_text="Please kindly ask me again."
       #Explaination: ProgramName is an parameter in dialogflow. It is defined as entity in dialogflow.
       ProgramName0=req.get("queryResult").get("parameters").get("ProgramName")
       #Explaination: processing the program name. Avoid cases where program name is returned as array of string rather than string.
       ProgramName=""
       if type(ProgramName0)==type([]):
           if len(ProgramName0)>=1:
               ProgramName=ProgramName0[0]
       elif type(ProgramName0)==type(""):
           ProgramName=ProgramName0
       if ProgramName=='graduateProgrammes':
           respose_text='Graduate Diploma in Systems Analysis, Master of Technology in Enterprise Business Analytics, Master of Technology in Intelligent Systems, Master of Technology in Software Engineering'
       elif ProgramName=='executive education':
           respose_text="https://www.iss.nus.edu.sg/executive-education"
       elif ProgramName=='postgraduate':
           respose_text="ISS provides Master of Technology and executive programmes."
       elif ProgramName=='Masters':
           respose_text="Master of Technology in Enterprise Business Analytics, Master of Technology in Intelligent Systems, Master of Technology in Software Engineering"


   #Explaination: This portion process CoursePreRequisites intent fulfillment in dialogflow. A json file is created to structurize information gathered from ISS webpage. Return respective pre-requisites based on json file.
   elif intent_name == "CoursePreRequisites" : ##
       #Explaination: Initial response
       respose_text="Please kindly ask me again with the course name given."
       #Explaination: Getting knowledge from local json file.
       gradudateInfo = datautil.GraduateProgrammeInfo()
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
       #Explaination: getting course name from the parameter parsed from dialogflow. If the dialogflow do not understand the query, it is likely that it returns empty string. 
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #print(CourseName0)
       #CourseName=""
       #Explaination: let CourseName be overriden by parameter query result. If course name parameter is not a valid return when the 1st query is not complete, then course name parameter is null. The processed raw query data (processed earlier by processContinuedIntent subroutine call) will then used as course name
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)
       #Explaination: generate response based on course name.
       if CourseName=='Graduate Diploma in Systems Analysis'  and ProgramName=="graduateProgrammes":           
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics'  and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Digital Leadership'  and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]       

       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"

       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()

   #Explaination: This portion process CourseFeeIntent intent fulfillment in dialogflow. Return strings based on full time/part time and student nationality.
   elif intent_name == "CourseFeeIntent" : ##
       CourseName=""
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
           
       respose_text="Please kindly ask me again with the course name given."
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       print(CourseName)
       #Explaination: optional. Full time/part time in query
       CourseType=req.get("queryResult").get("parameters").get("CourseType")
       #Explaination: optional. Student nationality in query
       StudentIdentity=req.get("queryResult").get("parameters").get("StudentIdentity")
       #Explaination: compulsory. dialogflow will generate the prompt to ask whether user is taking master course or executive course
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)
       #Explaination: answer is generated based on course name. Course Name is mandatory. If there is no course name in this query, next query is expected to be the course name.
       if CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="graduateProgrammes":
           #Explaination: default answer. Full time/part time and student nationality allows answers to be narrow down but not mandatory.
           respose_text="Full Time: S$10,013.29 (International Student: S$23,563.29 or S$37,463.29 Check service obligation)"
           if CourseType=="Part Time":
               respose_text="No part time course"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="No part time course"
               elif StudentIdentity=="International":
                   respose_text="No part time course"
           elif CourseType=="Full Time":
               respose_text="S$10,013.29"
               if StudentIdentity=="Singaporean":
                   respose_text="S$10,013.29"
               elif StudentIdentity=="Singapore PR":
                   respose_text="S$15,663.29"
               elif StudentIdentity=="International":
                   respose_text="S$23,563.29 or S$37,463.29 (Check service obligation)"
           elif StudentIdentity=="Singaporean":
               respose_text="S$10,013.29"
           elif StudentIdentity=="Singapore PR":
               respose_text="S$15,663.29"
           elif StudentIdentity=="International":
               respose_text="S$23,563.29 or S$37,463.29 (Check service obligation)"
           respose_text=CourseName+":"+respose_text

       elif CourseName=='Master of Technology in Enterprise Business Analytics'  and ProgramName=="graduateProgrammes":
           respose_text="S$19,951.22 to S$21,376.46 (International Student: S$52,023.40 to S$56,774.20)"
           if CourseType=="Part Time":
               respose_text="Part Time: S$19,951.22 to S$21,376.46 (International Student: S$52,023.40 to S$56,774.20)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$19,951.22 to S$21,376.46"
               elif StudentIdentity=="International":
                   respose_text="S$52,023.40 to S$56,774.20"
           elif CourseType=="Full Time":
               respose_text="Full Time: S$19,951.22 to S$21,376.46 (International Student: S$52,023.40 to S$56,774.20)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$19,951.22 to S$21,376.46"
               elif StudentIdentity=="International":
                   respose_text="S$52,023.40 to S$56,774.20"
           elif StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
               respose_text="S$19,951.22 to S$21,376.46"
           elif StudentIdentity=="International":
               respose_text="S$52,023.40 to S$56,774.20 "
           respose_text=CourseName+":"+respose_text

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="graduateProgrammes":
           respose_text="S$20,939.90 to S$22,095.50 (International Student: S$55,319.00 to S$59,171.00)"
           if CourseType=="Part Time":
               respose_text="Full Time: S$20,939.90 to S$22,095.50 (International Student: S$55,319.00 to S$59,171.00)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$20,939.90 to S$22,095.50"
               elif StudentIdentity=="International":
                   respose_text="S$55,319.00 to S$59,171.00"
           elif StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
               respose_text="S$20,939.90 to S$22,095.50"
           elif StudentIdentity=="International":
               respose_text="S$55,319.00 to S$59,171.00"
           elif CourseType=="Full Time":
               respose_text="Full Time: S$20,939.90 to S$22,095.50 (International Student: S$55,319.00 to S$59,171.00)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$20,939.90 to S$22,095.50"
               elif StudentIdentity=="International":
                   respose_text="S$55,319.00 to S$59,171.00"
           elif StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
               respose_text="S$20,939.90 to S$22,095.50"
           elif StudentIdentity=="International":
               respose_text="S$55,319.00 to S$59,171.00"
           respose_text=CourseName+":"+respose_text

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="graduateProgrammes":
           respose_text="S$17,981.35 or S$18,222.10 (International Student: S$45,956.50 or S$46,759.00)"
           if CourseType=="Part Time":
               respose_text="Part Time: S$17,981.35 or S$18,222.10 (International Student: S$45,956.50 or S$46,759.00)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$17,981.35 or S$18,222.10"
               elif StudentIdentity=="International":
                   respose_text="S$45,956.50 or S$46,759.00"
           elif CourseType=="Full Time":
               respose_text="Full Time: S$17,981.35 or S$18,222.10 (International Student: S$45,956.50 or S$46,759.00)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$17,981.35 or S$18,222.10"
               elif StudentIdentity=="International":
                   respose_text="S$45,956.50 or S$46,759.00"
           elif StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
               respose_text="S$17,981.35 or S$18,222.10"
           elif StudentIdentity=="International":
               respose_text="S$45,956.50 or S$46,759.00"
           respose_text=CourseName+":"+respose_text

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="graduateProgrammes":
           respose_text = 'Full Time: S$20,500.95 (International Student: S$22,750.95),\n Part Time: S$10,257.90 (International Student: S$11,382.90)'
           if CourseType=="Part Time":
               respose_text="Part Time: S$10,257.90 (International Student: S$11,382.90)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$10,257.90"
               elif StudentIdentity=="International":
                   respose_text="S$11,382.90"
           elif CourseType=="Full Time":
               respose_text="Full Time: S$20,500.95 (International Student: S$22,750.95)"
               if StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
                   respose_text="S$20,500.95"
               elif StudentIdentity=="International":
                   respose_text="S$22,750.95"
           elif StudentIdentity=="Singaporean" or StudentIdentity=="Singapore PR":
               respose_text="Full Time: S$20,500.95 ,\n Part Time: S$10,257.90 "
           elif StudentIdentity=="International":
               respose_text="Full Time: S$22,750.95 ,\n Part Time: S$11,382.90"
           respose_text=CourseName+":"+respose_text

       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"


       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()

   #Explaination: This portion process CourseDurationIntent intent fulfillment in dialogflow. An internal json file is created to structurize information gathered from ISS webpage. Return duration of respective postgraduate course based on json file.
   elif intent_name == "CourseDurationIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)

       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0

       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)

       if CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="graduateProgrammes":           
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Intelligent Systems' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Software Engineering' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Digital Leadership':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]

       #elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":        
           #stackableInfo = datautil.DataInfo().get_stackable_info()
           #respose_text=""
           #for cert in stackableInfo.read_cert_list_info("Smart Systems & Platforms"):
           #     
           #     respose_text+=cour['name']+":"+cour['duration']+" \n"
           #print(respose_text)
           
           
       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"

       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()
       
   #Explaination: This portion process CourseDescriptionIntent intent fulfillment in dialogflow. An internal json file is created to structurize information gathered from ISS webpage. Return respective postgraduate course description based on json file.
   elif intent_name == "CourseDescriptionIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)
       if CourseName=='Graduate Diploma in Systems Analysis'  and ProgramName=="graduateProgrammes":           
           respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Intelligent Systems' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Software Engineering' and ProgramName=="graduateProgrammes":
            respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Digital Leadership'  and ProgramName=="graduateProgrammes":
            respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]

       #Explaination: extract cert list from json file
       elif CourseName=='Graduate Diploma in Systems Analysis'  and ProgramName=="executive education":           
           stackableInfo = datautil.DataInfo().get_stackable_info()
           respose_text="There is a number course related: "
           for cert in stackableInfo.read_cert_list_info("Digital Solutions Development"):
                respose_text+=cert['CertificateName']+" "                
           respose_text+=". "+"Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ for further info."+" \n"


       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           stackableInfo = datautil.DataInfo().get_stackable_info()
           respose_text="There is a number course related: "
           for cert in stackableInfo.read_cert_list_info("Data Science"):
                respose_text+=cert['CertificateName']+" "                
           respose_text+=". Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ for further info."

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           stackableInfo = datautil.DataInfo().get_stackable_info()
           respose_text="There is a number course related: "
           for cert in stackableInfo.read_cert_list_info("Artificial Intelligence"):
                respose_text+=cert['CertificateName']+" "                
           respose_text+=" . Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems for further info."

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           stackableInfo = datautil.DataInfo().get_stackable_info()
           respose_text="There is a number course related: "
           for cert in stackableInfo.read_cert_list_info("Smart Systems & Platforms"):
                respose_text+=cert['CertificateName']+" "                

           respose_text+=" . Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering for further info"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"

           
       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()

   #Explaination: This portion process CourseScheduleIntent intent fulfillment in dialogflow. An internal json file is created to structurize information gathered from ISS webpage. Return next intake of each course based on json file.
   elif intent_name == "CourseScheduleIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)
       if CourseName=='Graduate Diploma in Systems Analysis'  and ProgramName=="graduateProgrammes":           
           respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Intelligent Systems' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Software Engineering' and ProgramName=="graduateProgrammes":
            respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="graduateProgrammes":
            respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]

       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"

       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()

   #Explaination: This portion process ApplicationIntent intent fulfillment in dialogflow. An internal json file is created to structurize information gathered from ISS webpage. Return application/admission info of each course based on json file.
   elif intent_name == "ApplicationIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)

       #print(CourseName)
       #print('Graduate Diploma in Systems Analysis' == CourseName)
       if CourseName=='Graduate Diploma in Systems Analysis'  and ProgramName=="graduateProgrammes":           
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Intelligent Systems' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Software Engineering' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="graduateProgrammes":
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"] 

       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"
           
       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()

   #Explaination: This portion process ExaminationsIntent intent fulfillment in dialogflow. An internal json file is created to structurize information gathered from ISS webpage. Return examination info of each course based on json file.
   elif intent_name == "ExaminationsIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)
       if CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="graduateProgrammes":           
           respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/graduate-diploma-in-systems-analysis'
       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="graduateProgrammes":
           respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-enterprise-business-analytics'
       elif CourseName=='Master of Technology in Intelligent Systems' and ProgramName=="graduateProgrammes":
           respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-intelligent-systems'
       elif CourseName=='Master of Technology in Software Engineering' and ProgramName=="graduateProgrammes":
            respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-software-engineering'
       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="graduateProgrammes":
            respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-digital-leadership'

       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"

       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()
      
   #Explaination: This portion process CourseModuleIntent intent fulfillment in dialogflow. An internal json file is created to structurize information gathered from ISS webpage. Return module list of each course based on json file.
   elif intent_name == "CourseModuleIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       #Explaination: Start to get course name
       CourseName=""
       #Explaination: If previous query does not consists of the course name, try to get the course name in current query by processing raw query text generated by dialogflow.
       if parsed_param==1:
           CourseName=processContinuedIntent(req)
       CourseName0=req.get("queryResult").get("parameters").get("CourseName")
       #CourseName=""
       if type(CourseName0)==type([]):
           if len(CourseName0)>=1:
               CourseName=CourseName0[0]
       elif type(CourseName0)==type(""):
           CourseName=CourseName0
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       print(ProgramName)
       if CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="graduateProgrammes":           
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="graduateProgrammes":
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Intelligent Systems' and ProgramName=="graduateProgrammes":
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Software Engineering' and ProgramName=="graduateProgrammes":
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="graduateProgrammes":
           respose_text = 'Module List: Digital Organisation Models,\nDigital Agility & Change Leadership,\nInnovation by Design\n'

       elif CourseName=='Graduate Diploma in Systems Analysis' and ProgramName=="executive education":
           respose_text="There are several courses related to digital solution. Go to https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms"

       elif CourseName=='Master of Technology in Enterprise Business Analytics' and ProgramName=="executive education":
           respose_text="There are course related to data science, predictive modelling and forecasting, business analytics and big data. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/ and https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science . For data protection and cyber security, go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity"

       elif CourseName=='Master of Technology in Intelligent Systems'  and ProgramName=="executive education":
           respose_text="There are course related to artificial intelligent, machine/artificial reasoning, software bot, robotic systems and intelligent sensing. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence and https://www.iss.nus.edu.sg/stackable-certificate-programmes/intelligent-systems "

       elif CourseName=='Master of Technology in Software Engineering'  and ProgramName=="executive education":
           respose_text="There are course related to smart/scalable/ubiquitous systems. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/software-engineering"

       elif CourseName=='Master of Technology in Digital Leadership' and ProgramName=="executive education":
           respose_text="There are course related to digital leadership and strategy. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership"

       elif CourseName=='Practical Language Processing':
           respose_text="There is course related to language processing, text analysis, text data mining. Go to https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics/graduate-certificate-in-practical-language-processing"

       elif CourseName=='Digital Innovation':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design"

       elif CourseName=='Digital Agility':
           respose_text="There is course related to digital design and innovation. Go to https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility"

       #Explaination: if course name is unobtainable, record the intent name in intent_state.txt     
       elif CourseName=="":
           int_stat=open("intent_state.txt","w+")
           print("333")
           int_stat.write(intent_name+"\n")
           int_stat.close()
           return make_response(jsonify({'fulfillmentText': respose_text}))

       gradudateInfo = datautil.GraduateProgrammeInfo()
       Info = gradudateInfo.read_modules_info(CourseName)["Items"]

       if respose_text == 'Course List:':
           respose_text="Module List:\n"
           for item in Info:
               for course in item["Courses"]:
                   respose_text+=course+",\n"
       respose_text=respose_text[:-2]

   else:
       respose_text = "Please repeat again with correct intent"
   # Branching ends here

   # Finally sending this response to Dialogflow.
   return make_response(jsonify({'fulfillmentText': respose_text}))

# ***************************
# WEBHOOK MAIN ENDPOINT : END
# ***************************

#Explaination: This subroutine is called when intent_state.txt records a valid unfinished intent query in the last conversation. As prompt is given to user to provide the correct course name, the subroutine is expected to crunch the raw query text. This subroutine is restricted to unfinished query which lack of course name info.
def processContinuedIntent(req):
   if 1:
       CourseName=""
       if 1:
           #Explaination: reset the state to proceed as per normal next time.
           int_stat0=open("intent_state.txt","w+")
           print ("799")
           print(req.get("queryResult").get("queryText"))
           int_stat0.write("NO999\n")
           int_stat0.close()
           parsed_param=0
           #Explaination: get the raw query text
           temp_str=req.get("queryResult").get("queryText")
           #Explaination: replace with synonyms
           temp_str=temp_str.replace("IS","intelligent")
           temp_str=temp_str.replace("KE","intelligent")
           temp_str=temp_str.lower()

           temp_str=temp_str.replace("reasoning","intelligent").replace("robotic","intelligent").replace("sensing","intelligent").replace("software agent","intelligent")
           temp_str=temp_str.replace("smart systems","software").replace("smart system","software").replace("smart","software").replace("scalable systems","software").replace("scalable system","software").replace("scalable","software").replace("ubiquitous systems","software").replace("ubiquitous system","software").replace("ubiquitous","software")
           temp_str=temp_str.replace("business analytics","business").replace("business analytic","business").replace("analytics","business").replace("analytic","business").replace("big data","business").replace("predictive modeling and forecasting","business").replace("predictive modeling","business").replace("modeling","business").replace("forecasting","business").replace("forecast","business").replace("model","business")
           temp_str=temp_str.replace("digital solution","analysis")

           temp_str=temp_str.replace("mtech se","software").replace("mtech in se","software").replace("master in se","software").replace("masters in se","software")
           temp_str=temp_str.replace("mtech ebac","business").replace("mtech in ebac","business").replace("master in ebac","business").replace("masters in ebac","business").replace("ebac","business")
           temp_str=temp_str.replace("mtech dl","digital").replace("mtech in dl","digital").replace("master in dl","digital").replace("masters in dl","digital")
           temp_str=temp_str.replace("diploma sa","analysis").replace("diploma in sa","analysis").replace("gdipsa","analysis")
           temp_str=temp_str.replace("mtech is","intelligent").replace("mtech in is","intelligent").replace("master in is","intelligent").replace("masters in is","intelligent")
           temp_str=temp_str.replace("mtech ke","intelligent").replace("mtech in ke","intelligent").replace("master in ke","intelligent").replace("masters in ke","intelligent").replace("knowledge","intelligent")


           #Explaination: analyze each word inside the raw query
           buff=re.split( " ",temp_str )           
           for elem in buff:
                #Explaination: avoid processing on words with commonality among postgraduate courses
                if elem in ["master","of","technology","in","masters","system","systems","engineering"]: continue
                #Explaination: finding matching course and return the correct course name. Return empty string if it fails.
                for coursee in [ 'Graduate Diploma in Systems Analysis', 'Master of Technology in Enterprise Business Analytics', 'Master of Technology in Intelligent Systems', 'Master of Technology in Software Engineering', 'Master of Technology in Digital Leadership']:
                    if coursee.lower().find(elem)!=-1:
                        CourseName=coursee
                        break
           return CourseName


if __name__ == '__main__':
   intent_state00=open("intent_state.txt","w+")
   intent_state00.write("NO999\n")
   intent_state00.close()
   newPort = int(os.environ.get("PORT", 5000))
   app.run(debug=False, host='0.0.0.0', port=newPort)

