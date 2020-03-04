ui = true
listener "tcp" {
    address = "[::]:8200"
    cluster_address = "[::]:8201"
    tls_disable = 1
    # tls_cert_file = "/etc/certs/vault.crt"
    # tls_key_file  = "/etc/certs/vault.key"
    
}

# Comment out if you enable HA Vault server below
storage "file" {
    path = "/vault/data"
}

# Uncomment for a HA Vault server. Requires Consul.
# storage "consul" {
#     address = "HOST_IP:8500"
#     path    = "vault"
#     token   = "abcd1234"  # If Consul ACLs are enabled
# }

# Example configuration for using auto-unseal, using AWS KMS.
# seal "awskms" {
#   region     = "us-east-1"
#   access_key = "AKIAIOSFODNN7EXAMPLE"
#   secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
#   kms_key_id = "19ec80b0-dfdd-4d97-8164-c6examplekey"
#   endpoint   = "https://vpce-0e1bb1852241f8cc6-pzi0do8n.kms.us-east-1.vpce.amazonaws.com"
# }

# Example configuration for using auto-unseal, using Google Cloud KMS.
# seal "gcpckms" {
#   credentials = "/usr/vault/vault-project-user-creds.json"
#   project     = "vault-project"
#   region      = "global"
#   key_ring    = "vault-keyring"
#   crypto_key  = "vault-key"
# }