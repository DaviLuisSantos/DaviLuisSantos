# Davi Luis

🇺🇸 English · [🇧🇷 Português](README.pt-BR.md)

**Full stack developer from Rio de Janeiro. I build systems that run in the real world, from APIs and web apps to hardware integrations and computer vision.**

> *Code is a way of thinking.* I try to write software the way I try to live: clearly, without shortcuts, and thinking about whoever comes next.

Most of my work happens far from the browser. A car pulls up to a gate, a camera reads the plate, and my code has a few hundred milliseconds to decide whether that gate opens. I spend my days with license plate cameras, access-control hardware, legacy Firebird databases and Windows servers in condominiums, where nobody is around to restart anything. That taught me to care about the boring parts: failure modes, tests, updates that roll themselves back.

[Portfolio](https://portifolio-daviluissantos-projects.vercel.app/en/) · [LinkedIn](https://www.linkedin.com/in/davi-luis/) · [YouTube](https://www.youtube.com/channel/UCryhrvnlMcEfvisWyQurlyA) · [Instagram](https://www.instagram.com/davi.luissc/)

---

## What I've built

### 🚗 LPR vehicle access-control server · *in production*
On-premise .NET server, built for Segmix, that decides in real time which vehicles may enter residential condominiums.
- Integrates **five camera vendors, each with its own protocol**: Alphadigi (HTTP, binary TCP, JSON-RPC), Hikvision, Motorola, Intelbras and Control iD UHF antennas. An architecture test keeps vendor code out of the core.
- **Moving off the legacy system:** a new mode runs without the Delphi/Firebird system the server was born next to. Vehicles, units, parking rights and access history come from the platform replacing it, and each passage is kept on disk until it's delivered.
- **Fail-closed by design:** when in doubt, the gate stays shut. Authorized plates are also synced to each camera, so the gate keeps working if the server goes down.
- **Self-healing operations:** detects cameras that stopped sending events and reconfigures them, and auto-updates during a maintenance window, rolling back if the health check fails.
- **1,300+ automated tests** (including contract tests against a real Firebird in Docker) and **90+ releases**. The source is private; builds ship through a [public releases repo](https://github.com/DaviLuisSantos/AlphadigiServidorLPR-releases).

`.NET 10` `ASP.NET Core` `Firebird` `SQLite` `MediatR` `GitHub Actions`

### 🔐 [ControlId.Net](https://github.com/DaviLuisSantos/ControlId.Net) · *open source, on [NuGet](https://www.nuget.org/packages/ControlId.Net)*
The .NET library I wished existed when I started integrating Control iD access-control devices and REP time clocks.
- Covers the whole documented API of the access line (iDAccess, iDFlex, iDFace, iDBox, iDUHF), from users, faces and turnstiles to SIP intercom, RTSP streaming and network settings, with a test that fails if any documented section goes missing.
- Built for many devices at once: operations across a fleet with a result per device, paginated reads with `IAsyncEnumerable`, and a per-device concurrency limit, tuned on a real iDFace.
- Managed sessions with automatic re-login, Push mode for devices behind NAT, and ASP.NET Core endpoints to authorize access in real time.
- A streaming parser for Brazilian time-clock files (AFD, Portaria 671/2021 and 1510/2009) that validates CRC-16 and survives corrupted lines.
- **220+ tests** on .NET 8 and .NET 10 (Linux) and .NET Framework 4.8 (Windows). Three NuGet packages (core, DependencyInjection, AspNetCore) published with Trusted Publishing (OIDC): no keys in the repo, and nothing ships unless every test passes.

`.NET 8` `.NET 10` `.NET Standard 2.0` `ASP.NET Core` `xUnit`

### 📟 [CYD PC Dashboard](https://github.com/DaviLuisSantos/cyd-pc-dashboard) · *ESP32 firmware*
A US$15 touchscreen that sits next to my monitor showing PC stats, processes, network, service checks, market quotes with 24h history, what's playing (with controls), shortcut buttons that run actions on the PC, and YouTube stats. [Flash it from your browser](https://daviluissantos.github.io/cyd-pc-dashboard/), no toolchain needed.
- Flicker-free rendering with off-screen sprites, color themes, night mode, an RGB status LED, auto brightness from the light sensor, and a UI in English and Portuguese.
- Over-the-air updates that roll back on their own if the new firmware isn't healthy, a web interface, and a PC agent the screen finds on the network by itself, also shipped as a Windows `.exe` so no Python is needed.
- The fun part was debugging the hardware: corrupted SPI reads because the display and touch controller shared a peripheral, and framebuffer reads shifted by one bit until I dropped the read clock to 6 MHz.

`C++` `ESP32` `PlatformIO` `Python` `GitHub Actions`

### More
- **[Arco](https://github.com/DaviLuisSantos/HabitSystem)** ([live](https://habit-system-front.vercel.app)), *v1.0*: a habit tracker PWA with weighted habits, partial check-ins and consistency scores. Vertical-slice .NET 9 API, JWT auth with per-device sessions, transactional email, continuous deploy to Azure, Next.js front end.
- **Emplaca** (private for now, *alpha*): my own Brazilian license plate recognition, with a detector and OCR trained in PyTorch and running natively in .NET via ONNX Runtime on the CPU. On a frozen test set of real gate-camera frames, the models fine-tuned on real images read the plate exactly in 64% of frames, and 83% at a second site they never trained on. Running the detector only where each camera actually sees plates cut the time per frame by 37% with the same accuracy.
- **[JobRadar AU](https://github.com/DaviLuisSantos/job-radar-au)**: tracks the Australian job market for Working Holiday visa holders. It collects listings every day, ranks them against a profile with a score that explains itself, tracks applications, and builds an aggregated monthly market snapshot for a newsletter for Brazilians moving to Australia. A .NET 10 rewrite of my Python prototype, [Job Tracker](https://github.com/DaviLuisSantos/job-tracker), checked to give the same scores on 5,388 real listings. Layered architecture, Postgres, a Blazor triage UI, running as Windows services.
- **YouTube research pipeline** (private): pulls video captions or, when YouTube rate-limits them, transcribes the audio locally with faster-whisper, then uses LLMs to analyze transcripts and extract insights for my channel. Runs from a small web UI.
- **[Roteiro Manager](https://github.com/DaviLuisSantos/RoteiroManager)**: the Markdown editor and teleprompter I use to record my own videos.

---

## How I work

- **Assume things will fail.** Networks drop, cameras freeze, databases lock. I design for that first: fail-closed defaults, retries with backoff, health checks, rollbacks.
- **Tests are what let me ship on a Friday.** Most of the code I care about runs where I can't reach it, so the test suite is my safety net.
- **Boundaries keep code honest.** Vendor protocols, frameworks and databases stay at the edges, and I let architecture tests enforce it.
- **Numbers over impressions.** I measure models on data they never saw, report what the confidence threshold really buys, and say clearly what hasn't been measured yet.
- **Automate the release.** Tag, build, test, publish, update. If a human has to remember a step, it will eventually be skipped.

## Tools I reach for

- **Back end:** C# / .NET, ASP.NET Core, EF Core, MediatR, Node.js
- **Front end:** TypeScript, React, Next.js, Blazor, Astro, Tailwind CSS
- **AI & computer vision:** PyTorch, ONNX / ONNX Runtime, OpenCV, object detection and OCR, synthetic data generation, Whisper (speech-to-text), LLM APIs
- **Data:** PostgreSQL, SQLite, Firebird
- **Cloud & DevOps:** Azure, Docker, GitHub Actions
- **Also:** Python, ESP32 / PlatformIO

## GitHub in numbers

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/0-profile-details.svg" />
  <img alt="Profile details" src="profile-summary-card-output/github/0-profile-details.svg" width="100%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/3-stats.svg" />
  <img alt="GitHub stats" src="profile-summary-card-output/github/3-stats.svg" width="49%" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/4-productive-time.svg" />
  <img alt="Productive time" src="profile-summary-card-output/github/4-productive-time.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-stats/releases-dark.svg" />
  <img alt="Releases shipped" src="profile-stats/releases-light.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/1-repos-per-language.svg" />
  <img alt="Repos per language" src="profile-summary-card-output/github/1-repos-per-language.svg" width="49%" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="profile-summary-card-output/github_dark/2-most-commit-language.svg" />
  <img alt="Most commit language" src="profile-summary-card-output/github/2-most-commit-language.svg" width="49%" />
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/DaviLuisSantos/DaviLuisSantos/output/github-snake-dark.svg" />
  <img alt="Snake eating my contribution graph" src="https://raw.githubusercontent.com/DaviLuisSantos/DaviLuisSantos/output/github-snake.svg" />
</picture>
</p>

## Beyond the code

I have a degree in Systems Analysis and Development, I'm studying Computer Science, and I'm **Microsoft Certified: Azure Fundamentals (AZ-900)**. On my YouTube channel, **Davi Dev**, I show the projects I'm building, the tools I use and what I'm learning along the way.

[**Watch on YouTube →**](https://www.youtube.com/channel/UCryhrvnlMcEfvisWyQurlyA)
