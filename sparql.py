import urllib2

# useful variables for the http request
user='student'
password='5hoPpeR4'
url='https://pgxlod.loria.fr/bigdata/namespace/kb/sparql'

# create the http request
request = urllib2.Request(url)
request.add_header('Accept', 'application/sparql-results+json')
request.add_header('Authorization', "Basic " + (user + ":" + password).encode("base64").rstrip())


def create_query(gene, medicine):
    pass

sparqlQuery='query=SELECT * { ?s ?p ?o } LIMIT 1'

# make the http request which is equivalent to : 
# curl --user student:5hoPpeR4 -v -H 'Accept:application/sparql-results+json' -X POST https://pgxlod.loria.fr/bigdata/namespace/kb/sparql --data-urlencode 'query=sparqlQuery'
result = urllib2.urlopen(url = request, data = sparqlQuery)

# print the results
print result.read()

