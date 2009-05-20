from pygr import cnestedlist, seqdb

def create_annotation_map(annotations, sequence_db):
    """
    Given annotations dictionary & a sequence db (BlastDB),
    construct an NLMSA/annotations map connecting the annotations
    with the sequence(s).
    """
    annotations_map = cnestedlist.NLMSA('test', mode='memory',
                                        use_virtual_lpo=True)

    annotation_db = seqdb.AnnotationDB(annotations, sequence_db)
    for v in annotation_db.values():
        annotations_map.addAnnotation(v)

    annotations_map.build()

    return annotations_map
