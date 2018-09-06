from . import get_page

frontier_q = ['']
visited_q = []

while len(frontier_q) > 0:
    current_url = frontier_q[0]
    frontier_q = frontier_q[1:]
    visited_q.append(current_url)

    text = get_page(current_url)
    extracted_links = link_parser(text)

    for link in extracted_links:
        if link not in frontier_q and link not in visited_q:
            frontier_q.append(link)
