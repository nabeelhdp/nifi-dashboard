# NiFi Dashboard
Authenticate against NiFi login and poll stats from NiFi instance

To view system diagnostics on console :

Update `config.ini` and run as 
`python nifipoll.py`

For dashboard, copy `bottle.py` from bottle webpage and drop in the same directory as the `nifi_poll.py`

Place `canvas.min.js` into a new folder called static ( Note: The trial expires in 2 months. So purchase full version for production use)

Run

`python dashboard.py &`

Wait till the url is shown on console.

Once seen, open browser and paste url followed by /dashboard

Eg. http://nifinode.tld/8080/dashboard

![Dashboard sample](https://github.com/nabeelhdp/NiFi-Dashboard/blob/master/SingleSnapshotView.PNG)
