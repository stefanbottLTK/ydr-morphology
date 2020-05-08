import psycopg2
import json

def get_form_from_db(event, context):
    event_body = json.loads(event['body'])
    lemma = (event_body['lemma'])
    pos = (event_body['pos'])
    passw = (event_body['pass'])
    results_list = []
    try:
        connection = psycopg2.connect(user = "yourdictionary",
                                      password = passw,
                                      host = "yourdictionary-dev.cqtzt424uvng.us-east-1.rds.amazonaws.com",
                                      port = "5432",
                                      database = "semantic_vectors")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        # print ("hello world")
        # print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        # cursor.execute("SELECT version();")
        # record = cursor.fetchone()
        # print("You are connected to - ", record,"\n")
        print("")
        sql_sting = (f"SELECT wordform FROM morphology WHERE lemma='{lemma}' and postag='{pos}' ")
        print(sql_sting)
        cursor.execute(sql_sting)
        # print(cursor.fetchone()[0])
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            # print(row[0] + "\t..")
            this_result = {"form" : row[0]}
            results_list.append(this_result)
        print("")
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                # print("PostgreSQL connection is closed")

    response = {
        'statusCode': 200,
        'body': json.dumps(results_list)
    }
    return response


def get_analyisis_from_db(event, context):
    event_body = json.loads(event['body'])
    form = event_body['form']
    passw = (event_body['pass'])
    results_list = []

    try:
        connection = psycopg2.connect(user = "yourdictionary",
                                      password = passw,
                                      host = "yourdictionary-dev.cqtzt424uvng.us-east-1.rds.amazonaws.com",
                                      port = "5432",
                                      database = "semantic_vectors")

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        # print ("hello world")
        # print ( connection.get_dsn_parameters(),"\n")
        # Print PostgreSQL version
        # cursor.execute("SELECT version();")
        # record = cursor.fetchone()
        # print("You are connected to - ", record,"\n")
        print("")
        sql_sting = (f"SELECT lemma, postag FROM morphology WHERE wordform='{form}' ")
        print(sql_sting)
        cursor.execute(sql_sting)
        rows = cursor.fetchall()
        print(rows)
        for row in rows:
            # print(row[0] + "\t..")
            this_result = {"pos" : row[1], "lemma" : row[0]}
            results_list.append(this_result)
        print("")
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                # print("PostgreSQL connection is closed")

    response = {
        'statusCode': 200,
        'body': json.dumps(results_list)
    }
    return response


def morphology(pos,lemma,form):
    if (pos is not None) and (lemma is not None):
        get_form_from_db(lemma, pos)
    elif (form is not None):
        get_analyisis_from_db(form)
    else:
        print("either specify a word form or a pair of lemma-and-POS-tag")




if __name__ == '__main__':
    morphology()
