# Hosted synthetic demonstration

Live service: **https://nestproof-demo.onrender.com/**. Render reported Live on 11 October 2026. External checks returned HTTP 200 for `/healthz` and HTTP 401 with a Basic authentication challenge for `/`. The Codex in-app browser could not open the Basic-auth page (`ERR_BLOCKED_BY_CLIENT`); this does not verify an authenticated browser workflow. Use a browser supporting HTTP Basic authentication and retrieve the password privately from Render. Never remove the access gate to work around a browser limitation.

Render Blueprint: `render.yaml`. This runs the complete Python API and browser UI in one free web service, using one worker and temporary SQLite storage. The hosted build is a demonstration, not a production financial service.

- Render generates `NESTPROOF_DEMO_PASSWORD`; obtain it privately from the service's Environment panel. Browser username: `judge`. Never put the password in README, screenshots, URLs or commits.
- The password protects the HTML, assets and API. Only the content-free `/healthz` endpoint is public. The application refuses to start on Render without the password.
- All invited reviewers share a synthetic workspace and may switch both demo personas. This gate does not create isolated user accounts. Use fictional files only; conduct one session at a time. For controlled studies, prefer a separate local database per participant.
- Free-instance files can disappear on redeployment or restart. Export receipts and study notes before ending a session. A cold start may delay the first visit.
- No paid disk or paid plan is selected. Durable production storage, real identity, tenant isolation and operational controls remain future work.

## Launch

Create a Render Blueprint from this repository's `main` branch. Review the free plan and generated environment values, deploy, then verify `/healthz`, password rejection, login, a source comparison, preview/confirm and undo. Add the returned live URL to README only after verification. A Render configuration file is not evidence of a successful deployment.

References: [Blueprint specification](https://render.com/docs/blueprint-spec), [free-instance limitations](https://render.com/docs/free).
