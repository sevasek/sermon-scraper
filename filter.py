# Filter - filter.py
# A function to filter the list of Sermon objects based on the Bible passage.
# Input: all Sermon objects (sermons)
# Output: only Sermon objects whose Bible passage overlaps with the given Bible passage.

import pythonbible as bible

import sermons

filtered_sermons = []

def is_overlapping(passage_1, passage_2):
    # Input: a list of Sermon objects (sermons)
    # Output: a filtered list of Sermon objects (filtered_sermons) that match the given Bible passage.
    
    def get_verses_from_reference(reference_str: str):
        # 1. Convert passage text to normalized verse IDs
        normalized_references = bible.get_references(reference_str)
    
        # 2. Get every individual verse ID within the passage
        verse_ids = bible.get_verse_ids(normalized_references)
        
        return set(verse_ids)

    def find_overlapping_verses(passage_1, passage_2):
        verses1 = get_verses_from_reference(passage_1)
        verses2 = get_verses_from_reference(passage_2)
        
        # Find overlapping verse IDs
        overlapping = verses1.intersection(verses2)
        if len(overlapping) > 0:
            return True
        else:
            return False
    
    return find_overlapping_verses(passage_1, passage_2)

    # --- Example Usage ---
    passage_a = "Matthew 1:1-10"
    passage_b = "Luke 3:23-38" # Matthew and Luke overlap in the genealogy of Jesus

    overlapping_ids = find_overlapping_verses(passage_a, passage_b)

    print(f"Overlapping verse count: {len(overlapping_ids)}")
    for verse_id in overlapping_ids:
        # Convert back to standard scripture reference format
        print(bible.get_bible_book_from_verse_id(verse_id).name, bible.get_chapter_and_verse_from_verse_id(verse_id))


def filter(sermons, bible_passage):
    filtered_sermons = []
    for sermon in sermons:
        if is_overlapping(sermon.bible_passage, bible_passage):
            filtered_sermons.append(sermon)
    return filtered_sermons

return filter(sermons, bible_passage)