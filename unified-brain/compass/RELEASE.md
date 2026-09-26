# Release checklist

A local candidate is not a public release. Never archive the working vault directly and never run the full template verifier against it.

## Automated preparation

The repository is maintainer source, not an already-built distribution. Keep the reviewed files in `scripts/template/defaults/` under version control. The builder requires them to replace personal configuration, planning, tasks, and knowledge state. Never populate these defaults from a personal vault.

CI runs the application and release-safety contracts, builds a fresh candidate outside the checkout, verifies its exact manifest, and checks disposable archive extraction. The generated `MANIFEST.sha256`, workspace state, ZIP, and checksum are build outputs, not source files to commit. CI does not establish native acceptance or publish a release.

1. Run `node scripts/verify_life_os_app.mjs .`, `node scripts/verify_assistant_contracts.mjs .`, and `python3 scripts/verify_release_safety.py`.
2. Choose an explicit version and a fresh output name outside the working vault. Existing destinations and archives are refused.
3. Build a sanitized local candidate:

```bash
python3 scripts/build_template.py --out ../life-os-releases --name LifeOS-1.1.0-candidate --version 1.1.0 --zip
```

4. Inspect the candidate's embedded `MANIFEST.sha256` and the archive's full `.sha256` sidecar. Verify archive contents and paths, not only its filename.
   Run `python3 scripts/verify_archive_restore.py /absolute/path/to/candidate.zip` to validate the sidecar, reject unsafe archive entries, extract into a disposable directory, and compare every restored file with the embedded manifest. This does not restore or test a personal vault.
5. Keep each flavor in its own fresh destination. The without-reading variant needs separate functional acceptance; do not assume removing a folder leaves all commands valid.

Raw plugin settings are never copied to staging. The builder reconstructs allowlisted settings first, strips machine-local state, and uses private staging. Unknown plugin settings are omitted. This favors safe defaults over preserving every customization.

Files covered by reviewed defaults are skipped before copying. Canonical project and writing boards are rebuilt empty, without reading their live cards or lane names. Other personal boards receive no filename-based exemption. Planning, task, and knowledge-layer personal state comes only from reviewed defaults. Desktop metadata and local agent directories are excluded; core appearance and webviewer state are reset. Review functional behavior after these resets, especially capture and board creation. A passing scan is not proof that every allowed source file has been manually reviewed.

## Human review before distribution

- Review the exact archive for private data, example labeling, source paths, and unexpected files. The machine-local working vault is not the review target.
- Check README, CHANGELOG, application manifest, notices, and candidate version metadata agree. Old 1.0.2 archives are not current Life OS candidates.
- Verify upstream binary provenance and license requirements separately. Kanban's bundled license is GPL-3.0, not MIT. Presence of a LICENSE file alone is not a completed redistribution review.
- Local REST API remains enabled over loopback HTTP in the package policy. Changing that default requires an explicit decision. Verify actual listener behavior in the isolated native test.
- Complete `Guide/23 Native Acceptance.md` against the archive checksum. Record desktop-native, mobile, provider, and MCP outcomes separately.
- Do not claim a provider is connected or a backup is recoverable without testing it.
- Commit, push, release creation, and publication require separate authorization.

## Upgrade and rollback

There is no in-place updater. Close Obsidian, back up the complete old vault, and extract the new candidate alongside it. Migrate personal content, custom configuration, and templates with conflict review. Do not copy the old or new `.obsidian` directory wholesale. Test restoring the backup before retiring any old copy. No archive cleanup or retirement is automatic.

## Current acceptance boundary

Synthetic tests exercise parser logic, controls, and packaging safety without personal notes or provider calls. They do not establish native Obsidian acceptance. Keep every unrun check marked not tested.
