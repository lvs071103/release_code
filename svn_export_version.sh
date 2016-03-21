#!/bin/bash
#Filename: svn_full_version.sh

EXPORT_PATH="./code/export/"
SVN_USER="test"
SVN_PASS="test"
SVN_URL="https://192.168.1.214/xxxx/yunwei/"
VERSION=$1

svn export --force --non-interactive --trust-server-cert --username ${SVN_USER} --password ${SVN_PASS} ${SVN_URL} ${EXPORT_PATH}/${VERSION} 2>&1>/dev/null

if [ "$?" -eq 0 ];then
	echo "本地导出成功"
else
	echo "本地导出失败"
	exit 1
fi

#cd ${EXPORT_PATH}
#tar -czf ${VERSION}.tar.gz ${VERSION}
#if [ "$?" -eq 0 ];then
#	echo "压缩成功,你可以上传了"
#	rm -rf ${VERSION}
#	exit 0
#else
#	echo "压缩失败"
#	exit 1
#fi
