### Install
---

pip install scrapy

pip install Pillow

pip install SQLAlchemy

pip install mysql-connector

pip install mysqlclient

---

###  settings.py

---

`For connect to database`

drivername="mysql",

user="user_name_DB",

passwd="password",

host="host_DB",

port="port_DB",

db_name="name_DB",

---

`For output email with statistics`

MAIL_FROM = 'who send email'

MAIL_HOST = 'smtp_server'

MAIL_USER = 'mail_user'

MAIL_PASS = 'password'

MAIL_SSL = True

MAIL_PORT = 465

MAIL_TLS = False

STATSMAILER_RCPTS = 'email_recipient'

`or`

STATSMAILER_RCPTS = ['test@test.test', 'test2@test.test']

---

`File with proxy servers for one`

`https:/8.8.8.8:3180`

`or more`

`https:/8.8.8.8:3180`

`https:/9.9.9.9:8080`

`....`

`path/name_file relative to the startup folder`

PROXY_LIST = ['proxy.txt']

---

`Number of retries on error`

RETRY_TIMES = 10

`When there will be the first RETRY, proxies will not change for this URL. When the retriever becomes 9, then this invalid proxy server will be deleted.`

---

`Folder with images`

`path/name_file relative to the startup folder`

IMAGES_STORE = 'name_folder'

---

### START YOU PROJECT

`cd path_to_project/name_project/name_project/`

**RUN**`

scrapy runspider spiders/name_you_scrapy.py -a category=restaurants -a address="San Francisco, CA" 

`or`

scrapy crawl name_you_scrapy -a category=restaurants -a address="San Francisco, CA" 

