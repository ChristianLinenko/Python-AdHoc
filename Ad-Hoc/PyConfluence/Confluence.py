import requests
from urllib.parse import quote
import json

class Webservices:
    user = 'chlinenko'
    pw = 'B0uncyTitties'
    def makePostCall(url, data, headers):
        response = None
        try:
            response = requests.post(url, data=data, headers=headers, auth=(Webservices.user, Webservices.pw))
        except:
            print('Exception caught trying to make POST callout')
            return None
        data = response.json()
        return data

    def makeGetCall(url):
        response = None
        try:
            response = requests.get(url, auth=(Webservices.user, Webservices.pw))
        except:
            print('Exception caught trying to make GET callout')
            return None
        data = response.json()
        return data

class Helpers:
    space = 'LPSSDD'
    def createOrFindPage(page_name, parent_page_name, page_html = None, parent_page_Id = None):
        # first check to see if the page already exists in this space
        # there can't be 2 pages with the same name in the same space
        print('Creating new page ' + page_name + ' under ' + parent_page_name)
        page_id = Helpers.getPageIdByName(page_name)
        if(page_id is None):
            parent_id = parent_page_Id
            if(parent_id is None):
                parent_id = Helpers.getPageIdByName(parent_page_name)
            if(parent_page_name is not None):
                url = 'https://confluence/rest/api/content/'
                if(page_html == None):
                    page_html = '<p>This is a new page I created in Python.</p>'
                data = '{"type":"page","title":"' + page_name + '", "ancestors":[{"id":' + parent_id + '}], "space":{"key":"' + Helpers.space + '"},"body":{"storage":{"value":"' + page_html + '","representation":"storage"}}}'
                headers = {'Content-Type': 'application/json'}
                data = Webservices.makePostCall(url, data, headers)
                if((data is not None) & (data.get('statusCode') == 200) & (data.get('id') is not None)):
                    page_id = data.get('id')
                    print('Page ' + page_name + ' created: ' + page_id)
                elif (data.get('statusCode') is not 200):
                    print('Error creating page: ')
                    print(json.dumps(data, indent=2))
                else:
                    print('id not found')
            else:
                print('Parent page doesnt exist: ' + parent_page_name)
        else:
            print('Page name ' + page_name + ' already exists: ' + page_id)
        return page_id

    def getPageIdByName(page_name):
        print('Searching for page by name: ' + page_name)
        url = 'https://confluence/rest/api/content?title=' + quote(page_name) + '&spaceKey=' + Helpers.space + '&expand=history'
        data = Webservices.makeGetCall(url)
        #print(json.dumps(response.json(), indent=2))
        val = 'Not found'
        if(data is not None):
            for s in data['results']:
                if(s.get('id')):
                    print('Page Found: ' + s.get('id'))
                    return s.get('id')
        print('Page not found: ' + page_name)
        return None