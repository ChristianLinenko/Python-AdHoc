import PyConfluence.Confluence
import sys
import PySalesforce.PySalesforce
import datetime
import json

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
            PyConfluence.Confluence.Helpers.createOrFindPage(new_str, last_parent_name)
        else:
            PyConfluence.Confluence.Helpers.createOrFindPage(s, 'Data Dictionary')
            last_parent_name = s
        count += 1
    print('Created/Checked ' + str(count) + ' pages')
    return count

def createApexClassPages(auth_key, instance_url):
    parent_id = PyConfluence.Confluence.Helpers.createOrFindPage('ApexClass', 'Data Dictionary')
    query_string = 'SELECT Id, Name, CreatedDate, CreatedBy.Name FROM ApexClass WHERE Status = \'Active\' ORDER BY Name'
    query_res = PySalesforce.PySalesforce.Tooling.query(query_string, auth_key, instance_url)
    #print(json.dumps(query_res, indent=2))
    count = 0
    for row in query_res['records']:
        name = row.get('Name')
        created_date = row.get('CreatedDate')
        created_by = 'GSO Salesforce'

        if(row.get('CreatedBy') is not None):
            created_by = row.get('CreatedBy')['Name']
        page_html = '<p>Created Date: ' + created_date[:10] + '</p>'
        page_html += '<p>Created By: ' + created_by + '</p>'
        page_html += '<p>Owner: TBD</p>'
        page_html += '<p>Description: TBD</p>'
        page_html += '<p>Link to GIT: TBD</p>'
        page_html += '<h3 id = "' + name + '-UpdatesTable">Updates Table</h3>'
        if False:
            page_html += '<div class ="table-wrap">';
            page_html += '<table class ="confluenceTable tablesorter tablesorter-default stickyTableHeaders" role="grid" style="padding: 0px;">'
            page_html += '<thead class ="tableFloatingHeaderOriginal">'
            page_html += '<tr role = "row" class ="tablesorter-headerRow">'
            page_html += '< th class ="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Change Description: No sort applied, activate to apply an ascending sort" style="user-select: none;">'
            page_html += '< div class ="tablesorter-header-inner" >Last Modified By< /div></th>'
            page_html += '< th class ="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Change Description: No sort applied, activate to apply an ascending sort" style="user-select: none;">'
            page_html += '< div class ="tablesorter-header-inner" >Last Modified Date< /div></th>'
            page_html += '< th class ="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Change Description: No sort applied, activate to apply an ascending sort" style="user-select: none;">'
            page_html += '< div class ="tablesorter-header-inner" > Change Description < /div></th>'
            page_html += '< th class ="confluenceTh tablesorter-header sortableHeader tablesorter-headerUnSorted" data-column="2" tabindex="0" scope="col" role="columnheader" aria-disabled="false" unselectable="on" aria-sort="none" aria-label="Change Description: No sort applied, activate to apply an ascending sort" style="user-select: none;">'
            page_html += '< div class ="tablesorter-header-inner" > Link to JIRA Story < /div></th>'
            page_html += '</tr>'
            page_html += '</thead>'
            page_html += '<tbody aria - live = "polite" aria - relevant = "all" >'
            page_html += '<tr role = "row" >'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '</tr>'
            page_html += '<tr role = "row" >'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '<td class ="confluenceTd"/>'
            page_html += '</tr>'
            page_html += '</tbody>'
            page_html += '</table>'
            page_html += '</div>'
        if(count == 0):
            PyConfluence.Confluence.Helpers.createOrFindPage(name, 'ApexClass', page_html, parent_id)
        count += 1
    print('Created ' + str(count) + ' pages')

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
    createApexClassPages(auth_key, instance_url)
    sys.exit(1)

if __name__ == '__main__':
    main()