if [ -f "already_ran" ]; then
    # pass
    echo "Already ran the Entrypoint once. Holding indefinitely for debugging.";
else
    # read ENV_VAR and create user;
    useradd -m $NAME -s /bin/bash;
    sudo adduser $NAME sudo;
    echo $NAME:$PASSWORD | chpasswd;
    # change volume owner for access promise
    if [ -d "/user_data" ]; then 
        # change HOME dir for user
        usermod -d /user_data $NAME
        cp /etc/skel/.bashrc /user_data
        cp /etc/skel/.profile /user_data
        #
        mkdir /user_data/.jupyter
        cp /root/.jupyter/jupyter_notebook_config.py /user_data/.jupyter/jupyter_notebook_config.py
        chmod -R 775 /user_data/.jupyter
        # user own /user_data
        chown -R $NAME:$NAME /user_data
    fi
fi
touch already_ran;

# Run repeat
service fail2ban start;
service ssh start;
if [ -d "/user_data" ]; then 
    # volume exists" 
    (nohup runuser -l $NAME -c "export PASSWORD=$PASSWORD&&jupyter notebook --ip=0.0.0.0 --notebook-dir=/user_data" 2> /dev/null&);
    (nohup runuser -l $NAME -c "export PASSWORD=$PASSWORD&&export SHELL=/bin/bash&&code-server --host 0.0.0.0 /user_data" 2> /dev/null&);
else
    (nohup runuser -l $NAME -c "export PASSWORD=$PASSWORD&&jupyter notebook --ip=0.0.0.0 --notebook-dir=/" 2> /dev/null&);
    (nohup runuser -l $NAME -c "export PASSWORD=$PASSWORD&&export SHELL=/bin/bash&&code-server --host 0.0.0.0 /" 2> /dev/null&);
fi

