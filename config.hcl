storage "file" {
  path = "./vault-data"
}

#Disabled due to mlock related errors in WSL, may not be needed in WSL2
disable_mlock = "true"

listener "tcp" {
  tls_disable = "true"
}
