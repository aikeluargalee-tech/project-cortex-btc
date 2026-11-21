##### PROJECT CORTEX-BTC — 00J: HARDWARE WALLET SECURITY, CUSTODY HARDENING & FIRMWARE AUDIT LEDGER
**Status:** Living Hardware Custody & Security Reference Ledger (Dedicated to Cold Storage, Multi-Sig Quorum, Firmware/Bootloader Audits & Anti-Tamper Defense)
**Last Updated:** Thursday, 19 November 2026 — 11:36 UTC (19:36 MYT / UTC+8)
**Governance Scope:** Dedicated Hardware Wallet & Self-Custody Reference Ledger (Cross-Linked to MOD 32 & MOD 65). Tracks hardware wallet threat vectors, cryptographic verification rules, multi-sig recovery hygiene, and firmware release audits without altering Pillar 1–5 market execution formulas.

---

###### 0. Machine-Readable Ledger Header (NotebookLM / Python Index)
```yaml
ledger_id: "00J"
entry_type: "HARDWARE_WALLET_SECURITY_AND_CUSTODY_LEDGER"
last_updated_utc: "2026-11-19T11:36:00Z"
last_updated_myt: "2026-11-19 19:36 MYT"
custody_architecture: "2-of-3 Multi-Vendor Hardware Quorum (Malaysia / Indonesia Jurisdiction Split)"
entropy_standard: "Offline Physical Dice-Roll Entropy + Output Descriptor & Seed/Steel Backup"
firmware_policy: "Targeted Security/Critical Updates Only + Offline GPG/SHA-256 Verification"
```

---

###### 1. Core Hardware Wallet Security Pillars & Operational Rules (MOD 32 / MOD 65 Bridge)
* **Multi-Vendor 2-of-3 Quorum & Jurisdictional Split:** Avoid single-vendor monoculture risk across devices (e.g., Coldcard, BitBox02 / BitBox02 Nova, Keystone). Keep keys distributed across the **Malaysia / Indonesia** dual-jurisdiction layout with full output-descriptor backups stored separately from seed/passphrase material so funds can be recovered even if a single vendor's tooling or companion app is compromised.
* **Offline Entropy & Zero Trust in Vendor RNG:** Generate seed entropy offline via physical dice rolls rather than trusting a single device or host RNG alone; back up seeds on durable steel / offline media without ever typing recovery words or passphrases into any computer, phone, browser, website, or AI prompt.
* **Selective Firmware Updates & Cryptographic Verification:** Treat firmware updates as high-risk operational events rather than routine auto-installs—update only when addressing genuine security/critical fixes or required features, and always verify developer **GPG signatures** and **SHA-256 checksums** offline before flashing.
* **Never Trust Host UI / Clipboard / Companion Apps Alone:** Always verify receiving addresses, change outputs, transaction fees, and swap/refund terms directly on hardware screens (and across independent screens where applicable), while enforcing hardware-locked exchange withdrawal whitelists and strict single-use address hygiene (no address reuse).

---

###### 2. Firmware & Vulnerability Audit Log (2026 Hardware Security Entries)
* **BitBox `11.2026` ("Cresta") Release Audit (Nov 19, 2026):**
  * **Bootloader Downgrade Protection:** Fixes a bootloader issue where a precisely timed power loss while saving settings could lower the minimum accepted firmware version if an attacker also held physical/bootloader access and power control. Includes a bootloader upgrade (expect multiple progress bars during installation).
  * **Transaction Fee Validation:** Fixes incomplete validation of app-supplied transaction data that could let a malicious app display a lower fee than miners receive (after fund preparation and repeated approvals/change-output warnings).
  * **Swap Refund Address Verification:** Fixes missing verification that a swap refund address belongs to the user's wallet, preventing a compromised app from substituting an attacker-controlled refund address without separate device confirmation.
  * **Multisig Derivation Path Restriction:** Restores restrictions on multisig receive address derivation paths so a malicious paired app cannot pull addresses outside standard search paths on registered multisig accounts (where withholding path details could create recovery friction even when recovery remains possible via descriptors/xpubs).
  * **Attestation Warning Banner & Device UI:** Makes the authenticity/genuine warning banner display globally regardless of setup/pairing state, and adds German device language support (with Italian and Spanish planned).
* **Prior 2026 Hardware Security Context (MOD 32 Cross-Reference):**
  * Tracks broader 2026 hardware and supply-chain lessons—including BitBox `07.2026` ("Oeschinen") and `08.2026` ("Dixence" v9.26.5) bootloader/memory/Silent-Payments fixes, reported mid-2026 Coldcard seed-generation flaw fallout, and browser/CDN clipper supply-chain risks (e.g., Nov 2026 Optimizely `track.js` incident).

---

###### 3. Pre-Update & Signing Checklist for Hardware Wallets
1. **Confirm Necessity & Read Full Notes:** Verify whether the update addresses an active security fix or required feature, and read the complete official release notes (never click links from emails, DMs, or QR codes).
2. **Verify Cryptographic Integrity:** Check official SHA-256 hashes and developer GPG signatures before applying firmware or companion app binaries; never enter seed words or passphrases during an update.
3. **Expect Multi-Stage Bootloader Behavior:** When a bootloader update is included (such as BitBox `11.2026` Cresta), maintain stable power/connection and watch for multiple progress bars and reboots without interrupting mid-flash.
4. **Verify Multisig Descriptors & On-Device Details:** Confirm multisig derivation paths/descriptors remain intact and verify addresses, amounts, and fees on-device prior to signing.
