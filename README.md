# Log Analysis
<p>  In this project, a large database with over a million rows is explored by building complex SQL queries to draw business conclusions for the data.

The project mimics building an internal reporting tool for a newpaper site to discover what kind of articles the site's readers like. The database contains newspaper articles, as well as the web server log for the site.
</p>

## How to run it ?

1. Install Python in your laptop/workstation.
   <https://www.python.org/downloads/>
2. Clone this repository to your laptop/workstation.
3. Open terminal(linux)/cmd(windows) and change your working directory to the cloned folder.
   In windows(cmd) : `cd /d {{Folder_location}}`
   In linux : `cd {{Folder_location}}`
4. Install psycopg2 for accessing postgresql(driver) using pip
    `pip install psycopg2`
5. Install Postgresql on your worstation and create a database with name `news`
    <https://www.postgresql.org/download/>
6. Download the log dump to insert the data into the database and unzip it `newsdata.sql`
    <https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip>
7. Insert the data into the database using the command : `psql -d news -f newsdata.sql`
8. Modify the Log_analysis project with your `DBNAME,USER,PASSWORD` of postgresql.
9. Run the Log_Analysis.py file in the folder using the command:
   `python Log_Analysis.py`
10. The output will be displayed on the terminal.
## How will be the output ?

```
1. What are the most popular three articles of all time?
*************************************************
*  Article                           | Views    *
*************************************************
* Candidate is jerk, alleges rival   | 338647   *
* Bears love berries, alleges bear   | 253801   *
* Bad things gone, say good people   | 170098   *
*************************************************

2. Who are the most popular article authors of all time?
***************************************
*  Author                  | Views    *
***************************************
* Ursula La Multa          | 507594   *
* Rudolf von Treppenwitz   | 423457   *
* Anonymous Contributor    | 170098   *
* Markoff Chaney           | 84557    *
***************************************

3. On which days did more than 1% of requests lead to errors?
************************
*  DATE      | Percent *
************************
* 2016-07-17 | 2.28    *
************************