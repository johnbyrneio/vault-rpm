# RPM Spec for Hashicorp Vault

Build RPMs for Hashicorp Vault

Basically a clone of https://github.com/tomhillable/consul-rpm repurposed for Vault

Tries to follow the [packaging guidelines](https://fedoraproject.org/wiki/Packaging:Guidelines) from Fedora.

* Binary: `/usr/bin/vault`
* Config: `/etc/vault.d/`
* Shared state: `/var/lib/vault/`
* Sysconfig: `/etc/sysconfig/vault`

# Using

Create the RPMs using one of the techniques outlined in the Build section below.

# Build

There are a number of ways to build the `vault` RPMs:
* Manual
* Vagrant
* Docker

Each method ultimately does the same thing - pick the one that is most comfortable for you.

### Version

The version number is hardcoded into the SPEC, however should you so choose, it can be set explicitly by passing an argument to `rpmbuild` directly:

```
$ rpmbuild --define "_version 1.3.2"
```

## Manual

Build the RPM as a non-root user from your home directory:

* Check out this repo. Seriously - check it out. Nice.
    ```
    git clone <this_repo_url>
    ```

* Install `rpmdevtools` and `mock`.
    ```
    sudo yum install rpmdevtools mock
    ```

* Set up your `rpmbuild` directory tree.
    ```
    rpmdev-setuptree
    ```

* Link the spec file and sources.
    ```
    ln -s $HOME/vault-rpm/SPECS/vault.spec $HOME/rpmbuild/SPECS/
    find $HOME/vault-rpm/SOURCES -type f -exec ln -s {} $HOME/rpmbuild/SOURCES/ \;
    ```

* Download remote source files.
    ```
    spectool -g -R rpmbuild/SPECS/vault.spec
    ```

* Spectool may fail if your distribution has an older version of cURL (CentOS
  6.x, for example) - if so, use Wget instead.
    ```
    VER=`grep Version rpmbuild/SPECS/vault.spec | awk '{print $2}'`
    URL='https://dl.bintray.com/mitchellh/vault'
    wget $URL/vault_${VER}_linux_amd64.zip -O $HOME/rpmbuild/SOURCES/vault_${VER}_linux_amd64.zip
    wget $URL/vault_${VER}_web_ui.zip -O $HOME/rpmbuild/SOURCES/vault_${VER}_web_ui.zip
    ```

* Build the RPM.
    ```
    rpmbuild -ba rpmbuild/SPECS/vault.spec
    ```

## Vagrant

If you have Vagrant installed:

* Check out this repo.
    ```
    git clone https://github.com/johnbyrneio/vault-rpm
    ```

* Edit `Vagrantfile` to point to your favourite box (Bento CentOS7 in this example).
    ```
    config.vm.box = "http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_centos-7.0_chef-provisionerless.box"
    ```

* Vagrant up! The RPMs will be copied to working directory after provisioning.
    ```
    vagrant up
    ```

## Docker

If you prefer building it with Docker:

* Build the Docker image. Note that you must amend the `Dockerfile` header if you want a specific OS build (default is `centos7`).
    ```
    docker build -t vault:build .
    ```

* Run the build.
    ```
    docker run -v $HOME/vault-rpms:/RPMS vault:build
    ```

* Retrieve the built RPMs from `$HOME/vault-rpms`.

# Result

One RPMs:
- vault server

# Run

* Install the RPM.
* Put config files in `/etc/vault.d/`.
* Change command line arguments to vault in `/etc/sysconfig/vault`.
* Start the service and tail the logs `systemctl start vault.service` and `journalctl -f`.
  * To enable at reboot `systemctl enable vault.service`.
  * If building for SysV init (pre-systemd) use the appropriate `service` and `chkconfig` commands.

## Config

Config files are loaded in lexicographical order from the `config-dir`. Some
sample configs are provided.

# More info

See the [vault.io](http://www.vaultproject.io) website.
