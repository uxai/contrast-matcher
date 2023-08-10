# contrast-matcher
Find new colors that match your existing color contrast. This helps with building secondary and tertiary color ramps.
Simply input your original foreground HSL, background HSL and the new hue value you would like to match with.

I am currently working on a javascript version to build a web interface.

## Sample output
```
Please enter the foreground color HSL values (0, 0, 0): 144,100,70 
Please enter the background color HSL values (0, 0, 0): 208,22,15  
+------------------------------------+
|         First pair results         |
+------------------------------------+
Contrast calculated is: 11.858
Contrast perceived is:  10.437
--------------------------------------
Please enter the new foreground Hue to match (0 - 259): 300
--------------------------------------
Calculated contrast match:
--------------------------------------
H:300, S:100, L:92
Contrast ratio: 11.812
Contrast difference from origin: 0.046
--------------------------------------
Perceived contrast match:
--------------------------------------
H:300, S:97, L:85
Contrast ratio: 10.537
Contrast difference from origin: 0.1
```
## Learn more
If you would like to learn more and try the web version - check out my [blog post on this topic](http://subtractiv.com/e/2)

## Contribute
If you would like to help improve this script, feel free to make a pull request.
