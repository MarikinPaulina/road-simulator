#!/bin/bash

for i in {0..52}; do
  let j=$i+37
  mv "cross2_00$j.png" "cross2_00$i.png"
done
