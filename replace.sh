#!/usr/env bash

shopname="amazing shop"
rmsshopuser="RMSshopuser"
rmsshoppasswd="RMSshoppasswd"
rmsuser="RMSuser"
rmspasswd="RMSpasswd"
shopurl="https://yourshopurl.com"
nickname="nickname"


find . -type f -name "*.py" -print0 | xargs -0 sed -i "s/__shopname__/$shopname/g"
find . -type f -name "*.py" -print0 | xargs -0 sed -i "s/__rmsshopuser__/$rmsshopuser/g"
find . -type f -name "*.py" -print0 | xargs -0 sed -i "s/__rmsshoppasswd__/$rmsshoppasswd/g"
find . -type f -name "*.py" -print0 | xargs -0 sed -i "s/__rmsuser__/$rmsuser/g"
find . -type f -name "*.py" -print0 | xargs -0 sed -i "s/__rmspasswd__/$rmspasswd/g"
find . -type f -name "*.py" -print0 | xargs -0 sed -i "s#__shopurl__#$shopurl#g"
find . -type f -name "*.py" -print0 | xargs -0 sed -i "s/__nickname__/$nickname/g"

find . -type f -name "*.html" -print0 | xargs -0 sed -i "s/__shopname__/$shopname/g"
find . -type f -name "*.html" -print0 | xargs -0 sed -i "s#__shopurl__#$shopurl#g"
find . -type f -name "*.html" -print0 | xargs -0 sed -i "s/__nickname__/$nickname/g"
