import urllib2

from recup_tsv import is_associated_91_91, is_associated_91_182, is_associated_test

# useful variables for the http request
user = 'student'
password = '5hoPpeR4'
url = 'https://pgxlod.loria.fr/bigdata/namespace/kb/sparql'

# create the http request
request = urllib2.Request(url)
request.add_header('Accept', 'application/sparql-results+json')
request.add_header('Authorization', "Basic " + (user + ":" + password).encode("base64").rstrip())


def create_query(gene, medicine):
    query = """
query=PREFIX atc: <http://bio2rdf.org/atc:>
PREFIX bio2rdfv: <http://bio2rdf.org/bio2rdf_vocabulary:>
PREFIX clinvar: <http://bio2rdf.org/clinvar:>
PREFIX clinvarv: <http://bio2rdf.org/clinvar_vocabulary:>
PREFIX dbv: <http://bio2rdf.org/drugbank_vocabulary:>
PREFIX disgenet: <http://rdf.disgenet.org/resource/gda/>
PREFIX drugbank: <http://bio2rdf.org/drugbank:>
PREFIX mapping: <http://biodb.jp/mappings/>
PREFIX medispan: <http://orpailleur.fr/medispan/>
PREFIX ncbigene: <http://bio2rdf.org/ncbigene:>
PREFIX pharmgkb: <http://bio2rdf.org/pharmgkb:>
PREFIX pharmgkbv: <http://bio2rdf.org/pharmgkb_vocabulary:>
PREFIX pubchemcompound: <http://bio2rdf.org/pubchem.compound:>
PREFIX sider: <http://bio2rdf.org/sider:>
PREFIX siderv: <http://bio2rdf.org/sider_vocabulary:>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX so: <http://bio2rdf.org/sequence_ontology:>
PREFIX umls: <http://bio2rdf.org/umls:>
PREFIX uniprot: <http://bio2rdf.org/uniprot:>


CONSTRUCT {}
WHERE {pharmgkb:%(medicine)s pharmgkbv:x-drugbank ?drug2.
       pharmgkb:%(medicine)s pharmgkbv:x-umls ?cui.
       pharmgkb:%(medicine)s pharmgkbv:x-pubchemcompound ?compound.
       ?drug3 siderv:pubchem-flat-compound-id ?compound.
       ?drug_target dbv:drug ?drug2.
       ?drug_target dbv:action ?action.
       ?drug2 dbv:x-pubchemcompound ?compound.
       ?drug2 dbv:x-atc ?atc.
       ?drug_target dbv:target ?target.
       ?target dbv:x-uniprot ?prot.
       pharmgkb:%(gene)s pharmgkbv:x-uniprot ?prot.
       pharmgkb:%(gene)s pharmgkbv:x-ncbigene ?gene.
       ?gene2 clinvarv:x-gene ?gene.
       ?gene2 clinvarv:x-sequence_ontology ?so.
       ?rcv clinvarv:Variant_Gene ?gene2.
       ?rcv clinvarv:Variant_Phenotype ?x.
       ?x clinvarv:x-medgen ?disease2.
       ?gene bio2rdfv:x-identifiers.org ?gene3.
       ?var sio:SIO_000628 ?gene3.
       ?var sio:SIO_000628 ?disease.
       ?gene3 sio:SIO_000062 ?react.
       ?disease sio:SIO_000095 ?mesh.
       ?disease sio:SIO_000008 ?semantic_type.
       ?disease skos:exactMatch ?disease2.
       ?drug3 siderv:side-effect ?disease3.
       ?disease skos:exactMatch ?disease3.
       ?disease4 mapping:medispan_to_sider ?disease3.
       ?disease2 mapping:clinvar_to_sider ?disease3.
       ?disease2 mapping:clinvar_to_medispan ?disease4.
      }
    """ % {'gene': gene, 'medicine': medicine}

    return query

# make the http request which is equivalent to : 
# curl --user student:5hoPpeR4 -v -H 'Accept:application/sparql-results+json' -X POST https://pgxlod.loria.fr/bigdata/namespace/kb/sparql --data-urlencode 'query=sparqlQuery'
i = 1
for (gene, medicine) in is_associated_91_91:
    print '============== Iteration %(i)d ==============' % {'i': i}
    print 'gene =', gene, ', medicine =', medicine
    query = create_query(gene, medicine)
    print query
    result = urllib2.urlopen(url=request, data='query=SELECT * { ?s ?p ?o } LIMIT 1')
    print result.read()
    #result = urllib2.urlopen(url=request, data=query)
    print "request successful"
    #destination = open("graphes/%s-%s.py" % (gene, medicine), "w")
    #destination.write("graph = %s" % result.read())
    #destination.close()
    #result.close()
    #i += 1
    break
