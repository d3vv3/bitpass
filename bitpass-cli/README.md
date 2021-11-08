# bitpass-cli

A command-line interface tool to syncronize yout Bitwarden pass.

## Usage

```
usage: main.py [-h] -user USER [--password PASSWORD] -gnupg_home GNUPG_HOME -public_gpg PUBLIC_GPG -pass_storage PASS_STORAGE [--notification_url NOTIFICATION_URL]

optional arguments:

  -h, --help            show this help message and exit

  --password PASSWORD   Password for your Bitwarden account. If not  
                        provided, the user will be prompted for the password.

  --notification_url NOTIFICATION_URL
                        URL for apprise integration. More at  
                        https://github.com/caronc/apprise

  --server SERVER       URL to a selfhosted instance of Bitwarden, for example
                        Vaultwarden.

required arguments:

  -user USER            Email to your Bitwarden account

  -gnupg_home GNUPG_HOME
                        Path to your .gnupg

  -public_gpg PUBLIC_GPG
                        Path to your public gpg key file

  -pass_storage PASS_STORAGE
                        Path to your Pass .password-storage
```



## Dependencies

1.  `bitwarden-cli` is a must. You can install it from [here](https://github.com/bitwarden/cli).
2.  `pip3 install -r requirements.txt`

That's all!
