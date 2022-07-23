source env/bin/activate
while true
do
    git pull
    git checkout main
    sleep .5
    echo 
    echo "Running new instance of routiney:"
    python main.py
    sleep 1
done
deactivate