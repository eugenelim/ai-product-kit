# Per-command spec checklist

Editorial guidance for F4 fan-out workers. When you author the per-command spec
under `docs/specs/cmd-<verb>/spec.md` for one of the seven in-scope Phase-4
template-fill commands (`/draft-vision`, `/draft-initiative`, `/context-map`,
`/end-to-end-flow`, `/sequence-initiative`, `/draft-spec`, `/handoff-packet`),
walk this list before declaring the spec ready for adversarial review. The
list is not machine-checked beyond a count assertion (T12b in the parent
spec's contract tests); it exists so the convention's surface stays consistent
across the seven specs without each author re-deriving it.

Read alongside `docs/CONVENTIONS.md` §"Phase-4 Template-Fill Commands —
`.claude/commands/draft-*.md` and siblings", which is the canonical contract.
This page restates that contract as an authoring checklist.

## Checklist

- [ ] **Cites the convention as `Constrained by:`.** The per-command spec's
  header bullet block names
  `docs/specs/phase-4-command-convention/spec.md` in its `Constrained by:`
  line, exactly as F3 per-template specs cite
  `template-authoring-convention`. Any deviation from the convention is
  surfaced here with a one-line "deviates from §X for reason Y" note, not
  silently absorbed.

- [ ] **Names the template path consumed (creating) OR the augmented child
  file path (augmenting).** For artifact-creating commands (`/draft-vision`,
  `/draft-initiative`, `/draft-spec`, `/handoff-packet`), name the
  `templates/<path>` the command copies — single-file `.md` or folder. For
  artifact-augmenting commands (`/context-map`, `/end-to-end-flow`,
  `/sequence-initiative`), name the child file inside
  `templates/initiative/` whose body the command will walk in-place within
  the existing initiative folder.

- [ ] **Names the destination write path (creating) OR confirms the parent
  initiative folder pre-exists (augmenting).** Creating commands name the
  exact destination under `delivery/` (e.g.,
  `delivery/visions/<slug>.md`,
  `delivery/initiatives/<slug>/`,
  `delivery/initiatives/<initiative-slug>/specs/<spec-slug>/`,
  `delivery/handoff-packets/<slug>/`). Augmenting commands declare the
  pre-existing folder
  `delivery/initiatives/<initiative-slug>/` as a hard pre-condition (Step 1
  exits code 2 if missing) and name the specific child file path the command
  fills.

- [ ] **Declares the parent-artifact-resolution rule.** Creating commands
  state which family directory holds candidate parents (e.g.,
  `validation/learnings/` for `/draft-vision`,
  `delivery/visions/` for `/draft-initiative`,
  `delivery/initiatives/<initiative-slug>/` for `/draft-spec`,
  `delivery/initiatives/<initiative-slug>/` for `/handoff-packet`), which
  `status:` values gate inclusion in the candidate list (terminal-or-killed
  set per the convention), and the exact remediation message emitted when
  the candidate list is empty. Augmenting commands explicitly skip this
  section (no resolution; the parent is the initiative folder named by the
  positional).

- [ ] **Enumerates the per-section interactive prompts with the human-facing
  copy.** For each H2 (and each H3 within an H2) of the template body or
  child file, name the question the command will ask the human, in the
  exact phrasing the command emits. This forces the spec to make the
  "one question at a time, never batch" rule concrete instead of abstract;
  it also makes the per-command adversarial review tractable (the reviewer
  reads the prompts and judges whether they elicit the right field). For
  long templates, group prompts by H2 with a sub-heading per H2 inside
  this section of the spec.
