#!/bin/bash
# Filename: svn_diff_version.sh
 
SVN_PATH="./code/src/yunwei"
 
last_version=$(tail -n 1 code/last_version)
 
if [ -z $last_version ];then
	echo "没有历史版本"
	cd ${SVN_PATH}
	echo "开始更新......"
	svn up
	echo "更新完毕"
	echo "记录新版本号"
        first_version=$(svn up | grep -E "版本|version|Version|At revision" | sed 's/[^0-9]//g')
	echo ${first_version} >> ../../last_version
	echo "OK,你可以上传了"
	exit 0
else
	cd ${SVN_PATH}
	svn up
	echo "更新完毕"
	new_version=$(svn up | awk '{print $3}' | grep -v ^$ | awk -F. '{print $1}')
	echo "上次版本：${last_version},当前版本:${new_version}"
 
	if [ "${last_version}" -ne "${new_version}" ];then
		if [ -e "../../patch/${last_version}_${new_version}" ]; then
			echo "已经存在差异目录"
		else
			echo "创建差异目录"
			mkdir -p ../../patch/${last_version}_${new_version}
		fi
		echo "开始分析差异文件"
		DIFF_NUM=$(svn diff -r ${last_version}:${new_version} --summarize|wc -l)
		if [ ${DIFF_NUM} -ne 0 ]; then
			DIFF_LIST=$(svn diff -r ${last_version}:${new_version} --summarize | awk -F" " '{print $2}')
			for file in ${DIFF_LIST} ; do
				echo ${file}
				FILE_NAME=`basename ${file}`
				FOLDER_NAME=`dirname ${file}`
				if [ ! -e "../../patch/${last_version}_${new_version}/${FOLDER_NAME}" ];then
					mkdir -p ../../patch/${last_version}_${new_version}/${FOLDER_NAME}
				fi
				cp -r ${file} ../../patch/${last_version}_${new_version}/${FOLDER_NAME}/
			done
			echo "记录新版本号"
			echo ${new_version} >> ../../last_version
			echo "OK,你可以上传了"
			exit 0
		else
			echo "无变化文件"
			exit 0
		fi
	else
		echo "无文件更新"
		exit 0
	fi
fi
