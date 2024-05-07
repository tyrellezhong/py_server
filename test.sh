#!/bin/bash
function getsum(){
    local sum=0  #局部变量
    for((i=$1; i<=$2; i++)); do
        ((sum+=i))
    done

    echo $sum
    echo $?
    # return $?
}
m=1
n=2
total=$(getsum $m $n)
echo "The sum is $total"
#也可以省略 total 变量，直接写成下面的形式
#echo "The sum is "$(getsum $m $n)