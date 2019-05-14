from flask import Flask, request, make_response, jsonify
import requests

import datautil

app = Flask(__name__)

## TODO: STEP 1 
APIKEY = "cea0632e0b89b7be95111b121e724958" # Place your API KEY Here... 
#"8a81d247d650cb16469c4ba3ceb7d265"
state=0
# **********************
# UTIL FUNCTIONS : START
# **********************

def getjson(url):
    resp =requests.get(url)
    print(resp)
    return resp.json()

def getWeatherInfo(location):
    API_ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?APPID={APIKEY}&q={location}"
    data = getjson(API_ENDPOINT)
    code = data["cod"]
    if code == 200:
        return data["weather"][0]["description"]

# **********************
# UTIL FUNCTIONS : END
# **********************

# *****************************
# Intent Handlers funcs : START
# *****************************

## TODO Step 3:
def getWeatherIntentHandler(req):
    """
    Get location parameter from dialogflow and call the util function `getWeatherInfo` to get weather info
    """
    # HINT: req.get("queryResult").get("parameters").get("some-example-parameter")

    location_dict=req.get("queryResult").get("parameters").get("location")
    print (f"{location_dict}")
    for item in eval( f"{location_dict}" ): 
        if eval( f"{location_dict}" )[item]!='':
            print(item,req.get("queryResult").get("parameters").get("location").get(item))
            location = eval( f"{location_dict}" )[item] #req.get("queryResult").get("parameters").get("location").get(item)#write code here
    
    #location = "??" # Make sure location is lower case

    # Call the getWeatherInfo function with `location` as input, and store the result in `info`
    info = getWeatherInfo(f"{location}")
    
    return f"Currently in {location} , its {info}"

# ***************************
# Intent Handlers funcs : END
# ***************************


# *****************************
# WEBHOOK MAIN ENDPOINT : START
# *****************************
@app.route('/', methods=['POST'])
def webhook():
   req = request.get_json(silent=True, force=True)
   intent_name = req["queryResult"]["intent"]["displayName"]



   if intent_name == "ISS-Organisation" : ##
       
       respose_text = "Go to https://www.iss.nus.edu.sg/about-us/iss-team/teaching-staff" ## Call your getWeatherIntentHandler with req object as input. 

   elif intent_name == "CourseListIntent" : ##
       respose_text="Please kindly ask me again."
       ProgramName=req.get("queryResult").get("parameters").get("ProgramName")
       if ProgramName=='graduate programmes':
           respose_text='Graduate Diploma in Systems Analysis, Master of Technology in Enterprise Business Analytics, Master of Technology in Intelligent Systems, Master of Technology in Software Engineering'
       elif ProgramName=='executive education':
           respose_text="https://www.iss.nus.edu.sg/executive-education"
       elif ProgramName=='postgraduate':
           respose_text="ISS provides Master of Technology and executive programmes."
       elif ProgramName=='Masters':
           respose_text="Master of Technology in Enterprise Business Analytics, Master of Technology in Intelligent Systems, Master of Technology in Software Engineering"


   elif intent_name == "CoursePreRequisites" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Software Engineering':
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]
       elif CourseName=='Master of Technology in Digital Leadership':
           respose_text = gradudateInfo.read_admission_info(CourseName)["pre-requisites"]            

   elif intent_name == "CourseFeeIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       print(CourseName)
       if CourseName=='Graduate Diploma in Systems Analysis':
           respose_text="S$10,013.29"
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text="S$19,951.22 to S$21,376.46"
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text="S$20,939.90 to S$22,095.50"
       elif CourseName=='Master of Technology in Software Engineering':
           respose_text="S$17,981.35 or S$18,222.10"
       elif CourseName=='Master of Technology in Digital Leadership':
           respose_text = 'S$20,500.95'

   elif intent_name == "CourseDurationIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Software Engineering':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       elif CourseName=='Master of Technology in Digital Leadership':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Duration"]
       
   elif intent_name == "CourseDescriptionIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Software Engineering':
            respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       elif CourseName=='Master of Technology in Digital Leadership':
            respose_text = gradudateInfo.read_overview_info(CourseName)["Overall Description"]
       
   elif intent_name == "CourseScheduleIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Software Engineering':
            respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]
       elif CourseName=='Master of Technology in Digital Leadership':
            respose_text = gradudateInfo.read_overview_info(CourseName)["Next Intake"]

   elif intent_name == "ApplicationIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Software Engineering':
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]
       elif CourseName=='Master of Technology in Digital Leadership':
           respose_text = gradudateInfo.read_admission_info(CourseName)["How to apply"]            


 
   elif intent_name == "ExaminationsIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       gradudateInfo = datautil.GraduateProgrammeInfo()
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/graduate-diploma-in-systems-analysis'
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-enterprise-business-analytics'
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-intelligent-systems'
       elif CourseName=='Master of Technology in Software Engineering':
            respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-software-engineering'
       elif CourseName=='Master of Technology in Digital Leadership':
            respose_text = 'https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-digital-leadership'

   elif intent_name == "CourseModuleIntent" : ##
       respose_text="Please kindly ask me again with the course name given"
       CourseName=req.get("queryResult").get("parameters").get("CourseName")
       gradudateInfo = datautil.GraduateProgrammeInfo()
       Info = gradudateInfo.read_modules_info(CourseName)["Items"]
       if CourseName=='Graduate Diploma in Systems Analysis':           
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Enterprise Business Analytics':
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Intelligent Systems':
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Software Engineering':
           respose_text = 'Course List:'
       elif CourseName=='Master of Technology in Digital Leadership':
           respose_text = 'Module List: Digital Organisation Models,\nDigital Agility & Change Leadership,\nInnovation by Design\n'

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



if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)

