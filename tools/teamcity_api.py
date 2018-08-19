import re
import sys
import base64
import httplib
from http import Http
#from bs4 import BeautifulSoup
from xml.dom.minidom import parseString
import time

http_conn = Http("http://ce.paddlepaddle.org:8080")

max_retry = 3
build_dict = {}


def show_build(build_id):
    """GET details build info of the build id"""

    auth = base64.b64encode('guest' + ':' + 'guest')
    headers = {"Authorization": "Basic " + auth}
    url = "/app/rest/builds/%s" % build_id
    for cnt in range(max_retry):
        try:
            status, resp, _ = http_conn.access("GET", url, headers=headers)
            if status == 200:
                break
        except Exception as e:
            if cnt == max_retry - 1:
                raise Exception("list builds fail, error: %s " % e)
            else:
                time.sleep(1)

    b = parseString(resp)
    builds = b.getElementsByTagName('build')
    for build in builds:
        status = build.getElementsByTagName('statusText')[0]
        date = build.getElementsByTagName('startDate')[0]
        revisions = build.getElementsByTagName('revisions')
        res = ''
        for revision in revisions:
            mm = revision.getElementsByTagName('revision')[0]
            res = mm.getAttribute('version')

        build_dict[res] = {'id':build.getAttribute('id'),\
             'weburl':build.getAttribute('webUrl'),\
             'status':status.childNodes[0].data,\
             'date':date.childNodes[0].data,\
             'version': res}


def list_build():
    """GET all abstract build info"""
    build_list = []
    auth = base64.b64encode('guest' + ':' + 'guest')
    headers = {"Authorization": "Basic " + auth}
    #assume no more then 60 builds one week. 
    url = "/app/rest/builds?buildType=PaddleCe_CEBuild&count=60"
    #list build should ensure suc.
    for cnt in range(2 * max_retry):
        try:
            status, resp, _ = http_conn.access("GET", url, headers=headers)
            if status == 200:
                break
        except Exception as e:
            if cnt == max_retry - 1:
                raise Exception("show builds fail, error: %s " % e)
            else:
                time.sleep(1)

    b = parseString(resp)
    builds = b.getElementsByTagName('build')
    for build in builds:
        build_list.append(build.getAttribute('id'))
    return (build_list)


if __name__ == '__main__':
    builds = list_build()
    print len(builds)

    for build in builds:
        try:
            show_build(build)
            time.sleep(0.5)
        except Exception as e:
            print("build failed, %s" % e)
            sys.exit(1)
    print(build_dict)

    import json
    with open('teamcity.json', 'w') as json_file:
        json_file.write(json.dumps(build_dict))
