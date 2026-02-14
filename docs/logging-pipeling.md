# CountIQ's Logging pipeline (runtime + deployment)

flowchart LR
  A[Django emits structured event dict]
    --> B[Python logging system]
    --> C[JSON formatter]
    --> D[stdout/stderr stream]
    --> E[Docker logging capture]
    --> F[AWS CloudWatch aggregation]
    --> G[Search / alerts / dashboards]
