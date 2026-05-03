# Serverless URL Shortener

A fully serverless URL shortening service built on AWS. Provisioned entirely with Terraform as infrastructure-as-code and deployed via a GitHub Actions CI/CD pipeline. 
Supports creating short codes from long URLs and redirecting short codes back to their original destination.
---

## What It Does
- **POST /shorten** — accepts a long URL and returns a generated short code stored in DynamoDB
- **GET /{short_code}** — looks up the short code and returns a 301 redirect to the original URL
- **CloudWatch alarm** — monitors Lambda error rate and fires when any errors are detected
- All infrastructure is defined in code — no manual AWS console setup required
---

## Architecture

```
Client
  │
  ▼
API Gateway (REST API)
  │
  ▼
AWS Lambda (Python 3.11)
  │
  ├──► DynamoDB (stores short_code → long_url mappings)
  │
  └──► CloudWatch (error rate alarm)

Infrastructure provisioned via Terraform
CI/CD pipeline via GitHub Actions
```

## Tech Stack

| Layer | Technology |
|---|---|
| Compute | AWS Lambda (Python 3.11) |
| Database | AWS DynamoDB (on-demand billing) |
| API | AWS API Gateway (REST) |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Observability | AWS CloudWatch Metrics & Alarms |
| Language | Python 3.11 |
---

## Project Structure
```
url-shortener/
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions CI/CD pipeline
├── lambda/
│   └── lambda_function.py    # Core Lambda handler (shorten + redirect logic)
├── terraform/
│   ├── main.tf               # All AWS resources (Lambda, DynamoDB, API Gateway, IAM)
│   ├── variables.tf          # Configurable variables (region, table name, function name)
│   └── outputs.tf            # Outputs API URL after deployment
├── .gitignore
└── README.md
```

## How to Deploy

### Prerequisites
- [AWS account](https://aws.amazon.com) with an IAM user that has programmatic access
- [Terraform](https://developer.hashicorp.com/terraform/install) installed
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and configured
- [Python 3.11+](https://www.python.org/downloads/) installed

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/AhnafHy/Url-Shortener.git
cd Url-Shortener
```

**2. Configure AWS credentials**
```bash
aws configure
```
Enter your AWS Access Key ID, Secret Access Key, region (`us-east-2`), and output format (`json`).

**3. Initialize Terraform**
```bash
cd terraform
terraform init
```

**4. Preview the infrastructure**
```bash
terraform plan
```

**5. Deploy**
```bash
terraform apply
```
Type `yes` when prompted. Terraform will output your API URL when complete.

**6. Test the API**

Shorten a URL:
```powershell
Invoke-WebRequest -Uri "https://ghsulsu9cf.execute-api.us-east-2.amazonaws.com/prod/shorten" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"url": "https://www.google.com"}'
```

Test the redirect:
```powershell
Invoke-WebRequest -Uri "https://ghsulsu9cf.execute-api.us-east-2.amazonaws.com/prod/{short_code}" -Method GET -MaximumRedirection 0
```

**7. Clean up (avoids AWS charges)**
```bash
terraform destroy
```

## API Reference

### POST /shorten

**Request body:**
```json
{
  "url": "https://www.example.com"
}
```

**Response:**
```json
{
  "short_code": "NuUtlz",
  "short_url": "Use GET /NuUtlz to redirect"
}
```

### GET /{short_code}

Returns a `301 Moved Permanently` redirect to the original URL.

| Status | Meaning |
|---|---|
| 301 | Short code found, redirecting |
| 404 | Short code not found |
| 400 | Invalid request |
---

## API Response Screenshot

**Shorten endpoint (POST /shorten):**

<img width="1834" height="254" alt="post-response" src="https://github.com/user-attachments/assets/d85120b9-842d-4e71-a190-7118f1e5a7a8" />


**Redirect endpoint (GET /{short_code}):**

<img width="1831" height="250" alt="get-response" src="https://github.com/user-attachments/assets/0d79f0fe-ca4a-4c5f-8fa5-db1fabc84da6" />


---

## Key Concepts Demonstrated

- **Infrastructure as Code (IaC)** — all AWS resources defined in Terraform, reproducible in any account
- **Serverless architecture** — no servers to manage, scales automatically, pay-per-request pricing
- **NoSQL data modeling** — DynamoDB with a single hash key for O(1) lookups
- **API design** — REST API with proper HTTP status codes (200, 301, 400, 404)
- **Observability** — CloudWatch alarm monitoring Lambda error rate in production
- **CI/CD** — automated deployment pipeline via GitHub Actions on every push to main
