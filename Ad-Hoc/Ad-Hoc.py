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
    page_html += '<p>Link to record: ' + l + '</p>'
    page_html += '<p>Business Owner: TBD</p>'
    return page_html

def getTableHTML(row):
    page_html = '<h3>Change History</h3>'
    if(row is None):
        page_html += '<table class="confluenceTable"><tbody><tr><th class="confluenceTh">Last Modified By</th><th class="confluenceTh">Last Modified Date</th><th class="confluenceTh">Change Description</th><th class="confluenceTh">Link to JIRA Story</th></tr><tr><td class="confluenceTd">TBD</td><td class="confluenceTd">TBD</td><td class="confluenceTd">Initial creation by Python</td><td class="confluenceTd">TBD</td></tr><tr><td class="confluenceTd"></td><td class="confluenceTd"></td><td class="confluenceTd"></td><td class="confluenceTd"></td></tr></tbody></table>'
    else:
        created_date = row.get('CreatedDate')
        created_by = 'GSO Salesforce'
        if (row.get('CreatedBy') is not None):
            created_by = row.get('CreatedBy')['Name']
        page_html += '<table class="confluenceTable"><tbody><tr><th class="confluenceTh">Last Modified By</th><th class="confluenceTh">Last Modified Date</th><th class="confluenceTh">Change Description</th><th class="confluenceTh">Link to JIRA Story</th></tr><tr><td class="confluenceTd">' + created_date[
                                                                                                                                                                                                                                                                                                    :10] + '</td><td class="confluenceTd">' + created_by + '</td><td class="confluenceTd">Initial creation by Python</td><td class="confluenceTd">TBD</td></tr><tr><td class="confluenceTd"></td><td class="confluenceTd"></td><td class="confluenceTd"></td><td class="confluenceTd"></td></tr></tbody></table>'
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
        #print(s)
        page_html = '<p><ac:structured-macro ac:name="children"/></p>'
        if(s.startswith('*')):
            new_str = s.replace('*', '')
            PyConfluence.Confluence.Helpers.createOrFindPage(new_str, last_parent_name, page_html)
            # need to add this tag to the HTML - '<p><ac:structured-macro ac:name="children"/></p>'
        else:
            PyConfluence.Confluence.Helpers.createOrFindPage(s, 'Data Dictionary', page_html)
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
        description = 'TBD'
        if(row.get('Description') is not None):
            description = row.get('Description')
        page_html = getDefaultPageInfo(row, instance_url)
        page_html += '<p>Description: ' + description + '</p>'
        page_html += '<p>API Version: ' + str(api_version) + '</p>'
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

