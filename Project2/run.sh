#!/bin/bash

chmod +x autocut.sh
./autocut.sh $1

chmod +x autoflip.sh
where=`pwd`
for file in `ls src/$1_*`
    do
        ./autoflip.sh `realpath $file` $where/result/${file#"src/"}  $2
        cd $where
    done

