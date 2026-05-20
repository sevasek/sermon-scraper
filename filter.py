# Filter - filter.py
# A function to filter the list of Sermon objects based on the Bible passage.
# Input: all Sermon objects (sermons)
# Output: only Sermon objects whose Bible passage overlaps with the given Bible passage.

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
    # Input: Two Bible passages (passage_1 and passage_2) in a list of pythonbible NormalizedReference objects.
    # Output: A boolean value indicating whether the two passages overlap (i.e., share at least one verse).
    
    verses_ids_1 = get_verses_from_reference(passage_1)
    verses_ids_2 = get_verses_from_reference(passage_2)
    
    # Find overlapping verse IDs
    overlapping = verses_ids_1.intersection(verses_ids_2)
    if len(overlapping) > 0:
        return True
    else:
        return False
    
# Main function to filter sermons by Bible passage
# Input: A list of Sermon objects (sermons) and a Bible passage (bible_passage) in string format.
# Output: A list of Sermon objects whose Bible passage overlaps with the given Bible passage.
def filter_by_bible_passage(sermons, normalised_bible_passage):
    filtered_sermons = []
    # Convert passage_1 to a list of NormalizedReference objects using bible.get_references().
    # sermon.bible_passage is already a list of NormalizedReference objects.
    # Use the is_overlapping function to check if the two passages overlap and if they do, add the sermon to the filtered_sermons list.
    passage_2 = normalised_bible_passage
    for sermon in sermons:
        passage_1 = sermon.bible_passage
        if is_overlapping(passage_1, passage_2):
            filtered_sermons.append(sermon)

    print(f"Found {len(filtered_sermons)} sermons that intersect.")
    for s in filtered_sermons:
        print(f"{s.title} by {s.speaker}")
    return filtered_sermons