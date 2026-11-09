JAGO EXPLORER THUMBNAILS

Shows embedded artwork previews for Jago drawing, dither, repeat, world, material, music, library, Pulse, 3D and Workscape projects. Save projects in the updated studio builds first. Older files without previews keep their normal icons until re-saved.

This optional Windows component needs administrator approval and installs its small native provider in Program Files/Common Files/Jago Suite/ExplorerThumbnails. Windows runs it through the isolated thumbnail-provider mechanism. It does not launch studios, access network services, change file-opening defaults or run at startup. It reads only the bounded embedded PNG cover, not the entire project.

Use Explorer medium, large or extra-large icons. Windows settings that disable thumbnails still apply. Existing thumbnails can remain cached until the file is saved again or the folder refreshed. Another thumbnail handler or a per-user handler can take precedence; this setup preserves other handlers.

Remove it through Windows Apps > Jago Explorer Thumbnails. Your projects stay untouched. This machine-wide Windows component has its own installer ownership because the creative apps remain usable without elevation. Removing the creative suite does not remove this optional shared Windows component.

Library reads the same project previews directly and does not require this Windows component. Companion's ordinary PNG/MP4 captures keep the standard Windows media previews; its Markdown/text exports are not reassociated.

Verification: native DLL rendering and aspect/alpha checks pass; per-user direct COM activation passes. Per-user Windows isolated-service activation failed on the development PC, so the shipped installer registers the class machine-wide. Actual elevated installation and Explorer browsing must be tested by the user; isolation has not been disabled in the shipped package.
