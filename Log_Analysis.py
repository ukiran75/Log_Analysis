# "Database code" for the DB Forum.

import psycopg2

DBNAME = "news"


# Function to get top three articles from the database
def get_top_articles():
    db = psycopg2.connect(database=DBNAME, user="uday", host="localhost", password="supersecret")
    c = db.cursor()
    c.execute("select a.title,b.views from articles as a join (select path,count(*) as views from log "
        "where path like '/article/%' GROUP BY path order by count(*) desc LIMIT 3) as b "
        "on b.path = concat('/article/',a.slug) order by b.views DESC;")
    articles = c.fetchall()
    print("1. What are the most popular three articles of all time?")
    print("*************************************************")
    print("*  {:<34}| {:<9}*".format("Article", "Views"))
    print("*************************************************")
    for article in articles:
        print("* {:<35}| {:<8} *".format(str(article[0]), str(article[1])))
    print("*************************************************\n")
    db.close()
    db.close()
    return articles


# Function to get the popular authors of all time
def get_top_authors():
    """Return all posts from the 'database', most recent first."""
    db = psycopg2.connect(database=DBNAME, user="uday", host="localhost", password="supersecret")
    c = db.cursor()
    c.execute("select authors.name,sum(views) as total_views from authors JOIN ( select a.author as authorId, b.views"
        " as views from articles as a join(select path,count(*) as views from log "
        "where path like '/article/%' GROUP BY path) as b on b.path = concat('/article/',a.slug)) "
        "article_views on authors.id = article_views.authorId GROUP BY authors.name "
        "order by sum(views) DESC;")
    authors = c.fetchall()
    print("2. Who are the most popular article authors of all time?")
    print("***************************************")
    print("*  {:<24}| {:<9}*".format("Author","Views"))
    print("***************************************")
    for author in authors:
        print("* {:<25}| {:<8} *".format(str(author[0]),str(author[1])))
    print("***************************************\n")
    db.close()
    return authors


# Function to get on which days with more than 1% error/bad requests to the server
def get_high_error_days():
    db = psycopg2.connect(database=DBNAME, user="uday", host="localhost", password="supersecret")
    c = db.cursor()
    c.execute("select * from (select A.date as date,round(100.0*B.error/A.views,2) "
              "as error_perct from"
              "(SELECT time::date as date,count(*) as views from log  group by time::date) A,"
              "(SELECT time::date as date,count(*)as error from log  where status like '404 %' group by time::date) B "
              "where A.date=B.date) error where error_perct >1.0")
    max_error_day = c.fetchall()
    print("3. On which days did more than 1% of requests lead to errors?")
    print("************************")
    print("*  DATE      | Percent *")
    print("************************")
    for day in max_error_day:
        print("* {:<10} | {:<6}  *".format(str(day[0]),str(day[1])))
    print("************************")
    db.close()
    return max_error_day


get_top_articles()
get_top_authors()
get_high_error_days()