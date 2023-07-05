# Cloud Resume Challenge - Backend

Repo containing code for the Backend part of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/).

## Description

A resume page built using Next.js and TailwindCSS. The page also includes a visitor counter which updates at every visit. Its value is stored in a DynamoDB table and dynamically retrieved via API Gateway and Lambda.

## Architecture
- DynamoDB table storing the current visitor count.
- API Gateway receiveing requests from the Frontend.
- Lambda function triggered by API Gateway endpoint updating/retrieving the visitor count from the DynamoDB table.

----
----> **Work In Progress**
---