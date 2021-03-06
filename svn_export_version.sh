#!/bin/bash
#Filename: svn_full_version.sh

EXPORT_PATH="./code/export"
SVN_USER="jack"
SVN_PASS="LVS@98186"
SVN_URL="https://192.168.2.214/leshu-svn/yunwei"
VERSION=$1

svn export --force --non-interactive --trust-server-cert --username ${SVN_USER} --password ${SVN_PASS} ${SVN_URL} ${EXPORT_PATH}/${VERSION} 2>&1>/dev/null

if [ "$?" -eq 0 ];then
	echo "本地导出成功"
else
	echo "本地导出失败"
	exit 1
fi
