import psycopg2
import re
import json

def read_freq_file(freqfile):
    click.echo(freqfile)
    f=open(freqfile,"r")
    f1 = f.readlines()
    for line in f1:
        line = line.rstrip()
        splitline = line.split("\t")
        form = splitline[0]
        postag = splitline[1]
        lemma = splitline[2]
        count = splitline[3]
        click.echo(postag)
        click.echo("hi")


def write2db(freqfile):
    click.echo(freqfile)
    try:
        connection = psycopg2.connect(user = "yourdictionary",
                                      password = "DQBx5TKaD5Xe6QRi",
                                      host = "yourdictionary-dev.cqtzt424uvng.us-east-1.rds.amazonaws.com",
                                      port = "5432",
                                      database = "semantic_vectors")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ("hello world")
        print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        f = open(freqfile, "r")
        f1 = f.readlines()
        for line in f1:
            line = re.sub(r'\'', '\'\'', line)
            line = line.rstrip()
            splitline = line.split("\t")
            form = splitline[0]
            postag = splitline[1]
            lemma = splitline[2]
            count = splitline[3]
            click.echo(postag + " " + lemma + " " + form + " " + count)
            try:
                cursor = connection.cursor()
                sql_sting = ("INSERT INTO morphology (lemma, postag, wordform, count) \n"
                             "   VALUES (\'{}\', \'{}\', \'{}\', {})"
                             "   ON CONFLICT ON CONSTRAINT morphology_pkey"
                             "   DO UPDATE SET count = {} "
                             "   RETURNING wordform ").format(lemma, postag, form, count, count)
                click.echo(sql_sting)
                cursor.execute(sql_sting)
                click.echo(cursor.fetchone()[0])
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print("Error while connecting to PostgreSQL", error)
                exit(0)
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        cursor.close()


    #closing database connection.
    if(connection):
        connection.close()
        print("PostgreSQL connection is closed")


def write2db_test():
    try:
        connection = psycopg2.connect(user = "yourdictionary",
                                      password = "DQBx5TKaD5Xe6QRi",
                                      host = "yourdictionary-dev.cqtzt424uvng.us-east-1.rds.amazonaws.com",
                                      port = "5432",
                                      database = "semantic_vectors")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print ("hello world")
        print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")
        sql_sting = ("INSERT INTO morphology (lemma, postag, wordform, count) \n"
                       "   VALUES (\'go\', \'VZB\', \'goes\', 3)"
                     "RETURNING wordform ")
        click.echo(sql_sting)
        cursor.execute(sql_sting)
        click.echo(cursor.fetchone()[0])
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

if __name__ == '__main__':
    write2db()

