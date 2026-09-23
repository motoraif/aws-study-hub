#!/usr/bin/env python3
"""One-off helper: append new quiz questions to data/quiz-questions.json.

Safe to re-run: questions are keyed by `id`, and existing ids are never
overwritten or duplicated. Validates structure before writing.
"""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, "data", "quiz-questions.json")

# Each: id, cert, domain, question, options[4], answer (index), explanation.
NEW = [
    # ── CLF-C02 ──────────────────────────────────────────────
    {"id":"clf-011","cert":"CLF-C02","domain":"Cloud Concepts",
     "question":"Which AWS Well-Architected Framework pillar focuses on the ability of a system to recover from failures and meet demand?",
     "options":["Operational Excellence","Reliability","Cost Optimization","Performance Efficiency"],
     "answer":1,
     "explanation":"The Reliability pillar covers the ability of a workload to perform its function correctly and consistently, including recovering from failures and dynamically acquiring resources to meet demand."},
    {"id":"clf-012","cert":"CLF-C02","domain":"Security & Compliance",
     "question":"Under the AWS shared responsibility model, which task is the customer's responsibility?",
     "options":["Patching the hypervisor","Configuring security groups and IAM policies","Maintaining physical data center security","Replacing failed disks in the storage fleet"],
     "answer":1,
     "explanation":"Customers are responsible for security IN the cloud, which includes configuring IAM, security groups, and encrypting their data. AWS is responsible for security OF the cloud (hardware, hypervisor, facilities)."},
    {"id":"clf-013","cert":"CLF-C02","domain":"Billing, Pricing & Support",
     "question":"Which AWS pricing model offers the largest discount for a one- or three-year commitment to a consistent amount of compute usage?",
     "options":["On-Demand","Savings Plans","Spot Instances","Dedicated Hosts"],
     "answer":1,
     "explanation":"Savings Plans offer lower prices in exchange for a commitment to a consistent amount of usage (measured in $/hour) for a 1- or 3-year term. Spot can be cheaper per-hour but is interruptible and not a commitment discount."},
    {"id":"clf-014","cert":"CLF-C02","domain":"Cloud Technology & Services",
     "question":"A company wants a managed service to run containers without managing the underlying EC2 instances. Which option is BEST?",
     "options":["Amazon EC2 with Docker installed","AWS Fargate","AWS Batch on EC2","Amazon Lightsail"],
     "answer":1,
     "explanation":"AWS Fargate is a serverless compute engine for containers that removes the need to provision and manage EC2 instances. It works with both ECS and EKS."},
    {"id":"clf-015","cert":"CLF-C02","domain":"Billing, Pricing & Support",
     "question":"Which tool lets you visualize, understand, and manage your AWS costs and usage over time?",
     "options":["AWS Config","AWS Cost Explorer","AWS CloudTrail","AWS Trusted Advisor"],
     "answer":1,
     "explanation":"AWS Cost Explorer provides an interface to visualize and analyze cost and usage data over time. CloudTrail logs API activity, Config tracks resource configuration, and Trusted Advisor gives best-practice checks."},

    # ── SAA-C03 ──────────────────────────────────────────────
    {"id":"saa-011","cert":"SAA-C03","domain":"Design Resilient Architectures",
     "question":"An application must decouple a fleet of producers from consumers and guarantee each message is processed by exactly one consumer. Which service fits BEST?",
     "options":["Amazon SNS","Amazon SQS","Amazon Kinesis Data Streams","AWS Step Functions"],
     "answer":1,
     "explanation":"Amazon SQS is a message queue where each message is consumed by a single consumer, decoupling producers from consumers. SNS is pub/sub (fan-out to many subscribers)."},
    {"id":"saa-012","cert":"SAA-C03","domain":"Design Secure Architectures",
     "question":"How should an EC2 application obtain credentials to call AWS APIs securely?",
     "options":["Hard-code access keys in the application","Store keys in environment variables","Attach an IAM role to the EC2 instance","Embed keys in the AMI"],
     "answer":2,
     "explanation":"Attaching an IAM role provides temporary, automatically rotated credentials via the instance metadata service. Never hard-code or embed long-term access keys."},
    {"id":"saa-013","cert":"SAA-C03","domain":"Design High-Performing Architectures",
     "question":"A read-heavy relational workload on Amazon RDS needs to scale read capacity without impacting the primary. What should you add?",
     "options":["A Multi-AZ standby","Read replicas","A larger instance class only","RDS Proxy"],
     "answer":1,
     "explanation":"Read replicas offload read traffic from the primary and can scale horizontally. A Multi-AZ standby is for failover and does not serve reads. RDS Proxy pools connections but doesn't add read capacity."},
    {"id":"saa-014","cert":"SAA-C03","domain":"Design Cost-Optimized Architectures",
     "question":"Which S3 storage class automatically moves objects between access tiers based on changing access patterns with no retrieval fees?",
     "options":["S3 Standard-IA","S3 One Zone-IA","S3 Intelligent-Tiering","S3 Glacier Flexible Retrieval"],
     "answer":2,
     "explanation":"S3 Intelligent-Tiering automatically moves objects between frequent and infrequent access tiers based on usage, with no retrieval fees, ideal for unpredictable access patterns."},
    {"id":"saa-015","cert":"SAA-C03","domain":"Design Secure Architectures",
     "question":"A company needs to give a mobile app temporary, limited access to upload to S3 without distributing AWS credentials. What is the BEST approach?",
     "options":["Create an IAM user per device","Use Amazon Cognito with IAM roles for temporary credentials","Make the bucket public","Share a single access key with all users"],
     "answer":1,
     "explanation":"Amazon Cognito federates identities and issues temporary, scoped AWS credentials via IAM roles, avoiding distribution of long-term keys and never requiring a public bucket."},

    # ── DVA-C02 ──────────────────────────────────────────────
    {"id":"dva-009","cert":"DVA-C02","domain":"Development with AWS Services",
     "question":"A Lambda function needs to process items from a DynamoDB table as they change. What should you configure?",
     "options":["A CloudWatch alarm on the table","A DynamoDB Stream as an event source for Lambda","An SNS topic on the table","API Gateway polling the table"],
     "answer":1,
     "explanation":"DynamoDB Streams capture item-level changes and can trigger a Lambda function via an event source mapping, enabling change-driven processing."},
    {"id":"dva-010","cert":"DVA-C02","domain":"Troubleshooting & Optimization",
     "question":"A developer wants distributed tracing across a microservices app on AWS to find latency bottlenecks. Which service helps?",
     "options":["AWS X-Ray","Amazon CloudWatch Logs","AWS Config","Amazon Inspector"],
     "answer":0,
     "explanation":"AWS X-Ray provides end-to-end distributed tracing, showing a service map and latency for each segment, ideal for locating bottlenecks in microservices."},
    {"id":"dva-011","cert":"DVA-C02","domain":"Security",
     "question":"What is the recommended way to store a database password used by a Lambda function, with automatic rotation?",
     "options":["Lambda environment variable in plaintext","AWS Secrets Manager","A hard-coded constant","An S3 object with public read"],
     "answer":1,
     "explanation":"AWS Secrets Manager securely stores secrets and supports automatic rotation. Plaintext environment variables and hard-coded values are insecure."},

    # ── SOA-C02 ──────────────────────────────────────────────
    {"id":"soa-006","cert":"SOA-C02","domain":"Monitoring, Logging & Remediation",
     "question":"Which service can automatically remediate a noncompliant resource configuration (e.g., an open security group) when detected?",
     "options":["AWS Config with remediation actions","Amazon CloudWatch Dashboards","AWS Cost Explorer","Amazon QuickSight"],
     "answer":0,
     "explanation":"AWS Config rules can detect noncompliant resources and trigger automatic remediation actions (via SSM Automation documents), such as removing an overly permissive rule."},
    {"id":"soa-007","cert":"SOA-C02","domain":"Deployment, Provisioning & Automation",
     "question":"An operator needs to apply an OS patch across hundreds of EC2 instances on a schedule without SSH. Which service is BEST?",
     "options":["AWS Systems Manager Patch Manager","AWS CodeDeploy","Amazon EventBridge","AWS Batch"],
     "answer":0,
     "explanation":"Systems Manager Patch Manager automates patching of managed instances on a schedule using maintenance windows, with no need for SSH or bastion hosts."},

    # ── SAP-C02 ──────────────────────────────────────────────
    {"id":"sap-005","cert":"SAP-C02","domain":"Design Solutions for Organizational Complexity",
     "question":"An enterprise wants to centrally govern multiple AWS accounts, apply guardrails, and consolidate billing. Which combination is BEST?",
     "options":["A single large account with many IAM users","AWS Organizations with Service Control Policies","Separate unrelated accounts with manual policies","AWS Config only"],
     "answer":1,
     "explanation":"AWS Organizations provides consolidated billing and centralized governance; Service Control Policies (SCPs) enforce guardrails across member accounts."},
    {"id":"sap-006","cert":"SAP-C02","domain":"Accelerate Workload Migration & Modernization",
     "question":"Which AWS service helps discover on-premises servers and their dependencies to plan a migration?",
     "options":["AWS Application Discovery Service","AWS DataSync","AWS Snowball","Amazon Macie"],
     "answer":0,
     "explanation":"AWS Application Discovery Service collects configuration and dependency data from on-premises servers to help plan migrations. DataSync/Snowball move data; Macie classifies sensitive data."},

    # ── DOP-C02 ──────────────────────────────────────────────
    {"id":"dop-005","cert":"DOP-C02","domain":"SDLC Automation",
     "question":"Which deployment strategy shifts a small percentage of traffic to a new version first to limit blast radius?",
     "options":["All-at-once","Canary","In-place full","Recreate"],
     "answer":1,
     "explanation":"A canary deployment routes a small share of traffic to the new version, monitors it, then gradually shifts the rest, limiting the impact of a bad release."},
    {"id":"dop-006","cert":"DOP-C02","domain":"Monitoring & Logging",
     "question":"You need a single view of metrics, logs, and traces plus automated alarms for a production app. Which combination is core to this on AWS?",
     "options":["CloudWatch (metrics/logs/alarms) with X-Ray tracing","Only S3 access logs","AWS Config rules","Amazon Inspector scans"],
     "answer":0,
     "explanation":"Amazon CloudWatch centralizes metrics, logs, dashboards, and alarms, while X-Ray adds distributed tracing, together providing full observability."},

    # ── SCS-C02 ──────────────────────────────────────────────
    {"id":"scs-005","cert":"SCS-C02","domain":"Threat Detection & Incident Response",
     "question":"Which service uses ML and threat intelligence to continuously detect malicious activity such as unusual API calls or crypto-mining?",
     "options":["Amazon GuardDuty","AWS WAF","AWS Shield Standard","Amazon Macie"],
     "answer":0,
     "explanation":"Amazon GuardDuty is a threat-detection service that analyzes CloudTrail, VPC Flow Logs, and DNS logs using ML to flag malicious or anomalous behavior."},
    {"id":"scs-006","cert":"SCS-C02","domain":"Data Protection",
     "question":"A team must ensure S3 objects are encrypted with keys they can audit and rotate, with usage logged in CloudTrail. Which option is BEST?",
     "options":["SSE-S3 (Amazon-managed keys)","SSE-KMS with a customer managed key","Client-side XOR obfuscation","No encryption, rely on bucket policy"],
     "answer":1,
     "explanation":"SSE-KMS with a customer managed key gives control over key policies, rotation, and detailed CloudTrail logging of key usage, satisfying audit requirements."},

    # ── ANS-C01 ──────────────────────────────────────────────
    {"id":"ans-005","cert":"ANS-C01","domain":"Network Connectivity",
     "question":"A company needs a private, dedicated, consistent-bandwidth connection between its data center and AWS. Which service provides this?",
     "options":["Site-to-Site VPN over the internet","AWS Direct Connect","VPC Peering","AWS PrivateLink"],
     "answer":1,
     "explanation":"AWS Direct Connect provides a dedicated private network connection with consistent bandwidth and lower latency than internet-based VPN. VPN is encrypted but rides the public internet."},
    {"id":"ans-006","cert":"ANS-C01","domain":"Network Design",
     "question":"To connect hundreds of VPCs and on-premises networks through a central hub, which service scales BEST?",
     "options":["VPC Peering mesh","AWS Transit Gateway","Individual VPN per VPC","Internet Gateway"],
     "answer":1,
     "explanation":"AWS Transit Gateway acts as a central hub connecting many VPCs and on-premises networks, avoiding the O(n^2) complexity of a full VPC peering mesh."},

    # ── AIF-C01 ──────────────────────────────────────────────
    {"id":"aif-005","cert":"AIF-C01","domain":"Fundamentals of AI and ML",
     "question":"Which term describes providing a few examples within a prompt to guide a foundation model's response?",
     "options":["Fine-tuning","Few-shot prompting","Pre-training","Reinforcement learning"],
     "answer":1,
     "explanation":"Few-shot prompting includes a small number of examples in the prompt to steer the model's output without changing its weights. Fine-tuning and pre-training modify the model itself."},
    {"id":"aif-006","cert":"AIF-C01","domain":"Applications of Foundation Models",
     "question":"Which AWS service provides access to multiple foundation models through a single API for building generative AI applications?",
     "options":["Amazon SageMaker Ground Truth","Amazon Bedrock","Amazon Comprehend","Amazon Rekognition"],
     "answer":1,
     "explanation":"Amazon Bedrock offers access to foundation models from multiple providers via a single API, with features like knowledge bases and agents for building GenAI apps."},
    {"id":"aif-007","cert":"AIF-C01","domain":"Guidelines for Responsible AI",
     "question":"Which practice helps reduce harmful or biased outputs from a generative AI application?",
     "options":["Disabling all logging","Implementing guardrails and content filtering","Removing human review entirely","Maximizing model temperature"],
     "answer":1,
     "explanation":"Guardrails and content filtering (e.g., Amazon Bedrock Guardrails) help block harmful, biased, or off-topic content, supporting responsible AI. Human oversight remains important."},

    # ── MLA-C01 ──────────────────────────────────────────────
    {"id":"mla-004","cert":"MLA-C01","domain":"ML Model Development",
     "question":"A model performs well on training data but poorly on new data. What is this called and one common fix?",
     "options":["Underfitting; add more layers","Overfitting; apply regularization or more data","Data leakage; increase learning rate","Vanishing gradient; remove validation set"],
     "answer":1,
     "explanation":"High training accuracy but poor generalization indicates overfitting. Common fixes include regularization, dropout, gathering more/representative data, or simplifying the model."},
    {"id":"mla-005","cert":"MLA-C01","domain":"Deployment & Orchestration of ML Workflows",
     "question":"Which Amazon SageMaker feature hosts a model for low-latency, real-time inference behind an HTTPS endpoint?",
     "options":["SageMaker Batch Transform","SageMaker Real-Time Endpoints","SageMaker Ground Truth","SageMaker Data Wrangler"],
     "answer":1,
     "explanation":"SageMaker Real-Time (hosted) Endpoints serve low-latency, synchronous inference over HTTPS. Batch Transform is for offline bulk inference."},

    # ── DEA-C01 ──────────────────────────────────────────────
    {"id":"dea-005","cert":"DEA-C01","domain":"Data Ingestion & Transformation",
     "question":"Which service is a serverless, fully managed extract-transform-load (ETL) service that can catalog data and run Spark jobs?",
     "options":["Amazon Athena","AWS Glue","Amazon Redshift","AWS Data Pipeline"],
     "answer":1,
     "explanation":"AWS Glue is a serverless ETL service with a data catalog and managed Apache Spark jobs. Athena queries data in place with SQL; Redshift is a data warehouse."},
    {"id":"dea-006","cert":"DEA-C01","domain":"Data Store Management",
     "question":"To run interactive SQL queries directly against data stored in Amazon S3 without loading it first, which service is BEST?",
     "options":["Amazon Athena","Amazon RDS","AWS Glue DataBrew","Amazon Kinesis"],
     "answer":0,
     "explanation":"Amazon Athena is a serverless, interactive query service that runs standard SQL directly against data in Amazon S3, with no infrastructure to manage."},

    # ── AIP-C01 ──────────────────────────────────────────────
    {"id":"aip-004","cert":"AIP-C01","domain":"Generative AI Application Design",
     "question":"Which technique augments a foundation model's responses with an organization's own documents at query time, without retraining?",
     "options":["Fine-tuning","Retrieval-Augmented Generation (RAG)","Pre-training from scratch","Quantization"],
     "answer":1,
     "explanation":"Retrieval-Augmented Generation (RAG) retrieves relevant documents (e.g., from a vector store or knowledge base) and adds them to the prompt, grounding responses without retraining."},
    {"id":"aip-005","cert":"AIP-C01","domain":"Responsible & Secure Generative AI",
     "question":"What does a vector embedding represent in a generative AI/RAG system?",
     "options":["A compressed image file","A numeric representation of text capturing semantic meaning","An IAM policy document","A billing record"],
     "answer":1,
     "explanation":"Embeddings are numeric vectors that capture the semantic meaning of text (or other data), enabling similarity search that powers retrieval in RAG systems."},
]


def key_ok(q):
    req = {"id","cert","domain","question","options","answer","explanation"}
    if not req.issubset(q):
        return f"missing keys: {req - set(q)}"
    if not isinstance(q["options"], list) or len(q["options"]) < 2:
        return "options must be a list of >=2"
    if not isinstance(q["answer"], int) or not (0 <= q["answer"] < len(q["options"])):
        return "answer index out of range"
    return None


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    existing = data.get("questions", [])
    have = {q["id"] for q in existing}

    added, errors = 0, 0
    for q in NEW:
        err = key_ok(q)
        if err:
            print(f"SKIP {q.get('id','?')}: {err}", file=sys.stderr); errors += 1; continue
        if q["id"] in have:
            continue
        existing.append(q); have.add(q["id"]); added += 1

    if errors:
        print(f"Aborting: {errors} invalid question(s).", file=sys.stderr)
        sys.exit(1)

    data["questions"] = existing
    import datetime
    data["updated"] = datetime.date.today().isoformat()
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Added {added} new question(s). Total now: {len(existing)}")


if __name__ == "__main__":
    main()
