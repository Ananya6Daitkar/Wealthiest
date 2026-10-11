# Hosted synthetic demonstration

Render Blueprint: `render.yaml`. This runs the complete Python API and browser UI in one free web service, using one worker and temporary SQLite storage. The hosted build is a demonstration, not a production financial service.

- Render generates `NESTPROOF_DEMO_PASSWORD`; obtain it privately from the service's Environment panel. Browser username: `judge`. Never put the password in README, screenshots, URLs or commits.
- The password protects the HTML, assets and API. Only the content-free `/healthz` endpoint is public. The application refuses to start on Render without the password.
- All invited reviewers share a synthetic workspace and may switch both demo personas. This gate does not create isolated user accounts. Use fictional files only; conduct one session at a time. For controlled studies, prefer a separate local database per participant.
- Free-instance files can disappear on redeployment or restart. Export receipts and study notes before ending a session. A cold start may delay the first visit.
- No paid disk or paid plan is selected. Durable production storage, real identity, tenant isolation and operational controls remain future work.

## Launch

Create a Render Blueprint from this repository's `main` branch. Review the free plan and generated environment values, deploy, then verify `/healthz`, password rejection, login, a source comparison, preview/confirm and undo. Add the returned live URL to README only after verification. A Render configuration file is not evidence of a successful deployment.

References: [Blueprint specification](https://render.com/docs/blueprint-spec), [free-instance limitations](https://render.com/docs/free).
