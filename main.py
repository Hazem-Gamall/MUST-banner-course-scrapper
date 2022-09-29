from time import sleep
import requests


def get_session():
    session = requests.Session()
    session.get('https://register.must.edu.eg/StudentRegistrationSsb/ssb/registration')
    return session

def enable_search(session):
    """My current theory is that i need to do this request so that
    the server assings something to my session in its database that allows me
    to perform the search request"""

    params = {
        'mode': 'search',
    }

    data = {
        'term': '202310',
        'studyPath': '',
        'studyPathText': '',
        'startDatepicker': '',
        'endDatepicker': '',
        # 'uniqueSessionId': 'wz0061664464778935',
    }

    session.post(
        'https://register.must.edu.eg/StudentRegistrationSsb/ssb/term/search',
        params=params,
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
        data=data
        )


def search(subject, course_number, crn_to_monitor):
    session = get_session()
    enable_search(session)
    
    course_search_params = {
        'txt_subject':subject,
        'txt_courseNumber':course_number,
        'txt_term':'202310',
        'startDatepicker':'',
        'endDatepicker':'',
        'pageOffset':0,
        'sortColumn':'subjectDescription',
        'sortDirection':'asc'
    }
    resp = session.get('https://register.must.edu.eg/StudentRegistrationSsb/ssb/searchResults/searchResults',params=course_search_params)
    print(resp)
    if resp.json()['data']:
        for course_entry in resp.json()['data']:
            crn = course_entry['meetingsFaculty'][0]['courseReferenceNumber']
            seats_available = course_entry['seatsAvailable']
            # print(f"Title: {course_entry['courseTitle']}")
            # print(f"Type: {course_entry['scheduleTypeDescription']}")
            # print(f"CRN: {crn}")
            # print(f"seatsAvailable: {seats_available}")
            # print('\n')
            if crn == crn_to_monitor and seats_available > 0:
                print("SEATS AVAILABLE MY NIGGA!!!\n\n")
    else:
        raise Exception('Please make sure that the course title you entered is correct.')

if __name__ == '__main__':
    print("""Enter the course name without spaces""")
    course_name = ''.join(input('course subject:').upper().split())
    subject = course_name[:4]
    course_number = course_name[4:]
    crn_to_monitor = input("Enter the CRN you would like to monitor:")
    print(subject, course_number, crn_to_monitor)
    while True:
        try:
            search(subject, course_number, crn_to_monitor)
        except Exception as e:
            print('Error', e)
        sleep(60)