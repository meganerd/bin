#!/bin/bash

#convert 1.jpg 2.jpg +append wallpaper.jpg

#files=(~/Downloads/wallpaper_dualmonitor/test/*)
#printf "%s\n" "${files[RANDOM % ${#files[@]}]}"

VERSION=1.00
declare -i COUNT
declare -a SOURCES
declare TARGET

print_usage() {
	printf "Usage:\n"
	printf "generate_wallpater.sh -f <src file> -d <src directory> -T <target file>\n"
}

print_help() {
	printf "generate_wallpaper.sh\n\n"
	printf "Combine multiple wallpapers into a single wallpaper.\n\n"
	print_usage
	printf "\nOptions:\n"
	printf "   -f (--file)       Source image file\n";
	printf "   -d (--directory)  Source directory (Random image file)\n";
	printf "   -T (--target)     Target image file to generate\n"
	printf "                     (Overwrites existing file)\n";
	printf "   -V (--version)    script version\n";
	printf "   -h (--help)       usage help \n\n";
}

ValidateDirectory() {
	#echo "ValidateDirectory() $1"
	if [ ! -d "$1" ]; then
		echo "Error: Directory \"$1\" does not exist!"
		exit 1
	fi
	return 0
}

ValidateFile() {
	#echo "ValidateFile() $1"
	if [ ! -f "$1" ]; then
		echo "Error: File \"$1\" does not exist!"
		exit 1
	fi

	if [[ ${1: -4} != ".jpg" && ${1: -4} != ".png"  ]]; then
		echo "Error: Unsupported file format for file \"${1}\" - Expected .jpg or .png"
		exit 1
	fi

	return 0
}

GetRandomFileFromDirectory() {
	#echo "GetRandomFileFromDirectory() $1 $2"
	directory=$2

	# Get all image files within directory
	files=(`find $directory -maxdepth 1 | egrep -e '.*\.(jpg|png)$'`)

	# Confirm that there are at least one wallpaper in directory
	if [[ ${#files[@]} > 0 ]]; then
		random_file=${files[RANDOM % ${#files[@]}]}
		eval "$1=${random_file}"
		return 0
	fi
	
	echo "Error: Couldn't find valid file within directory \"$directory\""
	exit 1
}




##### Handle start input parameters - Assign input values to variables. #####

# options may be followed by one colon to indicate they have a required argument
if ! options=$(getopt -o f:d:T:hV --long source:,target:,help,version -- "$@"); then
	# something went wrong, getopt will put out an error message for us
	exit 1
fi
eval set -- $options

while [ $# -gt 0 ]
do
	 case $1 in
	 -f|--file)
		ValidateFile "$2"
		SOURCES[$COUNT]="$2";
		((COUNT++));
		shift ;;
	 -d|--directory)
		ValidateDirectory "$2"
		GetRandomFileFromDirectory 'SOURCES[$COUNT]' $2
		((COUNT++));
		shift ;;
	 -T|--target) TARGET+="$2"; shift ;;
	 -h|--help) print_help; exit 0 ;;
	 -V|--version) echo "Version $VERSION"; exit 0 ;;
	 (--) shift; break;;
	 (-*) echo "$0: error - unrecognized option $1" 1>&2; exit 1;;
	 (*) break;;
	 esac
	 shift
done
##### END OF Handle start input parameters - Assign input values to variables. #####


if [[ -z ${SOURCES} || $COUNT < 1 ]]; then
	echo "Add at least one file and/or directory combined. (--file/--directory flag)"
	exit 1
fi

# If we have more than one source, we need to generate a combined wallpaper
if [[ $COUNT > 1 ]]; then

	# We need to generate a temp file (target file), so it have to be specified where to save it.
	if [[ -z ${TARGET} ]]; then
		  echo "Target file missing. (--target flag)" >&2
		  exit 1
	fi

	# Generate new wallpaper
	exec `convert ${SOURCES[@]} +append ${TARGET}`

	# Set wallpaper
	exec `hsetroot -fill ${TARGET}`

else	# we do not need to generate a wallpaper, as only one wallpaper is needed

# Set wallpaper
exec `hsetroot -fill ${SOURCES[0]}`

fi




