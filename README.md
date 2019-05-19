## SECTION 1 : PROJECT TITLE
## Patient Matching System

<img src="Miscellaneous/Banner.gif"
     style="float: left; margin-right: 0px;" />

---
## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
This project is a continuation from the Depression Screening System group project completed during the Machine Reasoning course. As a recap, the Depression Screening System deals with the problem of depression in youths and vulnerable segments of the community going undetected and untreated. It serves as an early warning system to put a spotlight on those vulnerable individuals who are displaying symptoms of depression. These vulnerable individuals can be spotted through the PHQ-9 Survey framework devised with the Depression Screening System. The output from that system is to provide a diagnosis (with a PHQ-9 score) on the level of severity of depression the individuals are having.
In this phase of project, the objective is to use the PHQ-9 scores of the individuals and match them to the many practitioners in the community partners, hospitals and IMH. 
Why Patient Matching? When we churn out a list of patients in batches as part of the PHQ-9 Survey, there is also a need to do the matching with practitioners in batches. There are some challenges to match patients to practitioners. First of all, practitioners fall into roughly 3 categories – Counsellors, Psychologists, Psychiatrists. Then there is the time availability of the practitioners, as well as language ability, which are all hard constraints. Also there is location preference and gender preference which are soft constraints. Then there is the cost based on the practitioner selected, which is a soft constraint to minimize it.
Using the State Space Search techniques embedded in the OptaPlanner, the Patient Matching System is able to optimally match a group of patients against a group of practitioners. The detail of how this match is executed will be covered in the next chapters.
This system provides benefits to those who are diagnosed with depression by matching appropriate practitioners with the right expertise and in accordance to some set constraints.



---
## SECTION 3 : CREDITS / PROJECT CONTRIBUTION


| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) | Email (Optional) |
| :------------ |:---------------:| :-----| :-----|
| CAO LIANG            | A0012884E | Architect, Application Logic, DROOLS Rules, Benchmark and Integration    | e0384184@u.nus.edu |
| GENG LIANGYU         | A0195278M | Web Application, Data Repository and Landing Page                        | e0384909@u.nus.edu |
| HAN DONGCHOU FRANCIS | A0195414A | Team Lead, Documentation, and Submission                                 | e0385045@u.nus.edu |
| ONG BOON PING        | A0195172B | KIE Workflow, DROOLS Rules, and Data Structure                           | e0384803@u.nus.edu |
| TAN CHIN GEE         | A0195296M | Domain Expert and Documentation                                          | e0384927@u.nus.edu |


---
## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

[Introduction Video](https://youtu.be/RXYVsCB5vHU)

---
## SECTION 5 : USER GUIDE

`<Github File Link>` : <https://github.com/francis-han/IRS-RS-2019-03-09-IS1PT-GRP-Pepper-PatientMatchingSystem/blob/master/UserGuide/Users%20Manual_Patient%20Matching.docx>

### [ * ] In order to run the system, you need Java 8 or later version.

> Download this file from https://github.com/francis-han/IRS-RS-2019-03-09-IS1PT-GRP-Pepper-PatientMatchingSystem/tree/master/SystemCodes/Submission/IRS-RS-2019-03-09-IS1PT-GRP-Pepper-PatientMatchingSystem.zip

> The file contains both executable jar and db files.

> Unzip the zip file, there will be a folder named "rs-patient-matching" generated.

> Open cmd/bash window, go to the above "rs-patient-matching" folder, eg: cd C:\Users\ Desktop\rs-patient-matching\

> Run command: java -jar rs-patient-matching-0.1.0.jar

> Open link: http://localhost:8090/ in browser.

> To run our system, type the command “java -jar rs-patient-matching-0.1.0.jar”.

> **Open your preferred browser and go to the URL** “http://localhost:8090/”


---
## SECTION 6 : PROJECT REPORT / PAPER

`<Github File Link>` : <https://github.com/francis-han/IRS-RS-2019-03-09-IS1PT-GRP-Pepper-PatientMatchingSystem/blob/master/ProjectReport/Project%20Report%20V2.pdf>


---
## SECTION 7 : MISCELLANEOUS

### BENCHMARK OF DIFFERENT SEARCH TECHNIQUES

A benchmark test was conducted against the various search algorithms as follows. We have made some observations as follows. All hard constraints are met. The level of soft constraints being met varies across the different search algorithms.

> **First Fit Decreasing**
> This is the slowest search algorithm in our scenario. This demonstrates the main characteristic of construction heuristic vs metaheuristic.

> **Tabu Search**
> This search made the fastest progress in the beginning but took a long time to converge into global optimum compared to Late Aceptance.

> **Simulated Annealing**
> This is the slowest search.

> **Late Acceptance**
> This is the fatest to reach the global optimum.

> **Step Counting Hill Climbing**
> This has reasonable performance and reached global optimum quite fast.



<img src="Miscellaneous/SearchResults.gif"
     style="float: left; margin-right: 0px;" />

