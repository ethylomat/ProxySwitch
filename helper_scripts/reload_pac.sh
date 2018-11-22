#! /bin/sh -u
networksetup -listallnetworkservices | awk 'NR>1' | while read SERVICE ; do
  if networksetup -getautoproxyurl "$SERVICE" | grep '^Enabled: Yes' >/dev/null; then
    networksetup -setautoproxystate "$SERVICE" off
    networksetup -setautoproxystate "$SERVICE" on
  fi
done