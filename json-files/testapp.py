import datautil

def test_datautil():
    gradudateInfo = datautil.GraduateProgrammeInfo()
    durationInfo = gradudateInfo.read_overview_info("Master of Technology in Intelligent Systems")["Duration"]
    print("durationInfo: {}".format(durationInfo))
    
if __name__ == '__main__':
    test_datautil()
    