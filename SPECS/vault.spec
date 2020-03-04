%if 0%{?_version:1}
%define         _verstr      %{_version}
%else
%define         _verstr      1.3.2
%endif

Name:           vault
Version:        %{_verstr}
Release:        1%{?dist}
Summary:        Vault is a tool for secrets management, encryption as a service, and privileged access management.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            https://www.vaultproject.io/
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
Source1:        %{name}.sysconfig
Source2:        %{name}.service
Source3:        %{name}.init
Source4:        %{name}.hcl
Source5:        %{name}.logrotate
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
BuildRequires:  systemd-units
Requires:       systemd
%else
Requires:       logrotate
%endif
Requires(pre): shadow-utils


%description
Vault is a tool for secrets management, encryption as a service, and privileged access management.

The key features of Vault are:

  - Secure Secret Storage: Arbitrary key/value secrets can be stored in Vault. Vault encrypts these secrets prior to writing them to persistent storage, so gaining access to the raw storage isn't enough to access your secrets. Vault can write to disk, Consul, and more.
  - Dynamic Secrets: Vault can generate secrets on-demand for some systems, such as AWS or SQL databases. For example, when an application needs to access an S3 bucket, it asks Vault for credentials, and Vault will generate an AWS keypair with valid permissions on demand. After creating these dynamic secrets, Vault will also automatically revoke them after the lease is up.
  - Data Encryption: Vault can encrypt and decrypt data without storing it. This allows security teams to define encryption parameters and developers to store encrypted data in a location such as SQL without having to design their own encryption methods.
  - Leasing and Renewal: All secrets in Vault have a lease associated with it. At the end of the lease, Vault will automatically revoke that secret. Clients are able to renew leases via built-in renew APIs.
  - Revocation: Vault has built-in support for secret revocation. Vault can revoke not only single secrets, but a tree of secrets, for example all secrets read by a specific user, or all secrets of a particular type. Revocation assists in key rolling as well as locking down systems in the case of an intrusion.


%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_bindir}
cp vault %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}.d
cp %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}.d/vault.hcl-dist
mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
mkdir -p %{buildroot}/%{_unitdir}
cp %{SOURCE2} %{buildroot}/%{_unitdir}/
%else
mkdir -p %{buildroot}/%{_initrddir}
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
cp %{SOURCE3} %{buildroot}/%{_initrddir}/vault
cp %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
%endif

%pre
getent group vault >/dev/null || groupadd -r vault
getent passwd vault >/dev/null || \
    useradd -r -g vault -d /var/lib/vault -s /sbin/nologin \
    -c "vault.io user" vault
exit 0

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%else
%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir %attr(750, root, vault) %{_sysconfdir}/%{name}.d
%attr(640, root, vault) %{_sysconfdir}/%{name}.d/vault.hcl-dist
%dir %attr(750, vault, vault) %{_sharedstatedir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?fedora} >= 14 || 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%endif
%attr(755, root, root) %{_bindir}/vault



%doc


%changelog
* Wed Mar 04 2020 John Byrne <john@johnbyrne.io> - 1.3.2-1
- Initial release using Vault version 1.3.2