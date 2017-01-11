import PyConfluence.Confluence
import sys
import PySalesforce.PySalesforce
import html
import json

def getDefaultPageInfo(row, instance_url):
    created_date = row.get('CreatedDate')
    id = row.get('Id')
    created_by = 'GSO Salesforce'
    if (row.get('CreatedBy') is not None):
        created_by = row.get('CreatedBy')['Name']
    page_html = '<p>Created Date: ' + created_date[:10] + '</p>'
    page_html += '<p>Created By: ' + created_by + '</p>'
    url = instance_url + '/' + id
    l = '<a href = "' + url + '">' + url + '</a>'
    page_html += '<p>Link to record' + l + '</p>'
    page_html += '<p>Business Owner: TBD</p>'
    return page_html

def getTableHTML(row):
    created_date = row.get('CreatedDate')
    created_by = 'GSO Salesforce'
    if (row.get('CreatedBy') is not None):
        created_by = row.get('CreatedBy')['Name']
    page_html = '<h3>Change History</h3>'
    page_html += '<table class="confluenceTable"><tbody><tr><th class="confluenceTh">Last Modified By</th><th class="confluenceTh">Last Modified Date</th><th class="confluenceTh">Change Description</th><th class="confluenceTh">Link to JIRA Story</th></tr><tr><td class="confluenceTd">' + created_date[:10] + '</td><td class="confluenceTd">' + created_by + '</td><td class="confluenceTd">Initial creation by Python</td><td class="confluenceTd">TBD</td></tr><tr><td class="confluenceTd"></td><td class="confluenceTd"></td><td class="confluenceTd"></td><td class="confluenceTd"></td></tr></tbody></table>'
    return page_html

def createMetadataTypesPages():
    filename = 'metadata_types.txt'
    metadata_types = []
    with open(filename) as f:
        metadata_types = f.read().splitlines()
    print('Metadata Types count: ' + str(len(metadata_types)))
    last_parent_name = None
    count = 0
    for s in metadata_types:
        print(s)
        if(s.startswith('*')):
            new_str = s.replace('*', '')
            #PyConfluence.Confluence.Helpers.createOrFindPage(new_str, last_parent_name)
        else:
            PyConfluence.Confluence.Helpers.createOrFindPage(s, 'Data Dictionary')
            last_parent_name = s
        count += 1
    print('Created/Checked ' + str(count) + ' pages')
    return count

def createApexClassPages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('ApexClass', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name, ApiVersion FROM ApexClass WHERE Status = \'Active\' ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    #print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        name = row.get('Name')
        api_version = row.get('ApiVersion')
        page_html = getDefaultPageInfo(row, instance_url)
        page_html += '<p>Description: TBD</p>'
        page_html += '<p>API Version: ' + str(api_version) + '</p>'
        page_html += '<p>Link to GIT: TBD</p>'
        page_html += getTableHTML(row)
        PyConfluence.Confluence.Helpers.createOrFindPage(name, 'ApexClass', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' ApexClass pages')

def createApexComponentPages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('ApexComponent', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name, ApiVersion, Markup FROM ApexComponent ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    # print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        name = row.get('Name')
        api_version = row.get('ApiVersion')
        markup = row.get('Markup')
        page_html = getDefaultPageInfo(row, instance_url)
        page_html += '<p>Description: TBD</p>'
        page_html += '<p>API Version: ' + str(api_version) + '</p>'
        page_html += '<p>Markup: ' + markup + '</p>'
        page_html += '<p>Link to GIT: TBD</p>'
        page_html += getTableHTML(row)
        PyConfluence.Confluence.Helpers.createOrFindPage(name, 'ApexComponent', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' ApexComponent pages')

def createVisualforcePages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('ApexPage - Visualforce Page', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name, ApiVersion, Description, Markup FROM ApexPage ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    # print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        name = row.get('Name')
        api_version = row.get('ApiVersion')
        markup = row.get('Markup')
        description = 'TBD'
        if(row.get('Description') is not None):
            description = row.get('Description')
        page_html = getDefaultPageInfo(row, instance_url)
        page_html += '<p>Description: ' + description + '</p>'
        page_html += '<p>API Version: ' + str(api_version) + '</p>'
        page_html += '<p>Markup: ' + markup + '</p>'
        page_html += '<p>Link to GIT: TBD</p>'
        page_html += getTableHTML(row)
        PyConfluence.Confluence.Helpers.createOrFindPage(name, 'ApexPage - Visualforce Page', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' Visualforce pages')

def createApexTriggerPages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('ApexTrigger', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name, ApiVersion, TableEnumOrId FROM ApexTrigger WHERE Status = \'Active\' ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    #print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        name = row.get('Name')
        api_version = row.get('ApiVersion')
        object_name = row.get('TableEnumOrId')
        page_html = getDefaultPageInfo(row, instance_url)
        page_html += '<p>Description: TBD</p>'
        page_html += '<p>API Version: ' + str(api_version) + '</p>'
        page_html += '<p>Object: ' + object_name + '</p>'
        page_html += '<p>Link to GIT: TBD</p>'
        page_html += getTableHTML(row)
        PyConfluence.Confluence.Helpers.createOrFindPage(name, 'ApexTrigger', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' ApexTrigger pages')

def createStaticResourcePages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('StaticResource', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name, Description FROM StaticResource ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    # print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        name = row.get('Name')
        description = 'TBD'
        if (row.get('Description') is not None):
            description = row.get('Description')
        page_html = getDefaultPageInfo(row, instance_url)
        page_html += '<p>Description: ' + description + '</p>'
        page_html += '<p>Link to GIT: TBD</p>'
        page_html += getTableHTML(row)
        PyConfluence.Confluence.Helpers.createOrFindPage(name, 'StaticResource', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' StaticResource pages')

# still needs work
def createCustomLabelPages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('CustomLabel', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name, value, shortDescription FROM CustomLabel ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        page_html = getDefaultPageInfo(row, instance_url)
        name = row.get('Name')
        value = row.get('value')
        shortDescription = 'TBD'
        if (row.get('Description') is not None):
            shortDescription = row.get('Description')
        page_html += '<p>Description: ' + shortDescription + '</p>'
        page_html += '<p>Value: ' + value + '</p>'
        if(count == 0):
            PyConfluence.Confluence.Helpers.createOrFindPage(name, 'ApexTrigger', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' ApexTrigger pages')

def getSalesforceAccessToken():
    print('Getting oauth info')
    auth_res = PySalesforce.PySalesforce.Authentication.getOAuthLogin('chlinenko@expedia.com', 'Seahawks1!IHqM3InSKOV6ODmlQJkxUhI2', '3MVG9zeKbAVObYjOhvCiHETlB.0FKdmahg1CGPsgpklxMAbpZUJtqgAxLKOk.KY49jL1BiQ05iHBhgKGyLkaD', '3173572092401760867', True)
    return auth_res

def main():
    #createMetadataTypesPages()
    auth_res = getSalesforceAccessToken()
    auth_key = auth_res.get('access_token')
    instance_url = auth_res.get('instance_url')
    print('auth_key: ' + auth_key)
    print('instance_url: ' + instance_url)
    # works
    #createApexClassPages(auth_key, instance_url)
    #createApexComponentPages(auth_key, instance_url)
    #createVisualforcePages(auth_key, instance_url)
    #createApexTriggerPages(auth_key, instance_url)
    #createStaticResourcePages(auth_key, instance_url)

    #doesn't work
    #createCustomLabelPages(auth_key, instance_url)
    sys.exit(1)

if __name__ == '__main__':
    main()