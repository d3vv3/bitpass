#!/usr/bin/env python3

"""
Import Bitwarden logins to your Linux Pass.

__author__ = devve

"""

# Import to run shell commands and create directories
import os

# Import to read cli arguments
import argparse

# Import to load json formatted
import json

# Import to handle public key and encryption
import gnupg

# Import to check if passwords have been leaked
import pwnedpasswords

# Import for prompt for password
from getpass import getpass

# Import for logging
import logging

# Import for notifications on leaked passwords
import apprise

# PATCH for an unsolved issue in GPG
# (https://github.com/isislovecruft/python-gnupg/issues/207)
import gnupg._parsers
gnupg._parsers.Verify.TRUST_LEVELS["ENCRYPTION_COMPLIANCE_MODE"] = 23


# LOGGING CONFIGURATION


# Configure logging
logging.basicConfig(format='[%(levelname)s] %(message)s')

# Creating a logger object
logger = logging.getLogger()

# Configure the logger threshold
logger.setLevel(logging.WARNING)

# Create the notification object
notif = apprise.Apprise()


# ARGUMENTS


# Create a parser object
parser = argparse.ArgumentParser()

required = parser.add_argument_group('required arguments')

required.add_argument('-user',
                      type=str,
                      help='Email to your Bitwarden account',
                      required=True)
parser.add_argument('--password',
                    type=str,
                    help=("Password for your Bitwarden account. "
                          "If not provided, the user will be prompted for the"
                          " password."),
                    required=False)
required.add_argument('-gnupg_home',
                      type=str,
                      help='Path to your .gnupg', required=True)
required.add_argument('-public_gpg', type=str,
                      help='Path to your public gpg key file',
                      required=True)
required.add_argument('-pass_storage',
                      type=str,
                      help='Path to your Pass .password-storage',
                      required=True)
parser.add_argument('--notification_url',
                    type=str,
                    help=('URL for apprise integration. More at '
                          'https://github.com/caronc/apprise'),
                    required=False)

args = parser.parse_args()


USER = args.user
PASSWORD = args.password
GNUPG_HOME = args.gnupg_home
PUBLIC_GPG = args.public_gpg
PASS_STORAGE = args.pass_storage
NOTIF_URL = args.notification_url


# BITWARDEN FUNCTIONS


# Login the user to the Bitwarden cli tool
def login(user: str, password: str):
    login = os.popen("bw login %s %s" % (user, password))
    output = login.read()
    logger.info("LOGIN SUCCESSFUL")
    return True


# Unlock the vault to get the session key
def unlock_vault(password: str):
    command = os.popen("bw unlock %s --raw" % password)
    logger.info("VAULT UNLOCKED")
    return command.read()


# Get the Bitwarden vault as a json file
def get_vault(password: str):
    session_key = unlock_vault(password)
    command = os.popen("bw sync --session %s" % session_key)
    output = command.read()
    logger.info("VAULT SYNCED")
    command = os.popen(("bw export %s --session %s --output /tmp/bw.json"
                       " --format json --raw") % (password, session_key))
    output = command.read()
    with open(output, "r") as dumped_vault:
        vault = json.load(dumped_vault)
    os.remove(output)
    logger.info("VAULT READ CORRECTLY")
    return vault


# Go through the folders and create them, the do the same for the `Logins`
def vault_iterator(vault: dict):
    folder_mapping = create_folder_structure(vault.get("folders", []))
    items_iterator(vault.get("items", []), folder_mapping)
    return


# PASS FUNCTIONS


# Template for every Pass file
def template(contents: list):
    x = """%s
        URL: %s
        Username: %s
        """ % (contents[1], contents[2], contents[0])
    return x


# Create the folders from Bitwarden in Pass
def create_folder_structure(folders: list):
    mapped = {}
    for folder in folders:

        path = "%s/%s" % (PASS_STORAGE, folder.get("name", ""))
        # Add the folder path to its id
        mapped[folder.get("id", "")] = path
        # Try to create the folder if it does not already exist
        try:
            os.mkdir(path)
        except Exception:
            pass
    # Return a dictionary of folder paths and their ids
    return mapped


# Get the fields out of an item
def get_item_fields(item: dict):
    try:
        name = item.get("name", "blank named")
    except Exception:
        name = "blank named"
    try:
        uri = item.get("login", {}).get("uris")[0].get("uri")
    except Exception:
        uri = ""
    try:
        username = item.get("login", {}).get("username", "")
    except Exception:
        username = ""
    try:
        password = item.get("login", {}).get("password", None)
    except Exception:
        password = None
    if (password is not None and pwnedpasswords.check(str(password)) > 0):
        warn = "The password for %s as %s at %s has been leaked" % (
            name, username, uri)
        try:
            notif.notify(
                body=warn,
                title="BitPass",
            )
        except Exception:
            pass
        logger.warning(warn)
    return [username, password, uri]


# Iterate through the vault and create the pass gpg encrypted files
def items_iterator(items: list, folder_paths: dict):
    # Iterate through the items in the vault
    for item in items:
        # Make sure the item we add is `Login` type
        if item.get("type", 0) != 1:
            continue
        # Get the path where the file goes
        folder_path = folder_paths.get(item.get("folderId"), PASS_STORAGE)
        file_path = folder_path + "/%s.gpg" % item.get("name")
        # If folder does not exist, create it
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        # If it already exists, delete it to update it
        if os.path.isfile(file_path):
            os.remove(file_path)
        # Create the content of the Pass file by filling the template
        file_content = template(get_item_fields(item))
        # Encrypt that content into a new file inside password-store
        create_encrypted_file(file_path, file_content)
    return


# GPG FUNCTIONS


# Create a gpg encrypted file with the given content
def create_encrypted_file(path: str, content: str):
    gpg = gnupg.GPG(homedir=GNUPG_HOME)
    byte_content = content.encode('utf-8')
    imported_key = import_gpg_key(PUBLIC_GPG)
    gpg.encrypt(byte_content, imported_key, encrypt=True, output=path)


# Import the user's public gpg key from its gpg_home directory
def import_gpg_key(path: str):
    # Stablish the gpg home directory
    gpg = gnupg.GPG(homedir=GNUPG_HOME)
    # Open the key and import it
    key_data = open(path).read()
    import_result = gpg.import_keys(key_data)
    # Return  the fingerprint as string
    return import_result.results[0].get("fingerprint")


if __name__ == "__main__":
    if PASSWORD is None or PASSWORD == "":
        PASSWORD = getpass("Bitwarden password [hidden]:")
    notif.add(NOTIF_URL)
    login(USER, PASSWORD)
    vault_iterator(get_vault(PASSWORD))
