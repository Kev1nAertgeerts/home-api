#####Variables###########
server_ipv4=192.168.68.54
project_name=home-api
user_name=admin
repository_private=https://github.com/Kev1nAertgeerts/home-api.git
main_branche_name=main
database=drank

#####Script########
sudo apt-get update
yes | sudo apt-get upgrade

cd /
cd /var/opt
adduser --system --home=/var/opt/$project_name --no-create-home --disabled-password --group --shell=/bin/bash $user_name

cd /opt
sudo mkdir $project_name
cd $project_name

yes | apt-get install git
git init
git remote add origin $repository_private
git pull origin $main_branche_name

yes | apt-get install virtualenv
virtualenv --python=python3 --system-site-packages venv
source venv/bin/activate


pip install -r requirements.txt
deactivate
/opt/$project_name/venv/bin/python3 -m compileall -x /opt/$project_name/venv/ /opt/$project_name

mkdir -p /var/opt/$project_name
chown $user_name /var/opt/$project_name # verander owner
mkdir -p /var/log/$project_name
chown $user_name /var/log/$project_name

mkdir /etc/opt/$project_name


cd /etc/opt/$project_name


chown root:$user_name /etc/opt/$project_name
chmod u=rwx,g=rx,o= /etc/opt/$project_name

/opt/$project_name/venv/bin/python3 -m compileall /etc/opt/$project_name

cd /

#####postgresql#######
sudo apt-get install -y postgresql postgresql-contrib

sudo systemctl start postgresql
sudo systemctl enable postgresql

sudo -u postgres psql
ALTER USER postgres WITH SUPERUSER;
CREATE DATABASE $database;

psql -d $database -U postgres
GRANT ALL PRIVILEGES ON DATABASE $database TO postgres;

\q
exit

#####nginx#######
cd /
yes | apt-get install nginx-light
cd /etc/nginx/sites-available

cat <<EOF >$project_name.be
server {
	listen 80;
	server_name $server_ipv4;
	root /var/www/$project_name.be;
	
	location / {
		proxy_pass         http://127.0.0.1:8000/;
		proxy_http_version 1.1;
		proxy_set_header   Upgrade \$http_upgrade;
		proxy_set_header   Connection keep-alive;
		proxy_set_header   Host \$host;
		proxy_cache_bypass \$http_upgrade;
		proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
		proxy_set_header   X-Forwarded-Proto \$scheme;
	}

	location /ws {
		proxy_pass         http://127.0.0.1:8000/ws;
		proxy_http_version 1.1;
		proxy_set_header   Upgrade \$http_upgrade;
		proxy_set_header   Connection "upgrade";
		proxy_set_header   Host \$host;
		proxy_cache_bypass \$http_upgrade;
		proxy_set_header   X-Forwarded-For \$proxy_add_x_forwarded_for;
		proxy_set_header   X-Forwarded-Proto \$scheme;
	}
}
EOF

cd /
cd /etc/nginx/sites-enabled
ln -s ../sites-available/$project_name.be

cd /

mkdir -p /var/cache/$project_name/static
mkdir -p /var/opt/$project_name/media
chown $user_name /var/opt/$project_name/media

source /opt/$project_name/venv/bin/activate

/opt/$project_name/venv/bin/pip install gunicorn

/opt/$project_name/venv/bin/python3 -m compileall /etc/opt/$project_name


######## fast-api service #######
cd /etc/systemd/system

cat <<EOF >$project_name.service

[Unit]
Description=FastAPI application
After=network.target

[Service]
User=admin
Group=admin
WorkingDirectory=/opt/home-api
Environment="PATH=/opt/home-api/venv/bin"
ExecStart=/opt/home-api/venv/bin/uvicorn fast:app --host 127.0.0.1 --port 8000 >
Restart=always

[Install]
WantedBy=multi-user.target

EOF

cd /etc/systemd/system
sudo ln -s /opt/$project_name/$project_name.service
sudo systemctl start $project_name
sudo systemctl enable $project_name

service nginx restart