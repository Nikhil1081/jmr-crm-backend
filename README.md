# JMR Infotech &bull; Multi-Employee CRM Portal (2026)

Enterprise CRM portal engineered for JMR Infotech's Oracle Platinum Partner ecosystem, featuring full tracking of 601 real representatives, 6,098 BFSI opportunities ($15.8B total pipeline), and 59 global partner banks.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Nikhil1081/jmr-crm-backend)

---

## 🌐 Live Deployments

- **Fresh Production Frontend (Firebase Hosting)**: [https://jmr-crm-portal-2026.web.app](https://jmr-crm-portal-2026.web.app)
- **Secondary Firebase Domain**: [https://jmr-crm-portal-2026.firebaseapp.com](https://jmr-crm-portal-2026.firebaseapp.com)
- **GitHub Repository**: [https://github.com/Nikhil1081/jmr-crm-backend](https://github.com/Nikhil1081/jmr-crm-backend)

---

## 🚀 1-Click Backend Deployment on Render (100% Free)

### Option 1: 1-Click Deploy via Render Blueprint
1. Click the **[Deploy to Render](https://render.com/deploy?repo=https://github.com/Nikhil1081/jmr-crm-backend)** button above.
2. Sign in to [Render](https://dashboard.render.com).
3. Set your environment variable:
   - `GROQ_API_KEY`: Enter your Groq API key (starts with `gsk_...`).
4. Click **Apply**. Render will automatically:
   - Install Python dependencies from `requirements.txt`
   - Run `python seed_jmr_600.py` to seed all 601 employees and 2026 BFSI deals
   - Launch `uvicorn crm_portal_single_file:app --host 0.0.0.0 --port $PORT`
5. Render will give you a public HTTPS URL: `https://<your-service>.onrender.com`.

### Option 2: Manual Web Service Setup on Render
1. Open [dashboard.render.com](https://dashboard.render.com) &rarr; Click **New +** &rarr; **Web Service**.
2. Select **Build and deploy from a Git repository** &rarr; choose `Nikhil1081/jmr-crm-backend`.
3. Fill in the following:
   - **Name**: `jmr-crm-backend`
   - **Runtime**: `Python 3`
   - **Branch**: `master`
   - **Build Command**: `pip install -r requirements.txt && python seed_jmr_600.py`
   - **Start Command**: `uvicorn crm_portal_single_file:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` ($0/mo)
4. Under **Environment Variables**:
   - `GROQ_API_KEY`: your Groq key
5. Click **Create Web Service**.

---

## 🔗 Connecting Frontend & Backend

Once your Render backend is live:
1. Open the frontend: [https://jmr-crm-portal-2026.web.app](https://jmr-crm-portal-2026.web.app)
2. In the top header, click **API: Local / Cloud**.
3. Paste your Render backend URL (e.g. `https://jmr-crm-backend.onrender.com`).
4. Click **Test Ping** &rarr; **Save & Connect**.

---

## 💻 Local Development

```bash
pip install -r requirements.txt
python seed_jmr_600.py
uvicorn crm_portal_single_file:app --reload
```
- Local Dashboard: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Admin Login: `admin@crm.com` / `admin123`
