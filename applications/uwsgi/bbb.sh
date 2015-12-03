VG_NAME='vg-mysql'
BASEDIR='/opt/mysql'
MYSQLBASE='/usr/local/mysql'
SVN_URL="https://192.168.5.246/svn/cloud/Goni/trunk/storage/seeddb"
SVN_USER="zhanshige"
SVN_PASS="C1c1b0b0"




svn --username ${SVN_USER} --password ${SVN_PASS} --no-auth-cache checkout ${SVN_URL} /tmp/abc/ --quiet <<EOF
t
EOF
echo 'svn checkout successfully'
