#!/usr/bin/bash

#a little script to remove trash

KEY1="__pycache__"
KEY2=".DS_Store"

k1list=$(find . -name $KEY1)
k2list=$(find . -name $KEY2)

rm -rf $k1list
rm -rf $k2list

# git rm (if necessary
git rm $k1list -rf
git rm $k2list -rf







