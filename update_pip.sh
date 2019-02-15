#!/bin/bash
for i in `pip3 list|awk '{print $1}'`
do
    sudo pip3 install -U $i
done
