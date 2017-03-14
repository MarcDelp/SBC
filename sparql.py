import urllib2
from time import sleep

from recup_tsv import is_associated_91_91, is_associated_91_182, is_associated_test

url = 'http://localhost:9999/blazegraph/namespace/kb/sparql'

# create the http request
request = urllib2.Request(url)
request.add_header('Accept', 'application/sparql-results+json')

def create_query(gene, medicine):
	query = """query=PREFIX atc: <http://bio2rdf.org/atc:>
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

		SELECT *
		WHERE {
			OPTIONAL {
				pharmgkb:%(gene)s pharmgkbv:x-uniprot ?uniprot_gene.
				?drugbank_gene dbv:x-uniprot ?uniprot_gene.

				OPTIONAL {
					?relation dbv:target ?drugbank_gene.
					BIND ("target" as ?gene_relation).
				}

				OPTIONAL {
					FILTER(!BOUND(?gene_relation)).
					?relation dbv:carrier ?drugbank_gene.
					BIND ("carrier" as ?gene_relation).
				}

				OPTIONAL {
					FILTER(!BOUND(?gene_relation)).
					?relation dbv:enzyme ?drugbank_gene.
					BIND ("enzyme" as ?gene_relation).
				}

				OPTIONAL {
					FILTER(!BOUND(?gene_relation)).
					?relation dbv:transporter ?drugbank_gene.
					BIND ("transporter" as ?gene_relation).
				}

				FILTER(BOUND(?gene_relation)).
				?relation dbv:drug ?drugbank_drug.

				OPTIONAL {
					pharmgkb:%(medicine)s pharmgkbv:x-drugbank ?drugbank_drug.
					BIND("found" as ?drug_path).
				}

				OPTIONAL {
					FILTER(! BOUND(?drug_path)).
					pharmgkb:%(medicine)s pharmgkbv:x-pubchemcompound ?compound.
					?drugbank_drug dbv:x-pubchemcompound ?compound.
					BIND("found" as ?drug_path).
				}

				OPTIONAL {
					FILTER(! BOUND(?drug_path)).
					pharmgkb:%(medicine)s pharmgkbv:x-pubchemcompound ?compound.
					?drugbank_drug dbv:x-pubmedchemcompound ?compound.
					BIND("found" as ?drug_path).
				}

				OPTIONAL {
					FILTER(! BOUND(?drug_path)).
					?drugbank_drug dbv:x-pharmgkb pharmgkb:%(medicine)s.
					BIND("found" as ?drug_path).
				}

				FILTER(BOUND(?drug_path)).
				BIND("true" as ?done).
			}

			OPTIONAL {
				FILTER(! BOUND(?done)).

				pharmgkb:%(gene)s pharmgkbv:x-ncbigene ?clinvar_gene.
				?gene_variant clinvarv:x-gene ?clinvar_gene.
				?clinvar_variant clinvarv:Variant_Gene ?gene_variant.
				?clinvar_variant clinvarv:Variant_Phenotype/clinvar:x-medgen ?clinvar_disease.

				OPTIONAL {
					pharmgkb:%(medicine)s pharmgkbv:umls ?medispan_ingredient.
					?medispan_drug mapping:medispan_to_umls ?medispan_ingredient.

					OPTIONAL {
						?medispan_drug medispan:indication ?medispan_disease.
						BIND("found" as ?medispan_path).
					}

					OPTIONAL {
						FILTER(!BOUND(?medispan_path)).
						?medispan_drug medispan:side_effect ?medispan_disease.
						BIND("found" as ?medispan_path).
					}

					FILTER(BOUND(?medispan_path)).

					OPTIONAL {
						?clinvar_disease mapping:clinvar_to_medispan ?medispan_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?clinvar_disease mapping:clinvar_to_sider ?sider_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?disgenet_disease skos:exactMatch ?medispan_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?disgenet_disease skos:exactMatch ?sider_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					FILTER(BOUND(?disease_path)).
				}

				OPTIONAL {
					FILTER(!BOUND(?disease_path)).

					pharmgkb:%(medicine)s pharmgkbv:x-pubchemcompound ?pubchem_compound.
					?sider_drug siderv:pubchem-flat-compound-id ?pubchem_compound.

					OPTIONAL {
						?sider_drug siderv:indication ?sider_disease.
						BIND("found" as ?sider_path).
					}

					OPTIONAL {
						FILTER(!BOUND(?sider_path)).
						?sider_drug siderv:side_effect ?sider_disease.
						BIND("found" as ?sider_path).
					}

					FILTER(BOUND(?sider_path)).

					OPTIONAL {
						?clinvar_disease mapping:clinvar_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?clinvar_disease mapping:clinvar_to_medispan ?medispan_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?disgenet_disease skos:exactMatch ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?disgenet_disease skos:exactMatch ?medispan_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					FILTER(BOUND(?disease_path)).
				}

				FILTER(BOUND(?disease_path)).
				BIND("true" as ?done).
			}

			OPTIONAL {
				FILTER(! BOUND(?done)).

				pharmgkb:%(gene)s pharmgkbv:x-ncbigene ?clinvar_gene.
				?clinvar_gene bio2rdfv:x-identifiers.org ?disgenet_gene.
				?disgenet_variant sio:SIO_000628 ?disgenet_gene.
				?disgenet_variant sio:SIO_000628 ?disgenet_disease.

				OPTIONAL {
					pharmgkb:%(medicine)s pharmgkbv:umls ?medispan_ingredient.
					?medispan_drug mapping:medispan_to_umls ?medispan_ingredient.

					OPTIONAL {
						?medispan_drug medispan:indication ?medispan_disease.
						BIND("found" as ?medispan_path).
					}

					OPTIONAL {
						FILTER(!BOUND(?medispan_path)).
						?medispan_drug medispan:side_effect ?medispan_disease.
						BIND("found" as ?medispan_path).
					}

					FILTER(BOUND(?medispan_path)).

					OPTIONAL {
						?disgenet_disease skos:exactMatch ?medispan_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?clinvar_disease mapping:clinvar_to_medispan ?medispan_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?sider_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?clinvar_disease mapping:clinvar_to_sider ?sider_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					FILTER(BOUND(?disease_path)).
				}

				OPTIONAL {
					FILTER(!BOUND(?disease_path)).

					pharmgkb:%(medicine)s pharmgkbv:x-pubchemcompound ?pubchem_compound.
					?sider_drug siderv:pubchem-flat-compound-id ?pubchem_compound.

					OPTIONAL {
						?sider_drug siderv:indication ?sider_disease.
						BIND("found" as ?sider_path).
					}

					OPTIONAL {
						FILTER(!BOUND(?sider_path)).
						?sider_drug siderv:side_effect ?sider_disease.
						BIND("found" as ?sider_path).
					}

					FILTER(BOUND(?sider_path)).

					OPTIONAL {
						?disgenet_disease skos:exactMatch ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?medispan_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?clinvar_disease mapping:clinvar_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					OPTIONAL {
						FILTER(! BOUND(?disease_path)).
						?disgenet_disease skos:exactMatch ?clinvar_disease.
						?clinvar_disease mapping:clinvar_to_medispan ?medispan_disease.
						?medispan_disease mapping:medispan_to_sider ?sider_disease.
						BIND("found" as ?disease_path).
					}

					FILTER(BOUND(?disease_path)).
				}

				FILTER(BOUND(?disease_path)).
				BIND("true" as ?done).
			}
		}
    """ % {'gene': gene, 'medicine': medicine}

    return query


