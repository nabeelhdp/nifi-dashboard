# Poll NiFi stats
Authenticate against NiFi login and poll stats from NiFi instance

To view system diagnostics on console :

Update `config.ini` and run as 
`python nifipoll.py`

For dashboard, copy bottle.py from bottle webpage and drop in the same directory as the `nifi_poll.py`
run
`python dashboard.py &`
Wait till the url is shown on console.
Once seen, open browser and paste url followed by /pie or /table to view respective visualizations
Make sure canvas.min.js is copied to the static folder.