def createObjPage(auth_key, instance_url, sObjectName, parent_name, parent_id):
    res = PySalesforce.PySalesforce.Standard.getSobjectMetadata(auth_key, instance_url, sObjectName)
    #print(json.dumps(res.json(), indent=2))
    name = res.get('name')
    label = res.get('label')
    key_Prefix = res.get('keyPrefix')
    page_html = '<p>Label: ' + label + '</p>'
    page_html += '<p>Name: ' + name + '</p>'
    page_html += '<p>Prefix: ' + str(key_Prefix) + '</p>'
    page_html += '<p>Business Owner: TBD</p>'
    page_html += '<p>Link to Object: TBD</p>'
    page_html += '<p>Created By: TBD</p>'
    page_html += '<p>Created Date: TBD</p>'
    page_html += '<h3>Metadata Types</h3>'
    page_html += '<p><ac:structured-macro ac:name="children"/></p>'
    new_page_id = PyConfluence.Confluence.Helpers.createOrFindPage(name, parent_name, page_html, parent_id)
    if(new_page_id is not None):
        # create child pages
        page_html = '<h3>Fields</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        fields_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('Fields - ' + label, label, page_html, new_page_id)
        page_html = '<h3>Record Types</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        record_types_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('Record Types - ' + label, label, page_html, new_page_id)
        page_html = '<h3>Validation Rules</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        validation_rules_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('Validation Rules - ' + label, label, page_html, new_page_id)
        page_html = '<h3>Workflow Rules</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        workflow_rules_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('Workflow Rules - ' + label, label, page_html, new_page_id)
        page_html = '<h3>Page Layouts</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        page_layouts_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('Page Layouts - ' + label, label, page_html, new_page_id)
        page_html = '<h3>List Views</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        list_view_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('List Views - ' + label, label, page_html, new_page_id)
        page_html = '<h3>Fields Sets</h3>'
        page_html += '<p><ac:structured-macro ac:name="children"/></p>'
        field_sets_page_id = PyConfluence.Confluence.Helpers.createOrFindPage('Field Sets - ' + label, label, page_html, new_page_id)
        count = 0
        for row in res['fields']:
            field_name = row.get('name')
            field_label = row.get('label')
            field_type = row.get('type')
            field_custom = row.get('custom')
            field_page_html = '<p>Label: ' + field_label + '</p>'
            field_page_html += '<p>Name: ' + field_name + '</p>'
            field_page_html += '<p>Field Type: ' + field_type + '</p>'
            field_page_html += '<p>Custom Field: ' + str(field_custom) + '</p>'
            field_page_html += '<p>Business Owner: TBD</p>'
            field_page_html += '<p>Link to Field: TBD</p>'
            field_page_html += getTableHTML(None)
            PyConfluence.Confluence.Helpers.createOrFindPage(name + '.' + field_name, label, field_page_html, fields_page_id)
            count += 1
        count = 0
        for row in res['recordTypeInfos']:
            field_name = row.get('name')
            if(field_name != 'master'):
                rt_available = row.get('available')
                rt_id = row.get('recordTypeId')
                url = instance_url + '/' + rt_id
                l = '<a href = "' + url + '">' + url + '</a>'
                field_page_html = '<p>Name: ' + field_name + '</p>'
                field_page_html += '<p>Available: ' + str(rt_available) + '</p>'
                field_page_html += '<p>Business Owner: TBD</p>'
                field_page_html += '<p>Link to record: ' + l + '</p>'
                field_page_html += getTableHTML(None)
                PyConfluence.Confluence.Helpers.createOrFindPage(name + '.' + field_name, label, field_page_html, record_types_page_id)
            count += 1

def createCustomObjectPages(auth_key, instance_url):
    standard_obj_pagent_id = PyConfluence.Confluence.Helpers.createOrFindPage('Standard', 'Objects')
    custom_obj_pagent_id = PyConfluence.Confluence.Helpers.createOrFindPage('Custom', 'Objects')
    custom_setting_pagent_id = PyConfluence.Confluence.Helpers.createOrFindPage('CustomSettings', 'Data Dictionary')
    res = PySalesforce.PySalesforce.Standard.getSobjects(auth_key, instance_url)
    #print(json.dumps(res.json(), indent=2))
    standard_object_names = []
    custom_object_names =[]
    custom_settings_names = []
    count = 0;
    for c in res.json()['sobjects']:
        if (c.get('customSetting')):
            custom_settings_names.append(c.get('name'))
            createObjPage(auth_key, instance_url, c.get('name'), 'CustomSettings', custom_setting_pagent_id)
        elif (c.get('custom')):
            custom_object_names.append(c.get('name'))
            createObjPage(auth_key, instance_url, c.get('name'), 'Custom', custom_obj_pagent_id)
        else:
            standard_object_names.append(c.get('name'))
            createObjPage(auth_key, instance_url, c.get('name'), 'Standard', standard_obj_pagent_id)
        count += 1
    print('Number of custom objects found: ' + str(len(custom_object_names)))
    print('Number of standard objects found: ' + str(len(standard_object_names)))
    print('Number of custom settings found: ' + str(len(custom_settings_names)))

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

def createPages():
    auth_res = getSalesforceAccessToken()
    auth_key = auth_res.get('access_token')
    instance_url = auth_res.get('instance_url')
    #print('auth_key: ' + auth_key)
    #print('instance_url: ' + instance_url)
    #createMetadataTypesPages()
    #createApexClassPages(auth_key, instance_url)
    #createApexComponentPages(auth_key, instance_url)
    #createVisualforcePages(auth_key, instance_url)
    #createApexTriggerPages(auth_key, instance_url)
    #createStaticResourcePages(auth_key, instance_url)
    createCustomObjectPages(auth_key, instance_url)

    # TODO
    # createCustomLabelPages(auth_key, instance_url)
    # for objects
    #   validation rules
    #   workflow rules
    #   page layouts
    #   list views
    #   field sets
    # flows and process builders
    # groups (queues and public groups)
    # permission sets
    # profiles
    # roles

def main():
    createPages()
    sys.exit(1)

if __name__ == '__main__':
    main()