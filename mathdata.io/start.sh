if [ ! -d "./apache-tomcat-9.0.12" ]
    wget https://www-eu.apache.org/dist/tomcat/tomcat-9/v9.0.12/bin/apache-tomcat-9.0.12.tar.gz

    tar xf apache-tomcat-9.0.12.tar.gz
fi

cp -R ./dist/MathDataLanding ./apache-tomcat-9.0.12/webapps/

./apache-tomcat-9.0.12/bin/startup.sh