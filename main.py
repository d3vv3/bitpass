"""
Import BitWarden logins to your Linux Pass.

__author__ = devve

"""

# Import to access enviroment variables, run shell commands and create directories
import os

# Import to load json formatted
import json

# Import to handle public key and encryption
import gnupg


# PATCH for an unsolved issue in GPG (https://github.com/isislovecruft/python-gnupg/issues/207)
import gnupg._parsers
gnupg._parsers.Verify.TRUST_LEVELS["ENCRYPTION_COMPLIANCE_MODE"] = 23


# ENVIROMENT VARIABLES


USER = os.environ.get("BW_USER", "")
PASSWORD = os.environ.get("BW_PASSWORD", "")
PUBLIC_GPG = "/gpg_home/" + os.environ.get("PUBLIC_GPG", "")


# BITWARDEN FUNCTIONS


def login(user: str, password: str):
    login = os.popen("bw login %s %s" % (user, password))
    output = login.read()
    return True


def unlock_vault(password: str):
    command = os.popen("bw unlock %s --raw" % password)
    return command.read()


def get_vault(password: str):
    session_key = unlock_vault(password)
    command = os.popen("bw export %s --session %s --output bw.json --format json --raw" % (password, session_key))
    output = command.read()
    with open(output, "r") as dumped_vault:
        vault = json.load(dumped_vault)
    os.remove(output)
    return vault


def vault_iterator(vault: dict):
    folder_mapping = create_folder_structure(vault.get("folders", []))
    items_iterator(vault.get("items", []), folder_mapping)
    return


# PASS FUNCTIONS


def template(username: str, password: str, url: str):
    x = """%s \n
        URL: %s \n
        Username: %s \n
        """ % (password, url, username)
    return x


def create_folder_structure(folders: list):    
    mapped = {}    
    for folder in folders:    
        path = "/password-store/%s" % folder.get("name", "")    
        mapped[folder.get("id", "")] = path    
        try:    
            os.mkdir(path)    
        except Exception:    
            pass    
    return mapped


def items_iterator(items: list, folder_paths: dict):
    gpg = gnupg.GPG(homedir='/gpg_home')
    for item in items:
        if item.get("type", 0) != 1:
            continue
        folder_path = folder_paths.get(item.get("folderId"), "/password-store")
        file_path = folder_path + "/%s" % item.get("name") + ".gpg"
        if os.path.isfile(file_path):
            os.remove(file_path)
        file_path_temp = file_path[:-4]
        try:
            uri = item.get("login", {}).get("uris")[0].get("uri")
            username = item.get("login", {}).get("username", "")
        except Exception:
            uri = ""
            username = ""
        file_content = template(username,
                                item.get("login", {}).get("password", ""),
                                uri)
        byte_content = file_content.encode('utf-8')
        imported_key = import_gpg_key(PUBLIC_GPG)
        gpg.encrypt(byte_content, imported_key, encrypt=True, output=file_path)
    return



# GPG FUNCTIONS


def import_gpg_key(path: str):
    gpg = gnupg.GPG(homedir='/gpg_home')
    key_data = open(path).read()
    import_result = gpg.import_keys(key_data)
    return import_result.results[0].get("fingerprint")


if __name__ == "__main__":
    login(USER, PASSWORD)
    vault_iterator(get_vault(PASSWORD))
