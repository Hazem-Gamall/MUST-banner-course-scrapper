from time import sleep
import requests
import aiohttp
import asyncio


async def init_session(session):
    await session.get('https://register.must.edu.eg/StudentRegistrationSsb/ssb/registration')
    return session

async def enable_search(session):
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

    await session.post(
        'https://register.must.edu.eg/StudentRegistrationSsb/ssb/term/search',
        params=params,
        headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
        data=data
        )


async def search(subject, course_number, crns_to_monitor, session):
    
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
    async with session.get('https://register.must.edu.eg/StudentRegistrationSsb/ssb/searchResults/searchResults',params=course_search_params) as response:
        json_response = await response.json()
        data = json_response['data']
        if data:
            for course_entry in data:
                course_title = course_entry['courseTitle']
                crn = course_entry['meetingsFaculty'][0]['courseReferenceNumber']
                seats_available = course_entry['seatsAvailable']

                if crn in crns_to_monitor and seats_available > 0:
                    print(f"{course_title}: {seats_available} SEATS AVAILABLE FOR {crn}\n\n")
        else:
            raise Exception('Please make sure that the course title you entered is correct.')

async def main():
    num_of_courses = int(input('How many courses do you want to track? '))
    courses = []
    for _ in range(num_of_courses):
        print("""Enter the course name without spaces""")
        course_name = ''.join(input('course subject:').upper().split())    
        course = {
            'subject': course_name[:4],
            'course_number':course_name[4:],
            'crns_to_monitor': input("Enter the CRNs you would like to monitor comma-seperated:").strip().split(',')
        }
         
        courses.append(course)
    async with aiohttp.ClientSession() as session:
        await init_session(session)
        await enable_search(session)
        
        
        try:
            while True:
                tasks = [search(session=session, **course) for course in courses ]
                await asyncio.gather(*tasks)
                sleep(2)
        except Exception as e:
            print('Error', e)

if __name__ == '__main__':
    asyncio.run(main())