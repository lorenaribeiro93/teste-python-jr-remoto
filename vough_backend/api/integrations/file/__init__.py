import json
import shutil
import tempfile


def file_exists(file):
    try:
        open_file = open(file, 'rt')
        open_file.close()
    except FileNotFoundError:
        return False
    else:
        return True


def create_file(file):
    open_file = open(file, 'wt+')
    orgs = list()
    json.dump(orgs, open_file)
    open_file.close()


def read_file(file):
    print(file)
    with open('api/integrations/file/orgs.json', 'r', encoding='utf8') as f:
        return json.load(f)


def store_org(file, org):
    with open(file, 'r', encoding='utf-8') as file_json,\
            tempfile.NamedTemporaryFile('w', delete=False) as out:
        
        orgs = json.load(file_json)
        org_logins = []
        for register in orgs:
            org_logins.append(register['login'])

        if orgs == [] or org['login'] not in org_logins:
            orgs.append(org)

        ordered_org = sorted(orgs, key=lambda row: row['score'], reverse=1)

        json.dump(ordered_org, out, ensure_ascii=False, indent=4,
                  separators=(',', ':'))

    shutil.move(out.name, file)
    return read_file('orgs.json')


def delete_org(org):
    file = 'api/integrations/file/orgs.json'
    orgs = None
    with open(file, 'r', encoding='utf-8') as file_json,\
            tempfile.NamedTemporaryFile('w', delete=False) as out:

        orgs = json.load(file_json)
        org_logins = []
        for register in orgs:
            org_logins.append(register['login'])
        if org in org_logins:
            for item in orgs:
                if item['login'] == org:
                    orgs.remove(item)
        json.dump(orgs, out, ensure_ascii=False, indent=4,
                  separators=(',', ':'))

    shutil.move(out.name, file)
    return read_file(file)