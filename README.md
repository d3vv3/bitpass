# Bitwarden to Pass syncronizer

While Bitwarden is much more friendly on Android and iOS devices, Pass can be so much more
convenient in the computer.

This tool was created to have the best of both worlds.


## Setting up

### Docker

1. Clone the repository by `git clone <this_repo>`
2. Change `Dockerfile` enviroment variables for your values  
		i.   `BW_USER`: your Bitwarden user  
		ii.  `BW_PASSWORD`: your Bitwarden password  
		iii. `PUBLIC_GPG`: your exported public key which you can get by `gpg --armor --export your_email > your_public_key.pub`
3. Run `docker build -t local/bitpass:latest .`
4. Run `docker run -v /home/<your_user>/.gnupg:/gpg_home -v /home/<your_user>/.password-store:/password-store local/bitpass`
5. Create a cron job to execute step 4 whenever you want

### Docker-compose

1. Clone the repository by `git clone <this_repo>`
2. Change `docker-compose.yml` enviroment variables for your values  
		i. 	 `BW_USER`: your Bitwarden user  
		ii.  `BW_PASSWORD`: your Bitwarden password  
		iii. `PUBLIC_GPG`: your exported public key which you can get by `gpg --armor --export your_emai    l > your_public_key.pub`
3. Change `docker-compose.yml` volumes for your values  
		i.  `/home/<you_user>/.gnupg/:/gpg_home` being the path where your GPG home is  
		ii. `/home/<your_user>/.password-store/:/password-store` being the path where your pass `password-store` is  
4. Run `docker-compose up`


## Colaborate

Please feel free to open issues or colaborate!


## Known issues

* I am currently using a workaround for a gnupg python issue, as can be seen [here](https://github.com/isislovecruft/python-gnupg/issues/207)
