# Project architecture
## Description
Here you can see a master-slave replication MySQL cluster with 
two hosts and application server with gunicorn and django WSGI app.

Database replication was selected to not take care of database write statements distribution.
So, if master host is offline, app became read-only.  

Read statements are randomly distributed among database hosts. 
If one host fails, read queries will be directed to another.

Project can be started with
        
    docker-compose up
    
When startup is complete, port 8000 is exposed for accessing HTTP REST API 

You can access these API endpoints:

1. Get reader by id. Default id range is [1..50000] 
    
       GET: http://localhost:8000/api/v1/library/reader/<pk>/
    
   Example:
    
       $ curl http://localhost:8000/api/v1/library/reader/1/
    
2. Get CSV export of all readers and books

       GET: http://localhost:8000/api/v1/library/export/
    
   Example:
    
       $ curl -O -J http://localhost:8000/api/v1/library/export/
    
## Startup order:
1. Database master and slave containers start
1. App container starts and waits for database connections become available
1. DBMS start to apply cluster config [can connect, but it's a trap, actually it is a bad idea start doing stuff here]
1. DBMS restart after applying config [no connections here, previous connections are aborted]
1. DBMS start again [**can connect to database at last**]
1. App container begin doing django things: migrate, generate data and launch wsgi server

# Database router logic
Router manages only read connections, writes always directed to master database host.
Read connections randomly distributed among master and slave database hosts.

If one hosts have connection problems, it is marked as "offline" and not used for reads.
After a time (default 30 seconds) mark is removed and new attempt to connect is made. 
If still offline - marked again, and so on.

When master database host is offline, app is working in read-only mode. Writes will raise an exception.

# Results
1. All endpoints are working if there is at least one database host online
1. When two hosts are online, read load are distributed among them increasing read performance
