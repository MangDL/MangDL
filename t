readarray -d - -t ls<<<0.0.1-0+20211209230346721736
echo $ls | awk '{print $1}'
