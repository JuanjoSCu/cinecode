# Handoff

## Before resuming

- Update `STATE.md`: current phase, approved choices, open notes and next action.
- Save user notes verbatim in `notes/round-N.md`.
- Record running jobs with their command, status file and log.
- Save the text snapshot with `python tools/snapshot.py "handoff"`.

## Continue the work

Continue in the current Codex chat unless the user explicitly asks for or accepts a
new one. Context compaction is not a request for another chat. When a new chat is
requested, use the available Codex chat tool with the film folder and this prompt,
translated into the user's language:

> Continue from STATE.md. Read the Cinecode SKILL.md referenced in AGENTS.md and its
> Codex integration reference. Refresh copied tools with
> `python KIT/scripts/init_film.py . --update-tools`. Read STATE.md and only the files
> it names, preserve the approved choices, and carry out the next action.

If no chat tool is available, provide the absolute film path and this prompt.
`python tools/handoff.py --lang es --dry-run` prints the resume instruction; it does
not create a chat. Never report that a chat started unless a tool confirms it.

## For the resumed chat

Read the skill, refresh tools, then read `STATE.md` first. Continue from its next
action without asking again about choices or authorizations already recorded.
