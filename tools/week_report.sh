docker exec -it teamcity-agent-week bash -c "source ~/.bashrc; cd /workspace/week/tools; python wiki_api.py && python teamcity_api.py && python3 gen_report.py >> week.log 2>&1 " 
sh send_email.sh  >> week.log 2>&1 
