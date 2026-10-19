# Suite preview installer

Use Development/stage-suite-preview.py to prepare a fresh clean-source snapshot. Then run build-full-installer.py with --payload, --output and --version. Add --test for the isolated maintenance-test AppId and registry namespace. Use the bundled compiler path recorded by the build tool; installer source, brand resources and ownership logic live here.

One component-selecting installer can install an individual app or the suite. Full includes optional Office rendering and offline English lyric transcription; Compact omits these larger components. PDF and OCR tools are individually selectable under Library. Engine licences and support files travel with their payload. Optional transcription runs only when requested and installs no background service.

The preview AppId and chosen root are retained on updates. Setup remembers selections and location; deselection removes known program files and registrations. Unknown personal additions, projects and settings are preserved. Close running apps before setup. Separate older Companion previews remain separate until explicitly migrated. Test updates, add/remove, wrong-location protection and uninstall under the isolated identity.

Workscape tabs the studios including Pulse. At setup completion it opens Workscape if available; standalone launch choices remain available. Preview and public/stable release channels stay separate. Current snapshot/evidence: Development/PREVIEW-SAVEPOINT.md.

Build.ps1, pilot.iss and the pilot test scripts are narrower Library/Workscape development tools. They are retained for those focused checks, not the full-suite build path.

For an installer-only handover, pass --installer-only and the explicit --date to Development/stage-suite-preview.py. This stages all selected app/tool bytes and a complete payload hash manifest without preparing portable/source release ZIPs. Installer 0.3.8 keeps the existing preview identity and also registers Companion recorder/preview/update helpers with Restart Manager. Public release preparation remains separate.
