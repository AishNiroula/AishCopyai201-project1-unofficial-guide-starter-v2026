with open('README.md', 'r') as f:
    lines = f.readlines()

chunks_data = [
    ("admin_add_drop_deadline.txt#0", """On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other."""),
    ("course_biol_160.txt#0", """BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from."""),
    ("course_hist_118_workload.txt#0", """Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format."""),
    ("dining_pellew_dining_hall_followup.txt#0", """Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation."""),
    ("housing_innisfree_hall.txt#0", """Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter."""),
]

output = []
chunk_idx = 0
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("**Chunk") and "source: ``" in line:
        source, text = chunks_data[chunk_idx]
        output.append(f"**Chunk {chunk_idx+1}** — source: `{source}` — produced by: `chunker.py::split_documents`\n")
        output.append("\n")
        output.append("```\n")
        output.append(text + "\n")
        output.append("```\n")
        chunk_idx += 1
        i += 1
        while i < len(lines) and lines[i].strip() != "```":
            i += 1
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            output.append(lines[i])
            i += 1
        continue
    output.append(line)
    i += 1

with open('README.md', 'w') as f:
    f.writelines(output)

print(f"Updated {chunk_idx} chunks.")
