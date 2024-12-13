#!/bin/bash

source optparse.bash

optparse.define short=n long=name desc="Name of the RAM disk" variable=name default=ramdisk
optparse.define short=s long=size desc="Size of the RAM disk" variable=size default=1G

source $(optparse.build)

if [ $(id -u) -ne 0 ]
    then echo Please run this script as root or using sudo!
    exit
fi

rdDir="/tmp/ramdisk"

mkdir $rdDir
chmod 777 $rdDir
echo "Created directory at $rdDir"

mount -t tmpfs -o size=$size $name $rdDir
echo "Mounted tmpfs $name at $rdDir of size $size"

mount | tail -n 1
