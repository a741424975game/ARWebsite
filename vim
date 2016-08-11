server {
    listen      80;
    server_name armanager.imwork.net;  
    charset     utf-8;
 
 
    location /media  {
        alias /home/ubuntu/ARWebsite/uploads;
    }
 
    location /static {
        alias /home/ubuntu/ARWebsite/MyApp/static;
    }
 
    location / {
        uwsgi_pass  unix:/home/ubuntu/ARWebsite/uwsgi.sock;
        include     /etc/nginx/uwsgi_params;
    }
}
