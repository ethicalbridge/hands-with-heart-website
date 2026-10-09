# Hands With Heart Foundation website

Static site (HTML, CSS, a little JS). No build tools beyond Python 3.

- `python3 build.py` regenerates every page. Edit content in `build.py` (news, stories, partners, people), then re-run.
- Preview: `python3 -m http.server` in this folder, open http://localhost:8000
- Deploy: upload the folder contents as the site root (all links are relative).
- Styles follow the HwH Brand Manual v1: Heart Red #CB2E28, Ink #141414, Paper #F5F4F4, Inter Tight + Lora, programme colours for tags only.

## Structure
About us (home, with Founder / Advisors / Team / Team leaders sections) · Our objectives (5 external + systems for scale) · Our projects (ParaSurf, Bahía de Niños, Missions: Bali, Costa Rica, Ukraine, Romania, Argentina/Chaco) · Stories · News · Reports · Partners · Contact · Donate

## Still needed from the team (marked yellow "To add" on the pages)
1. Founder biography and consented portrait; advisors, team and team leaders (names, roles, bios, portraits).
2. Existing Stories from the current site, with photo and recorded consent for each.
3. A payment link: set `DONATE_URL` in `build.py` (currently opens an email).
4. Partner logos, once each partner has given written permission (names only for now). UNICEF is deliberately not listed until the relationship is documented.
5. Check the NEWS items and the cumulative figures (96 missions, 636 volunteers, 5,511 people, 9,547 sessions) before publishing; the Strategic Direction notes these need reconciling.
6. Confirm the Bahía de Niños funding figures and phase dates are cleared for public release.
