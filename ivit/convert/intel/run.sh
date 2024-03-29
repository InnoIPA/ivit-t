#!/bin/bash
# ---------------------------------------------------------
# Set the default value of the getopts variable 
mount_gpu="--gpus=all"
workspace="/workspace"
main_container="ivit-t"
mode=false
docker_image="willqiuinnodisk/intel-convert"
docker_name="intel-convert"
# ---------------------------------------------------------
# help
function help(){
	echo "-----------------------------------------------------------------------"
	echo "Convert model."
	echo
	echo "Syntax: scriptTemplate [-p|m|h]"
	echo "options:"
	echo "m		Run code on terminal"	
	echo "h		help."
	echo "-----------------------------------------------------------------------"
}

while getopts "mh" option; do
	case $option in
		m )
			mode=true
			;;
		h )
			help
			exit
			;;
		\? )
			help
			exit
			;;
		* )
			help
			exit
			;;
	esac
done

# ---------------------------------------------------------
# Open container mode
if [[ ${mode} == false ]]; then
	volume="--volumes-from ${main_container}"
else
	volume="-v `pwd`:${workspace}"
fi

# ---------------------------------------------------------
# open docker container
echo "-----Run container of intel-----"

# Run container
docker_cmd="docker run \
			--name ${docker_name} \
			${mount_gpu} \
			--user root \
			--rm -dt \
			--net=host --ipc=host \
			-w ${workspace} \
			${volume}\
			-v /etc/localtime:/etc/localtime:ro \
			${docker_image} \" bash \""

echo ""
echo -e "Command: ${docker_cmd}"
echo ""
bash -c "${docker_cmd}"
echo "Converted."













