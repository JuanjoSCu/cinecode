# Codex integration

This fork adapts Sarp Yıldız's MIT-licensed Cinecode kit for Codex. Adaptation: JuanjoSC.
These host instructions apply to the shared Quick and Film references, including older
examples that name Claude tools. Follow the user's actual request and the host's
instructions when a reference disagrees with them.

## Tools and conversation

- Resolve `KIT` to the installed skill folder. Create each film in a separate project
  folder outside the kit.
- Use the available shell/file tools. On Windows use `python` or `py -3` if `python3`
  is unavailable. Quote paths containing spaces; use UTF-8 for project files.
- An old `Bash`, `Read`, `Grep` or `run_in_background` example describes an operation,
  not a required tool. Use the current shell, file reader, `rg`, and process/session
  handles. Poll long jobs and report progress; keep heavy GPU renders sequential.
- Ask only for missing decisions. Use `request_user_input_async` for creative
  preferences when available, or an allowed question tool following its actual schema
  and mode restrictions; otherwise ask in the final reply. A previous approval,
  complete brief or permission to decide remains valid. Do not repeat approval gates
  covered by the request, including authorization to install dependencies.
- `SendUserFile` means show the output: Codex desktop supports Markdown media embeds
  with absolute paths, for example `![Preview](/absolute/path/film.mp4)`, plus a
  clickable file link. Inspect stills before presenting them. In a text-only host,
  provide the path and say inline playback is unavailable. Do not claim to have heard
  audio if only loudness measurements were available.
- `wrap_up`, Claude's Skill tool and `mcp__ccd_session__start_session` are not Codex
  requirements. Read `SKILL.md` normally; use commentary for progress and final for
  deliveries. Never simulate a successful unavailable tool.

## Controls and validation

This installation does not register lifecycle hooks. `guard.py` and `hook.cjs` are
retained upstream utilities for Claude and regression coverage. They do not inspect
Codex conversations or enforce its gates. `usage.py` reads Claude logs, so it cannot
measure Codex tokens, budgets or costs.

The coordinator shows plans/stills before unresolved creative approvals, respects
licensed assets, records decisions in `STATE.md`, and preserves project boundaries.
Render checks still run through `make.py`, `qc.py`, `words_check.py`,
`validate_shots.py` and deterministic capture. Diagnose and fix failed checks;
do not bypass them because chat hooks are absent. Inspect rendered stills and
probe the resulting MP4, including audio streams and duration.

## Subagents and models

Delegate independent tasks only when there is a clear benefit. Give each helper file
ownership, input files and completion criteria; tell it others may be working and
not to revert their changes. Use `brief.py` for a film helper's rules. Scripts handle
mechanical checks without a helper.

Check model names printed by `brief.py` against those actually exposed by the host.
Prefer `gpt-6-luna` at low or medium effort for bounded routine work, `gpt-6-sol` for
more complex work, and `gpt-6-astra` for high uncertainty. Respect explicit choices
and fixed-role models. If a suggestion is unavailable, use an appropriate available
model or do the task in the main chat; never invent availability. For `inherit`, omit
the override. If the host requires a fresh-context fork for an override, supply all
necessary context in its task message. Report participating helpers and their work;
include model and effort only when confirmed by the environment.

## Resume and update

Update `STATE.md` throughout the work. Continue the current chat after compaction.
Create another chat only if the user explicitly requests or accepts it; discover an
available Codex chat tool then pass the film folder and resume prompt. If unavailable,
`python tools/handoff.py --lang es --dry-run` prints a portable instruction. The
script does not create a Codex chat.

Use this fork for updates: `https://github.com/JuanjoSCu/cinecode`.

- Git installation: inspect status and remotes, then use `git -C KIT pull --ff-only`
  from the fork when clean. Preserve local edits; never reset them away.
- Download installation: there is no `.git`. Fetch the fork into a staging folder
  with Codex's skill-installer, validate it, preserve the old folder outside skill
  discovery as a backup, and replace only this skill. Do not run `git pull` against
  a download or create two discoverable copies.
- `init_film.py <film> --update-tools` refreshes copied tools and managed instructions
  without replacing the film's authored content.

See [OpenAI's migration guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin#review-what-openai-supports)
for provider-specific instructions. This is a local skill installation, not a
public plugin-directory submission.
