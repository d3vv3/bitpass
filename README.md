# Bitwarden to Pass synchronizer

While Bitwarden is much more friendly on Android and iOS devices, Pass can be so much more convenient in the computer.

This tool was created to have the best of both worlds.

## bitpass-cli

A command-line interface tool to synchronize your Bitwarden pass.

### Usage

```
usage: bitpass-cli [-h] --user USER [--password PASSWORD] --gnupg_home GNUPG_HOME --public_gpg PUBLIC_GPG --pass_storage PASS_STORAGE

optional arguments:

  -h, --help            Show this help message and exit.

  --password PASSWORD   Password for your Bitwarden account. If not  
                        provided, the user will be prompted for the
                        password.

required arguments:

  --user USER           Email to your Bitwarden account.
  
  --gnupg_home GNUPG_HOME
                        Path to your .gnupg.

  --public_gpg PUBLIC_GPG
                        Path to your public gpg key file.

  --pass_storage PASS_STORAGE
                        Path to your Pass .password-storage
```



### Dependencies

1. `bitwarden-cli` is a must. You can install it from [here](https://github.com/bitwarden/cli).

2. `pip3 install -r requirements.txt`

Thats all!


## Setting up in Docker

### Docker

1. Clone the repository by `git clone https://github.com/d3vv3/bitpass.git`
2. Change `Dockerfile` environment variables for your values  
		1. `BW_USER`: your Bitwarden user  
	2. `BW_PASSWORD`: your Bitwarden password  
	3. `PUBLIC_GPG`: your exported public key which you can get by `gpg --armor --export your_email > your_public_key.pub`
3. Run `docker build -t local/bitpass:latest .`
4. Run `docker run -v /home/<your_user>/.gnupg:/gpg_home -v /home/<your_user>/.password-store:/password-store local/bitpass`
5. Create a cron job to execute step 4 whenever you want

### Docker-compose

1. Clone the repository by `git clone https://github.com/d3vv3/bitpass.git`
2. Change `docker-compose.yml` environment variables for your values  
		1.  `BW_USER`: your Bitwarden user  
	2. `BW_PASSWORD`: your Bitwarden password  
	3. `PUBLIC_GPG`: your exported public key which you can get by `gpg --armor --export your_email > your_public_key.pub`
3. Change `docker-compose.yml` volumes for your values  
    1. `/home/<you_user>/.gnupg/:/gpg_home` being the path where your GPG home  
    2. `/home/<your_user>/.password-store/:/password-store` being the path where your pass `password-store` is.
4. Run `docker-compose up`


## Collaborate

Please feel free to open issues or collaborate!


## Known issues

* I am currently using a workaround for a gnupg python issue, as can be seen [here](https://github.com/isislovecruft/python-gnupg/issues/207).
