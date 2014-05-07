#!/bin/bash

# smbd has to be started to print on AAU
# (Else, the login box will not appear before printing)

sudo systemctl start smbd.service
sudo systemctl start cupsd.service

