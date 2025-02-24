FROM apache/airflow:2.10.4
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY quarto.sh /
RUN cd / && bash /quarto.sh

COPY setup_conn.py $AIRFLOW_HOME
RUN python $AIRFLOW_HOME/setup_conn.py

USER root

# openjdk-17-jdk : installs java as spark requires it 
# procps : installs ps to monitor processes 
# --no-install-recommends : keep image light by avoiding unnecessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk procps

# set JAVA_HOME to where its installed
ENV JAVA_HOME='/usr' 
# update the path variables
ENV PATH=$PATH:$JAVA_HOME/bin

# download spark
RUN curl https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz -o spark-3.5.1-bin-hadoop3.tgz

# Change permissions of the downloaded tarball to make it accessible
RUN chmod 755 spark-3.5.1-bin-hadoop3.tgz

# Create the target directory and extract the tarball to it
# --strip-components=1 : removes root directory (which is 'spark-3.5.1-bin-hadoop3/') from extracted files, everything gets put in /opt/spark = easier installation, no nested dirs
    # you would also have to do ENV SPARK_HOME=/opt/spark/spark-3.5.1-bin-hadoop3
RUN mkdir -p /opt/spark && tar xvzf spark-3.5.1-bin-hadoop3.tgz --directory /opt/spark --strip-components=1

# sets SPARK_HOME env variable to point to spark installation directory
# updates path so you can run commands from anywhere
ENV SPARK_HOME='/opt/spark'
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# verify Java and ps command installation
RUN echo "JAVA_HOME: $JAVA_HOME" && \
    echo "PATH: $PATH" && \
    java -version && \
    ps aux