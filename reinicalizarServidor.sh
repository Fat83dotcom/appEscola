#!/usr/bin/bash
sudo systemctl restart nginx
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
sudo systemctl status nginx
