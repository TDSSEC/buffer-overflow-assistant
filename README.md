# Buffer Overflow Assistant
## What is this
This was built to assist with Windows Buffer Overflows, whilst learning in the OSCP labs.  
Please note, **this will not work out of the box in the OSCP**. You should learn using the provided materials how to perform buffer overflow attacks.  
For me, writing a script to help automate some of the more manual tasks was a great way to learn.
## What it does
This provides a menu with options from 1-9 which allow you to execute certain tasks. 
Example - fire a for loop of A's to find out how many crash the service.  
Example - send bad characters, you can then manually check to see what needs to be removed  
Example - utilises patternCreate to find the offset value.
## How to Use
The script will need modifying, the sections that need to be modified are commented out in the script. This is typically where the unique PoC causing the overflow will need to be written to.
