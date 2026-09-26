# Contributing

Thanks for helping grow this list! This is a curated, *awesome*-style list of
Obsidian vaults and Markdown knowledge bases.

## Quick start

- **Easiest:** open a [Suggest a vault](https://github.com/obsidian-pkm-vault/awesome-obsidian-vault/issues/new/choose) issue.
- **Faster:** open a pull request that edits `README.md` directly.

## Adding a vault

All vaults live in the main table in `README.md`. Add one row:

```
| Category | Name — author | [vault](https://...) | [web](https://...) |   |
```

Rules:

1. **Category** — reuse an existing category if one fits. Keep rows for the
   same category grouped together.
2. **Name — author** — use an em dash (`—`) between the title and the
   author/handle. Single spaces only.
3. **vault** — link to the source (usually a Git repo). Use `N/A` if there is
   no downloadable vault.
4. **web** — link to the published site. Use `N/A` if there is none.
5. **✨ column** — leave it blank. Maintainers add ✨ to mark a *standout pick*:
   a vault that is especially polished, complete, or widely used. Make your
   case for it in the PR/issue description.
6. **Counts** — if you add or remove rows, update the number in the section
   heading (e.g. `## Table ... (48)`).

## What belongs here

- Markdown-based vaults / knowledge bases, ideally Obsidian-compatible.
- Content that is publicly accessible (a repository or a live site).

Output from static-site generators (Hugo, Quartz, etc.) is welcome — note that
the syntax may not be 100% Obsidian-compatible, as mentioned in the README.

## Automated checks

A weekly GitHub Action checks every link in the repo with
[lychee](https://github.com/lycheeverse/lychee). Broken links open an issue
automatically, so please make sure links you add resolve correctly.

## License

By contributing, you agree that your contributions are dedicated to the public
domain under [CC0 1.0](LICENSE).
