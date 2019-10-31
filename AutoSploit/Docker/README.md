# Docker deployment instructions

## tl;dr

Using [docker-compose](https://docs.docker.com/compose/install/):

```bash
git clone https://github.com/NullArray/AutoSploit.git
cd Autosploit/Docker
docker-compose run --rm autosploit
```

Using just Docker:

```bash
git clone https://github.com/NullArray/AutoSploit.git
cd Autosploit/Docker
# If you wish to edit default postgres service details, edit database.yml. Should work out of the box
# nano database.yml
docker network create -d bridge haknet
docker run --network haknet --name msfdb -e POSTGRES_PASSWORD=s3cr3t -d postgres
docker build -t autosploit .
docker run -it --network haknet -p 80:80 -p 443:443 -p 4444:4444 autosploit
```

## Abstract

- Launching `Autosploit` as a Docker container makes it very easy to use the tool in a hosted cloud environment (AWS, Azure, ...)
- Separate `postgres` database into individual service for data persistence and potential async updating of the database
- Create a small bridge network `haknet` so the service discovery is automatic
- Launch `postgres` and `Autosploit` container, both linked by `haknet`
- Autosploit will automatically launch preconfigured `msfconsole` to the external `postgres` container through `haknet` transparent network
- Total image size of Kali + Metasploit + Autosploit : 1.75GB

## Deploy

### Step 1 - Create bridge network

This will enable the Metasploit Framework to talk to the `postgres` database using its hostname, making it abstract.

A Tor Socks Proxy can also be added to perform transparent proxy when launching exploits (not for reverse shells though, obviously).

```bash
docker network create -d bridge haknet
```

### Step 2 - Launch services

All automagically linked

#### Step 2.1 - Launch postgres

Launch a vanilla `postgres` service, linked to `haknet`

```bash
docker run --network haknet --name msfdb -e POSTGRES_PASSWORD=s3cr3t -d postgres
```

#### Step 2.2 - Launch Autosploit

Launch `Autosploit`.

This Dockerfile will copy the default database config to `~/.msf4/database.yml`. You can edit the configuration file `database.yml` to your liking before building.

Please be aware that the first build will take some time (~10mn)

Building will be faster if done on a hosted server as it benefits from the -grade bandwidth

```bash
git clone https://github.com/NullArray/AutoSploit.git
cd Autosploit/Docker
nano database.yml # Exemple configuration should work fine
docker build -t autosploit .
docker run -it --network haknet -p 80:80 -p 443:443 -p 4444:4444 autosploit
```
