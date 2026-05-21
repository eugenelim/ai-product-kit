# Contributing

Thanks for being here.

## For agents (Claude Code, Cursor, Codex, Gemini CLI, Copilot)

Read [`AGENTS.md`](AGENTS.md) first. `CLAUDE.md` is a symlink to it.

For any work beyond a one-line edit, follow the [work-loop](.claude/skills/work-loop/SKILL.md) and the spec/plan discipline in [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md).

## For humans

The ordered build queue is in [`ROADMAP.md`](ROADMAP.md). Pick the lowest-numbered open item.

Quick reference:

1. **What is this kit?** → [`docs/CHARTER.md`](docs/CHARTER.md)
2. **How does work happen?** → [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md)
3. **What's the build queue?** → [`ROADMAP.md`](ROADMAP.md)
4. **How do I scaffold a new component?** → `tools/new-spec.sh <slug>`
5. **How do I check my work?** → `tools/pre-pr.sh`

## The minimum bar for a PR

- [ ] Spec under `docs/specs/<feature>/spec.md` (use `tools/new-spec.sh`)
- [ ] Plan under `docs/specs/<feature>/plan.md`
- [ ] `tools/pre-pr.sh` returns clean
- [ ] If the change adds a new component, `docs/INVENTORY.md` has a new row
- [ ] If the change is structural (new top-level dir, new ontology type, new phase), an RFC under `docs/rfc/` exists and is accepted
- [ ] Commit message follows conventional commits with a `Spec:` footer
- [ ] The corresponding ROADMAP.md item is checked

## Conventions, in one paragraph

Markdown with YAML frontmatter for everything that isn't code. Kebab-case filenames. ISO dates for temporal files. Every artifact declares `object_type:` per the ontology in [`context/frameworks/ontology.md`](context/frameworks/ontology.md). Every artifact with `human_approval_required: true` has a non-empty `human_owned_decisions:` list. The audits will check these mechanically.

## When in doubt

Open an RFC in `docs/rfc/`. Quiet deviation is how the convention layer rots.
