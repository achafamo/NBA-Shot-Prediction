if [ -e "/etc/postgresql/9.3/main/pg_hba.conf" ]; then
	echo "pg_hba.conf is there, skipping postgresql setup"
else
	echo "pg_hba.conf is NOT there, installing postgresql"
	sudo apt-get install -y postgresql postgresql-contrib
fi

if [ $(sudo cat /etc/postgresql/9.3/main/pg_hba.conf | grep 'vagrant' | wc -l) -eq 0 ]; then
	echo "vagrant user is NOT set up for postgresql databases, adding vagrant"
	echo "local\tall\t\tvagrant\t\t\t\tpeer" | sudo tee -a /etc/postgresql/9.3/main/pg_hba.conf
	sudo -u postgres /usr/lib/postgresql/9.3/bin/pg_ctl -D /var/lib/postgresql/9.3/main restart
	sudo -u postgres psql -c "CREATE USER vagrant SUPERUSER;"
else
	echo "vagrant user is set up for postgresql databases"
fi
sudo printf "CREATE USER db_user WITH PASSWORD 'nba_database';\nCREATE DATABASE nba_database WITH OWNER db_user;">create_db.sql
sudo -u postgres psql -f create_db.sql
sudo apt-get install unzip
sudo apt-get install dos2unix
pip install SQLAlchemy
pip install psycopg2
pip install -e git+https://github.com/ethanluoyc/statsnba-playbyplay.git#egg=statsnba