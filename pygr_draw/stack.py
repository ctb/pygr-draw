"""
Code for stacking annotations so that they don't overlap.

"""

def sort_by_length(a, b):
    return -cmp(len(a.sequence), len(b.sequence))

def sort_by_name(a, b):
    return cmp(a.name, b.name)

def stack_annotations(seq, nlmsa, sort_annotations_by=sort_by_length):
    slots_d = {}

    # get a list of all annotations on this sequence.
    annotations = list(nlmsa[seq])

    if sort_annotations_by:
        annotations.sort(sort_annotations_by) # e.g. length

    for annotation in annotations:
            
        assert not slots_d.has_key(annotation.id)

        subseq = annotation.sequence

        overlapping = nlmsa[subseq]
        assert len(overlapping) > 0, "must overlap with itself!?"

        slot = 0

        if len(overlapping) > 1:
            # find the slot (vertical offsets) of all overlapping annots
            slot_list = set()

            for overlap in overlapping:
                assigned_slot = slots_d.get(overlap.id)

                if assigned_slot != None:
                    slot_list.add(assigned_slot)

            # have some slots already assigned? find first unassigned one
            first_available_slot = 0
            if slot_list:
                slot_list = list(slot_list)
                slot_list.sort()

                for i, j in zip(slot_list, range(len(slot_list))):
                    if i != j:
                        # unassigned slot in middle of slots list
                        first_available_slot = j
                        break
                else:
                    # slot list all full up; go one more
                    first_available_slot = len(slot_list)
                    
            # ta-da!
            slot = first_available_slot

        # save in dictionary
        slots_d[annotation.id] = slot

    return slots_d

