#!/usr/bin/env bash
#
# Install a certificate in the Firefox DB using CERTutil
#
# -AUTOR: Breogan Costa @ RHEA Group
#
# -TESTED: Firefox 85.0.1 (64 bit) on Ubuntu 20.04 LTS and Ubuntu Mate 18.04.5 LTS



function usage {
  echo "Error: no certificate filename or name supplied."
  echo "Usage: $ ./linux-cert-install-firefox.sh <certname>.pem <Cert-DB-Name>"
  exit 1

}

if [ -z "$1" ] || [ -z "$2" ]
  then
    usage
fi

certificate_file="$1"
certificate_name="$2"
for certDB in $(find  ~/.mozilla* -name "cert9.db")
do
  cert_dir=$(dirname ${certDB});
  echo "Mozilla Firefox certificate" "install '${certificate_name}' in ${cert_dir}"
  certutil -A -n "${certificate_name}" -t "TCu,Cuw,Tuw" -i ${certificate_file} -d sql:"${cert_dir}"
done
