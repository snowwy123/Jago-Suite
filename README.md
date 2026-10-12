# Jago Suite 2.8.0

Creative tools that work independently and together.

**Open source. Free forever.**

[Visit the website](https://jagosuite.co.uk/) · [Download the suite](https://github.com/snowwy123/Jago-Suite/releases/latest) · [Read the illustrated guide](Jago-Suite-Full-Guide.pdf)

## Download and get started

Download **Jago-Suite-v2.8.0.zip** from this repository’s Releases. Right-click the ZIP and choose **Extract All**, then open **Jago-Workscape.exe**.

Choose a studio from Workscape’s home screen, open several in tabs, or work side by side. Every studio also opens independently from its own folder. Keep the extracted folder structure together. No installer needed.

Windows apps require **64-bit Windows** and **Microsoft Edge WebView2 Runtime**. The seven studios also include named HTML files for offline browser use.

## Explore the studios

Each studio has its own source repository, individual download and online demo.

| Studio | What it does | Links |
|---|---|---|
| **Wobble** | Drawing, illustration and animation. | [Repository](https://github.com/snowwy123/Jago-Wobble-Studio) · [Download](https://github.com/snowwy123/Jago-Wobble-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-Wobble-Studio/) |
| **Dither** | Dithering, palettes and animated print effects. | [Repository](https://github.com/snowwy123/Jago-Dither-Studio) · [Download](https://github.com/snowwy123/Jago-Dither-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-Dither-Studio/) |
| **Repeat** | Seamless patterns and repeat layouts. | [Repository](https://github.com/snowwy123/Jago-Repeat-Studio) · [Download](https://github.com/snowwy123/Jago-Repeat-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-Repeat-Studio/) |
| **World** | Worldbuilding, maps, characters, family trees and timelines. | [Repository](https://github.com/snowwy123/Jago-World-Studio) · [Download](https://github.com/snowwy123/Jago-World-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-World-Studio/) |
| **Material** | Textures, materials and surface effects. | [Repository](https://github.com/snowwy123/Jago-Material-Studio) · [Download](https://github.com/snowwy123/Jago-Material-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-Material-Studio/) |
| **Sound** | Music, sound effects and ambience. | [Repository](https://github.com/snowwy123/Jago-Sound-Studio) · [Download](https://github.com/snowwy123/Jago-Sound-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-Sound-Studio/) |
| **Library** | Asset and font browsing, production layouts and PDF tools. | [Repository](https://github.com/snowwy123/Jago-Library-Studio) · [Download](https://github.com/snowwy123/Jago-Library-Studio/releases/latest) · [Try online](https://snowwy123.github.io/Jago-Library-Studio/) |
| **Workscape** | An optional home for studio tabs, side-by-side work and connected workflows. | [Repository](https://github.com/snowwy123/Jago-Workscape) · [Download](https://github.com/snowwy123/Jago-Workscape/releases/latest) |

## Work across studios

Use **Send to studio** to move supported artwork, audio and other assets between the apps. Turn a Wobble drawing into a Dither print, build a Repeat pattern from your artwork, or use Material and Repeat tiles on World maps.

Workscape brings the studios together while keeping their documents and tools separate. You can also use individual apps and export files for other creative software.

Save editable projects alongside your finished exports so you can return to your work.

## Guides and source

Read [**Jago-Suite-Full-Guide.pdf**](Jago-Suite-Full-Guide.pdf) for illustrated introductions, first projects, technical features and connected workflows. Individual downloads include their studio’s PDF guide, and each app’s **?** menu provides help and shortcuts.

This repository contains shared integration code, themes, fonts and cross-studio tests. Application source and build instructions live in the individual repositories linked above.

### Shared-module checks

Place the seven studio repositories beside this repository using these local folder names: `jago-wobble`, `jago-dither`, `jago-repeat`, `jago-world`, `jago-material`, `jago-sound` and `jago-library`.

From this repository, run:

```sh
node --test Suite/Tests/shared-modules.test.cjs
```

## About & rights

Open source. Free forever. Personal, professional and commercial use are welcome.

Imported assets and third-party components retain their own licences. See [LICENSE.txt](LICENSE.txt) and the individual studios’ notices. use are welcome. Imported assets and third-party components retain their own licences. See LICENSE.txt and the individual notices.
