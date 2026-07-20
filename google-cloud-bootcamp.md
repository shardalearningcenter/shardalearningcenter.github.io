---
layout: page
title: Google Cloud Bootcamp
permalink: /google-cloud-bootcamp/
---

# Google Cloud Bootcamp

A practical, project-first bootcamp to learn **Google Cloud Platform (GCP)** — from free-tier setup to shipping real cloud apps.

**Who it’s for:** Developers, students, DevOps beginners, and anyone targeting Associate Cloud Engineer skills  
**Style:** Hands-on labs · No fluff · Build → deploy → observe  
**Related:** [Courses](/courses/) · [LLM Bootcamp](/llm-bootcamp/) · [C Getting Started](/c-getting-started/)

---

## What You’ll Build

| Project | Skills |
|---|---|
| Static site on Cloud Storage + HTTPS | Storage, CDN-style hosting |
| Containerized API on Cloud Run | Docker, serverless containers |
| Event pipeline: Pub/Sub → Function | Messaging, serverless |
| VM + firewall + SSH | Compute Engine networking |
| BigQuery analytics dashboard query | Data warehouse SQL |
| Capstone: full stack on GCP | End-to-end architecture |

---

## Table of Contents

1. [Module 1 — Foundations & Free Tier](#module-1--foundations--free-tier)  
2. [Module 2 — IAM, Projects & CLI](#module-2--iam-projects--cli)  
3. [Module 3 — Compute (VMs & Containers)](#module-3--compute-vms--containers)  
4. [Module 4 — Storage & Networking Basics](#module-4--storage--networking-basics)  
5. [Module 5 — Serverless (Cloud Run, Functions, Pub/Sub)](#module-5--serverless-cloud-run-functions-pubsub)  
6. [Module 6 — Data (Cloud SQL & BigQuery)](#module-6--data-cloud-sql--bigquery)  
7. [Module 7 — Observability, Security & Cost](#module-7--observability-security--cost)  
8. [Module 8 — Capstone & Career Path](#module-8--capstone--career-path)  
9. [Cheatsheet](#cheatsheet)  
10. [Suggested 4-Week Schedule](#suggested-4-week-schedule)

---

## Module 1 — Foundations & Free Tier

**Goal:** Understand GCP mental model and set up a safe billing-aware account.

### Lessons

| # | Topic |
|---|---|
| 1 | What is cloud? IaaS vs PaaS vs SaaS |
| 2 | GCP global layout: regions, zones, projects |
| 3 | Create a Google Cloud account + Free Trial / Free Tier |
| 4 | Console tour: Navigation menu, Cloud Shell, billing alerts |
| 5 | Enable APIs (why “API not enabled” errors happen) |

### Hands-on Lab 1.1 — First project

1. Create project: `gcp-bootcamp-demo`  
2. Set a **budget alert** (e.g. $5 and $10)  
3. Open **Cloud Shell** and run:

```bash
gcloud config list
gcloud projects list
gcloud config set project YOUR_PROJECT_ID
```

### Task
Write 5 lines in a notes file: *region vs zone*, *project vs billing account*, *what Free Tier covers*.

---

## Module 2 — IAM, Projects & CLI

**Goal:** Use `gcloud` confidently and never leave the project wide open.

### Lessons

| # | Topic |
|---|---|
| 1 | Identities: users, service accounts, groups |
| 2 | Roles: basic vs predefined vs custom (least privilege) |
| 3 | Service accounts for apps (not your personal user) |
| 4 | `gcloud` auth, configs, and multiple projects |
| 5 | Cloud Shell vs local SDK install |

### Essential commands

```bash
# Login & project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud config set compute/region asia-south1
gcloud config set compute/zone asia-south1-a

# IAM quick view
gcloud projects get-iam-policy YOUR_PROJECT_ID

# Create a service account
gcloud iam service-accounts create app-runner \
  --display-name="App Runner"
```

### Hands-on Lab 2.1
Create service account `app-runner@...`, grant **roles/run.invoker** (or Viewer for practice), list members.

### Task
Explain in one sentence: why apps should use a **service account**, not your Google login key.

---

## Module 3 — Compute (VMs & Containers)

**Goal:** Launch a VM, SSH in, and understand when to use VMs vs containers.

### Lessons

| # | Topic |
|---|---|
| 1 | Compute Engine machines, disks, images |
| 2 | Firewall rules (ingress / egress) |
| 3 | SSH from browser & from `gcloud compute ssh` |
| 4 | Startup scripts |
| 5 | Containers overview → Artifact Registry |

### Hands-on Lab 3.1 — Nginx on a VM

```bash
gcloud compute instances create web-1 \
  --machine-type=e2-micro \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --tags=http-server

gcloud compute firewall-rules create allow-http \
  --allow=tcp:80 \
  --target-tags=http-server \
  --description="Allow HTTP"
```

SSH and install nginx:

```bash
gcloud compute ssh web-1
sudo apt update && sudo apt install -y nginx
sudo systemctl enable --now nginx
```

Open external IP in browser → “Welcome to nginx!”

### Hands-on Lab 3.2 — Tiny Docker image

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
CMD ["python", "app.py"]
```

```python
# app.py
from flask import Flask
app = Flask(__name__)

@app.get("/")
def hi():
    return {"ok": True, "msg": "hello from container"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

### Task
Stop or delete the VM when done (`gcloud compute instances stop web-1`) to save quota/cost.

---

## Module 4 — Storage & Networking Basics

**Goal:** Host files, understand buckets, and basic VPC ideas.

### Lessons

| # | Topic |
|---|---|
| 1 | Cloud Storage buckets, classes, lifecycle |
| 2 | Public vs private objects; signed URLs idea |
| 3 | VPC, subnets, internal vs external IP |
| 4 | Load balancing (conceptual) |
| 5 | Cloud CDN (conceptual) |

### Hands-on Lab 4.1 — Static website bucket

```bash
BUCKET="gcp-bootcamp-site-$RANDOM"
gcloud storage buckets create gs://$BUCKET --location=asia-south1

echo '<h1>Hello from Cloud Storage</h1>' > index.html
gcloud storage cp index.html gs://$BUCKET/index.html
```

Then in Console: enable static website config / permissions carefully (prefer uniform bucket-level access + least privilege).

### Task
Upload a second page `about.html` and open both object URLs.

---

## Module 5 — Serverless (Cloud Run, Functions, Pub/Sub)

**Goal:** Deploy without managing servers — the most practical GCP skill for developers.

### Lessons

| # | Topic |
|---|---|
| 1 | Cloud Run: container → HTTPS URL |
| 2 | Revisions, concurrency, min/max instances |
| 3 | Cloud Functions (Gen2) for event glue |
| 4 | Pub/Sub topics & subscriptions |
| 5 | Event arc: upload → notify → process |

### Hands-on Lab 5.1 — Deploy to Cloud Run

```bash
gcloud artifacts repositories create apps \
  --repository-format=docker \
  --location=asia-south1

gcloud builds submit --tag asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/apps/hello:v1

gcloud run deploy hello \
  --image=asia-south1-docker.pkg.dev/YOUR_PROJECT_ID/apps/hello:v1 \
  --region=asia-south1 \
  --allow-unauthenticated \
  --port=8080
```

Hit the service URL — JSON hello response.

### Hands-on Lab 5.2 — Pub/Sub ping

```bash
gcloud pubsub topics create bootcamp-events
gcloud pubsub subscriptions create bootcamp-events-sub --topic=bootcamp-events
gcloud pubsub topics publish bootcamp-events --message="hello-pubsub"
gcloud pubsub subscriptions pull bootcamp-events-sub --auto-ack --limit=5
```

### Task
Change the Flask message, rebuild, redeploy Cloud Run as `v2`. Confirm the new revision serves traffic.

---

## Module 6 — Data (Cloud SQL & BigQuery)

**Goal:** Store app data and run analytics SQL.

### Lessons

| # | Topic |
|---|---|
| 1 | Cloud SQL (Postgres/MySQL) overview |
| 2 | Connecting from Cloud Run (private IP / connectors — concepts) |
| 3 | BigQuery datasets, tables, jobs |
| 4 | Public datasets & first SELECT |
| 5 | When to use SQL DB vs warehouse vs Storage |

### Hands-on Lab 6.1 — BigQuery first query

In BigQuery console (or `bq`):

```sql
SELECT
  word,
  word_count
FROM
  `bigquery-public-data.samples.shakespeare`
WHERE
  corpus = 'hamlet'
ORDER BY
  word_count DESC
LIMIT 10;
```

### Hands-on Lab 6.2 — Load a CSV to BigQuery

1. Upload `sales.csv` to a bucket  
2. Create dataset `bootcamp`  
3. Load job → table `sales`  
4. Query totals by day

### Task
Write a query that returns top 5 rows from your table and save it as a saved query.

---

## Module 7 — Observability, Security & Cost

**Goal:** Operate like a professional — logs, metrics, IAM hygiene, spend control.

### Lessons

| # | Topic |
|---|---|
| 1 | Cloud Logging: query by resource |
| 2 | Cloud Monitoring: uptime checks (intro) |
| 3 | Error Reporting / alerts (intro) |
| 4 | Secrets Manager vs env vars |
| 5 | Budgets, quotas, rightsizing e2-micro / Cloud Run |

### Hands-on Lab 7.1
1. Open Logs Explorer for your Cloud Run service  
2. Filter severity ≥ ERROR  
3. Create a budget alert if you haven’t  

### Security checklist

- [ ] No public buckets with sensitive data  
- [ ] Service accounts have least roles  
- [ ] Keys downloaded only when required (prefer ADC / workload identity)  
- [ ] Delete idle VMs / disks  
- [ ] Billing alerts on  

---

## Module 8 — Capstone & Career Path

### Capstone: “URL Shortener Lite” on GCP

**Architecture**

```text
User → Cloud Run (API)
         ↓
    Firestore or Cloud SQL (mappings)
         ↓
    Cloud Storage (optional static admin page)
         ↓
    Cloud Logging + budget alerts
```

**Requirements**

1. `POST /shorten` `{ "url": "https://..." }` → `{ "code": "abc123" }`  
2. `GET /abc123` → redirect to original URL  
3. Deploy on **Cloud Run**  
4. README with architecture diagram + deploy commands  
5. Cost note: how you kept it near free tier  

### Stretch goals
- Pub/Sub event on each click  
- BigQuery export of click counts  
- Custom domain + HTTPS load balancer (advanced)

### Career mapping

| Role | Focus modules |
|---|---|
| Cloud / DevOps Engineer | 2, 3, 4, 7 |
| Backend developer on GCP | 5, 6, 7 |
| Data analyst | 6, 7 |
| Associate Cloud Engineer exam | All + practice exams |

**Cert tip:** After this bootcamp, practice [Google Associate Cloud Engineer](https://cloud.google.com/learn/certification/cloud-engineer) sample questions — map each wrong answer back to a module.

---

## Cheatsheet

```bash
# Project
gcloud config set project PROJECT_ID
gcloud services enable run.googleapis.com compute.googleapis.com \
  artifactregistry.googleapis.com cloudbuild.googleapis.com pubsub.googleapis.com

# VM
gcloud compute instances list
gcloud compute ssh INSTANCE

# Cloud Run
gcloud run services list --region=REGION
gcloud run services describe SERVICE --region=REGION

# Storage
gcloud storage ls
gcloud storage cp ./file gs://BUCKET/

# Pub/Sub
gcloud pubsub topics list
gcloud pubsub subscriptions pull SUB --auto-ack

# Cleanup (example)
gcloud run services delete hello --region=asia-south1
gcloud compute instances delete web-1
```

### Region pick (India-friendly default)
`asia-south1` (Mumbai) — change if your audience is elsewhere.

---

## Suggested 4-Week Schedule

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Modules 1–2 | Project + IAM + `gcloud` fluency |
| 2 | Modules 3–4 | VM nginx + Storage static page |
| 3 | Module 5 | Cloud Run app + Pub/Sub lab |
| 4 | Modules 6–8 | BigQuery lab + Capstone deployed |

**Study load:** ~6–8 hours/week.

---

## Cleanup Habit (Do This Always)

When a lab ends:

1. Delete Cloud Run services you don’t need  
2. Stop/delete VMs + unused disks  
3. Delete test buckets with sample data  
4. Check **Billing → Reports**  

---

## What’s Next?

- Ship AI on GCP: combine with [LLM Bootcamp](/llm-bootcamp/) (Vertex AI later)  
- Language foundations: [Python Bootcamp](/python-bootcamp/) · [C Getting Started](/c-getting-started/)  
- Browse all: [Courses](/courses/)

---

*Build on the free tier. Watch billing. Prefer Cloud Run over always-on VMs. That is how you learn GCP without surprise bills.*
