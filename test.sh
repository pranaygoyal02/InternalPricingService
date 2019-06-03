#!/bin/bash
set -x
echo "Processing Order_id 12345"
curl -i http://localhost:5000/todo/api/v1.0/tasks/12345/GBP_USD > test_output.log
#if [ $? == 0 ];then
#echo "Processed Order_id 12345 and Processing the next order"
curl -i http://localhost:5000/todo/api/v1.0/tasks/5000/GBP_USD >> test_output.log
echo "Process Complete"