# The Auto Booker 9000!

### WIP WIP WIP Does not work

Tired of logging in and booking rooms at swinburnes hawthorne campus?
with the power of my googling skills and procrastination to do my assignments, now you can!

## The plan:
* Run this python script using selenium on headless chrome on my personal server
* use a cronjob to run the script daily
* send a push notification to my phone with the results
* intergrate with google calander to automatically place the booking

## setting up ubuntu 18.04 (bionic)
* ```apt update && apt upgrade -y```
* ```apt install chromium-browser```
* ```apt install chromium-chromedriver```
* ```apt install python3-selenium```