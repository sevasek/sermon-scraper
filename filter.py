# Filter - filter.py

import pythonbible as bible

def get_verses_from_reference(normalized_references):
    
    # Return an empty set if input is null
    if not normalized_references:
        return set()
    
    # If it's a list flatten it
    if isinstance(normalized_references, list):
        verse_ids = []
        for ref in normalized_references:
            verse_ids.extend(bible.convert_reference_to_verse_ids(ref))
        return set(verse_ids)
    # Single reference
    else:
        return set(bible.convert_reference_to_verse_ids(normalized_references))

def is_overlapping(passage_1, passage_2):

    verses_ids_1 = get_verses_from_reference(passage_1)
    verses_ids_2 = get_verses_from_reference(passage_2)
    
    # Find overlapping verse IDs
    overlapping = verses_ids_1.intersection(verses_ids_2)
    if len(overlapping) > 0:
        return True
    else:
        return False
    
def filter_by_bible_passage(sermons, normalised_bible_passage):
    filtered_sermons = []
    passage_2 = normalised_bible_passage
    for sermon in sermons:
        passage_1 = sermon.bible_passage
        if is_overlapping(passage_1, passage_2):
            filtered_sermons.append(sermon)

    print(f"Found {len(filtered_sermons)} sermons that intersect.")
    for s in filtered_sermons:
        print(f"{s.title} by {s.speaker}")
    return filtered_sermons