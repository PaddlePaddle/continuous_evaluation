#array=(guochaorong@baidu.com)
array=(paddle-dev@baidu.com)
for mail in ${array[@]}
do
    cat index.html | formail -I "Content-type:text/html;charset=gb2312" -I "Subject: PaddlePaddle CE weekly report." -I "To:"$mail | /usr/sbin/sendmail -t guochaorong123@163.com
done
