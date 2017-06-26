#! python3.4

import psycopg2

DBNAME = "news"
"""Query to get the top viewed Articles"""
Articles_Query = "select a.title,b.views from articles as a join (" \
                 "select path,count(*) as views from log where path like " \
                 "'/article/%' GROUP BY path order by count(*)desc LIMIT 3) " \
                 "as b on b.path = concat('/article/',a.slug)" \
                 "order by b.views DESC"

"""Query to get favorite Authors of all time"""
Authors_query = "select authors.name,sum(views) as total_views from authors " \
                "JOIN ( select a.author as authorId, b.views as views from " \
                "articles as a join(select path,count(*) as views from log " \
                "where path like '/article/%' GROUP BY path) as b on " \
                "b.path = concat('/article/',a.slug)) article_views on " \
                "authors.id = article_views.authorId GROUP BY authors.name " \
                "order by sum(views) DESC;"

"""Query to get the day with more than 1% error requests"""
Max_Error_Query = "select * from (select A.date as date," \
                  "round(100.0*B.error/A.views,2) as error_perct from" \
                  "(SELECT time::date as date,count(*) as views from log " \
                  "group by time::date) A,(SELECT time::date as date," \
                  "count(*)as error from log  where status like '404 %' " \
                  "group by time::date) B where A.date=B.date) error " \
                  "where error_perct >1.0"


# Connect to the PostgreSQL database.Returns a database connection.
def connect(DBNAME):
    try:
        db = psycopg2.connect(database=DBNAME, user="uday", host="localhost",
                              password="supersecret")
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        exit(1)


# Function to Execute the query and return the results
def fetch_query(query):
    db, c = connect(DBNAME)
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


# Function to print top three articles from the database.
def print_top_articles():
    articles = fetch_query(Articles_Query)
    print("1. What are the most popular three articles of all time?")
    print("*************************************************")
    print("*  {:<34}| {:<9}*".format("Article", "Views"))
    print("*************************************************")
    for article in articles:
        print("* {:<35}| {:<8} *".format(str(article[0]), str(article[1])))
    print("*************************************************\n")


# Function to print the popular authors of all time.
def print_top_authors():
    authors = fetch_query(Authors_query)
    print("2. Who are the most popular article authors of all time?")
    print("***************************************")
    print("*  {:<24}| {:<9}*".format("Author", "Views"))
    print("***************************************")
    for author in authors:
        print("* {:<25}| {:<8} *".format(str(author[0]), str(author[1])))
    print("***************************************\n")


# Function to print which day we had more than 1% error requests to the server
def print_high_error_days():
    max_error_day = fetch_query(Max_Error_Query)
    print("3. On which days did more than 1% of requests lead to errors?")
    print("************************")
    print("*  DATE      | Percent *")
    print("************************")
    for day in max_error_day:
        print("* {:<10} | {:<6}  *".format(str(day[0]), str(day[1])))
    print("************************")


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_high_error_days()
