# for debugging in python
    * if you are using VScode then launch.json is already created for you
    * https://code.visualstudio.com/docs/python/debugging

# Add your public ssh key to the machine
   * cat ~/.ssh/<id_rsa|ed_25..>.pub | type C:\Users\<user>\.ssh\<id_rsa|ed25..>.pub
   * ssh into ec2 instance:
    - ssh -i ~/.ssh/<id_rsa|ed_25..> ubuntu@<public-instance-ip>
   * add your public key to ~/.ssh/authorized_keys

# to copy all backend files to the machine
    * cd Alpha
    * scp -r backend ubuntu@<public-instance-ip>:/home/ubuntu

# to run on a new ec2 instance
    * cd backend;sudo apt-get -y update;sudo apt-get install dos2unix;dos2unix install.sh;source install.sh

# ssh
    child crawler: (172.31.17.222)
        * ssh ubuntu@ec2-63-34-9-19.eu-west-1.compute.amazonaws.com
        * scp -r backend ubuntu@ec2-63-34-9-19.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * xvfb-run --server-num=99 python3 Crawler/child_crawler.py

    brute crawler: (172.31.29.221)
        * ssh ubuntu@ec2-54-78-140-177.eu-west-1.compute.amazonaws.com (ip-172-31-29-221)
        * scp -r backend ubuntu@ec2-54-78-140-177.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * python3 Crawler/brute_crawler.py

    parent crawler: (172.31.22.150)
        * ssh ubuntu@ec2-63-32-98-107.eu-west-1.compute.amazonaws.com
        * scp -r backend ubuntu@ec2-63-32-98-107.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * python3 Crawler/crawler.py

    vulnerability scanner: (172.31.31.188)
        * ssh ubuntu@ec2-3-249-197-165.eu-west-1.compute.amazonaws.com
        * scp -r backend ubuntu@ec2-3-249-197-165.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * python3 VulnerabilityScanner/main.py

    html validator: (172.31.21.8) 
        * ssh ubuntu@ec2-18-203-95-175.eu-west-1.compute.amazonaws.com
        * scp -r backend ubuntu@ec2-18-203-95-175.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * python3 html_validator/html_validator.py

    js checker: (172.31.26.128)
        * ssh ubuntu@ec2-54-217-155-211.eu-west-1.compute.amazonaws.com
        * scp -r backend ubuntu@ec2-54-217-155-211.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * python3 js_checker/js_checker.py

    error scanner: (172.31.20.129)
        * ssh ubuntu@ec2-3-253-72-225.eu-west-1.compute.amazonaws.com
        * scp -r backend ubuntu@ec2-3-253-72-225.eu-west-1.compute.amazonaws.com:/home/ubuntu
        * python3 Error_Scanner/error_scanner.py