i = 1
passed = []
for (gene, medicine) in is_associated_91_91:
    print '============== Iteration %(i)d ==============' % {'i': i}
    print 'gene =', gene, ', medicine =', medicine
    try:
        query = create_query(gene, medicine)
        result = urllib2.urlopen(url=request, data=query)
        print "request successful"
        destination = open("graphes/%s-%s.py" % (gene, medicine), "w")
        destination.write("graph = %s" % result.read())
        destination.close()
        result.close()
        i += 1
        sleep(10)
    except Exception:
	print "request failed"
        passed.append(i)
        i += 1

for (gene, medicine) in is_associated_91_182:
    print '============== Iteration %(i)d ==============' % {'i': i}
    print 'gene =', gene, ', medicine =', medicine
    try:
        query = create_query(gene, medicine)
        result = urllib2.urlopen(url=request, data=query)
        print "request successful"
        destination = open("graphes/%s-%s.py" % (gene, medicine), "w")
        destination.write("graph = %s" % result.read())
        destination.close()
        result.close()
        i += 1
        sleep(10)
    except Exception:
	print "request failed"
        passed.append(i)
        i += 1

for (gene, medicine) in is_associated_test:
    print '============== Iteration %(i)d ==============' % {'i': i}
    print 'gene =', gene, ', medicine =', medicine
    try:
        query = create_query(gene, medicine)
        result = urllib2.urlopen(url=request, data=query)
        print "request successful"
        destination = open("graphes/%s-%s.py" % (gene, medicine), "w")
        destination.write("graph = %s" % result.read())
        destination.close()
        result.close()
        i += 1
        sleep(10)
    except Exception:
	print "request failed"
        passed.append(i)
        i += 1

print i, passed
