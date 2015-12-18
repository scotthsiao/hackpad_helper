# hackpad_helper
Somo help scripts for Hackpad

# Features
hackpad_crawler: Fetch all Hackpad pads' title to CSV file since the "show more" is not functional

#hackpad_crawler
Usage:

  1. rename account.ini.sample to account.ini
  
  ```
    mv account.ini.sample account.ini
  ```
  2. edit the ini file settings
  
  ```
  $ cat account.ini
  [General]
  workspace = https://yourworkspace.hackpad.com/
  api_key = *******
  api_secret = ******
  ```
  3. run the crawler
  
  ```
  $ python crawler.py
  ```
  4. check result file called "pad_list.csv"
  
  ```
  $ cat pad_list.csv
  ```
