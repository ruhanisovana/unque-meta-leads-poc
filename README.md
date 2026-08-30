# UnQue - Meta Lead Ads PoC

## Live Demo Links
- **Backend (Live):** https://unque-meta-leads-poc.vercel.app
- **Get All Leads:** https://unque-meta-leads-poc.vercel.app/api/leads
- **Fake Meta Lead Tool (Click to create lead):** https://unque-meta-leads-poc.vercel.app/api/test-lead
- **GitHub Repo (This Repo):** https://github.com/YOUR_USERNAME/unque-meta-leads-poc
  -> Replace YOUR_USERNAME with your actual GitHub username from screenshot

## What You Must Show - How I Tested
1. Open Mobile App (mobile/App.js) on phone - screen already open
2. On laptop, open Fake Meta Lead Tool link above - it creates a new lead
3. Lead appears automatically in App within 2 seconds - no touch on device

## How it works
1. Meta Lead Ad submitted -> Meta calls `POST /api/webhook` with `leadgen_id`
2. For PoC (as assignment says fake lead allowed), `GET /api/test-lead` simulates Meta's Lead Testing Tool and creates same payload
3. React Native App polls `GET /api/leads` every 2 seconds using `setInterval`
4. New lead appears live

## Architecture

## 📹 Demo & Walkthrough

### 1. System Walkthrough (Main Demo - As per Requirement)
This video shows the complete flow as requested - App already open, submitting lead via Meta Lead Testing Tool, and lead appearing live without refreshing.
🔗 **Link:** https://drive.google.com/file/d/1WErhAdruA4meklThDUcOfbZ4ahDIPlCL/view?usp=drivesdk

### 2. Coding Walkthrough (Architecture & Code Explanation)
Detailed code walkthrough explaining Webhook, Graph API, Socket.io integration, and React Native frontend.
🔗 **Link:** https://drive.google.com/file/d/1whW36jt6s6oS48ILV8h65QxBq_8voWCl/view?usp=drivesdk

---
**Note:** Both videos access is set to `Anyone with the link - Viewer`
