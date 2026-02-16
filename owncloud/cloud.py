#!/usr/bin/python3

from lxml import etree
from requests import request
from requests.utils import quote, unquote
from pathlib import Path
import json


def get_tag_info(url, user, passwd):
    r = request(
        "PROPFIND", url, auth=(user, passwd), data=open("./propfind-tagid.xml", "rb")
    )
    xml = etree.fromstring(r.content)
    nsmap = xml.nsmap
    response = xml.findall("d:response", namespaces=nsmap)
    # name:id
    tag_dict = dict()
    href = list()
    for i in response:
        i_id = i.find("*//oc:id", namespaces=nsmap)
        i_name = i.find("*//oc:display-name", namespaces=nsmap)
        tag_dict[i_name.text] = i_id.text
        href.append(i.find("d:href", namespaces=nsmap).text)
    return tag_dict, href


def get_tag_id(fileid, url, user, passwd):
    url = url + fileid
    _, href = get_tag_info(url, user, passwd)


def create_tag(tag_name, url, user, passwd):
    d = {"name": tag_name, "userVisible": True, "userAssignable": True}
    headers = {"content-type": "application/json"}
    r = request("POST", url, auth=(user, passwd), data=json.dumps(d), headers=headers)


def delete_tag(tag_id, url, auth):
    r = request("DELETE", url + "/{}".format(tag_id), auth=auth)


def get_fileid(path, url, user, passwd):
    r = request(
        "PROPFIND",
        url=url + "/{}/{}".format(user, quote(path)),
        auth=(user, passwd),
        data=open("./propfind-fileid.xml", "rb"),
        headers={"Depth": "1"},
    )
    xml = etree.fromstring(r.text)
    nsmap = xml.nsmap
    response = xml.findall("d:response", namespaces=nsmap)
    # filename:id
    file_dict = dict()
    for i in response:
        fullname = i.find("d:href", namespaces=nsmap).text
        filename = Path(fullname).name.__str__()
        # fileid = i.find('d:propstat/d:prop/oc:fileid', namespaces=nsmap)
        fileid = i.find("*//oc:fileid", namespaces=nsmap).text
        file_dict[unquote(filename)] = fileid
    return file_dict


def get_table(table_file):
    table = list()
    with open(table_file, "r") as raw:
        raw.readline()
        for line in raw:
            line = line.split(",")
            index = int(line[0])
            filename = "{}_{}".format(*line[1:3])
            leixing = line[3]
            leixing = "1-{}".format(leixing)
            banzou = line[4]
            banzou = "2-{}伴奏".format(banzou)
            yuyan = line[5]
            if "&" in yuyan:
                yuyan = yuyan.split("&")
                yuyan = ["3-{}".format(i) for i in yuyan]
            else:
                yuyan = ["3-{}".format(yuyan)]
            lingchang_raw = line[6]
            lingchang = list()
            for i in lingchang_raw:
                if i == "无":
                    lingchang.append("4-无领唱")
                else:
                    lingchang.append("4-{}. solo".format(i))
            table.append([index, filename, leixing, banzou, *yuyan, *lingchang])
    return table


def assign_tag(fileid, tagid, url, user, passwd):
    r = request("PUT", "{}/{}/{}".format(url, fileid, tagid), auth=(user, passwd))
    print(fileid, tagid, r.status_code)


def main():
    tag_url = "https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags"
    list_url = "https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/files"
    file_tag_url = "https://phdchorus.ucas.ac.cn/owncloud/remote.php/dav/systemtags-relations/files/"
    folder = "01___薄荷曲库___01"
    with open("key", "r") as _:
        raw = _.read().strip().split(" ")
        user, passwd = raw
    tag_dict, _ = get_tag_info(tag_url, user, passwd)
    filename_id_dict = get_fileid(folder, list_url, user, passwd)
    # get_tag_id(fileid, file_tag_url, user, passwd)
    table = get_table("./table.csv")
    todo = list()
    miss = list()
    for i in table:
        tag_id_to = list()
        for j in i[2:]:
            tag_id_to.append(tag_dict[j])
        try:
            # index, filename, fileid, tagids
            todo.append([i[0], i[1], filename_id_dict[i[1]], i[2:], tag_id_to])
        except KeyError:
            todo.append([i[0], i[1]])
            miss.append([i[0], i[1]])

    todo_me = todo
    for record in todo_me:
        print(record)
        fileid, tagids = record[2], record[-1]
        for tagid in tagids:
            assign_tag(fileid, tagid, file_tag_url, user, passwd)
    print(*miss)

    # tag_id = input('Enter tag id to list file:')
    # list_file_by_tag(tag_id, list_url, auth)
    # tag_name = input('Enter new tag name:')
    # create_tag(tag_url, auth, tag_name)
    # tag_name = input('Enter tag name you want to delete:')
    # tag_id = tag_dict[tag_name]
    # delete_tag(tag_url, auth, tag_id)


if __name__ == "__main__":
    main()
