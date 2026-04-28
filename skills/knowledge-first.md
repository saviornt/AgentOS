# Knowledge First Workflow

When answering any technical question:

## Step 1 — Check MongoDB

Query stored knowledge first.

## Step 2 — If found

Return cached answer.

## Step 3 — If NOT found

1. Use SearXNG MCP
2. Gather latest information
3. Validate against multiple sources
4. Store result in MongoDB

## Step 4 — Update Redis state

Log:

- query
- result source
- timestamp
