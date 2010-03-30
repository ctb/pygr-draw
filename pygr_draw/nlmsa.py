"""
Library for taking lists/dicts of sequence annotations and creating an NLMSA.

"""

from pygr import cnestedlist, seqdb

def create_annotation_map(annotations, sequence_db):
    """
    Given annotations list/dict & a sequence db (BlastDB),
    construct an NLMSA/annotations map connecting the annotations
    with the sequence(s).

    If annotations is a dict, it's used to construct an AnnotationDB
    directly; if it's a list, it's converted into an in-memory dict
    first.  This Has Scalability Implications: don't do this for
    20m annotations; use a shelve-db instead!
    
    """

    try:
        annotations.keys()
    except AttributeError:
        # assume annotations is a list! convert to a dict => AnnotationDB.
        d = {}
        for n, a in enumerate(annotations):
            d[n] = a

        annotations = d
    
    annotations_map = cnestedlist.NLMSA('test', mode='memory',
                                        pairwiseMode=True)

    annotation_db = seqdb.AnnotationDB(annotations, sequence_db)
    for v in annotation_db.itervalues():
        annotations_map.addAnnotation(v)

    annotations_map.build()

    return annotations_map
