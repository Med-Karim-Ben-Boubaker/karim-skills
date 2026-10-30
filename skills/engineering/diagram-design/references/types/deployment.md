# Deployment

**Answers:** what runs where, how many, and behind which boundary. Use it when the code holds the answer: Dockerfiles, compose files, Kubernetes manifests, Terraform, CI jobs, cron schedules.

## Layout

- **Groups are real boundaries**: an environment, a network, a cluster, a cloud account. `dashed` for logical boundaries, solid for network ones.
- Nodes are what runs: containers, jobs, functions, managed services. Sublabel is the image or artifact with its version (`etl:1.4.2`). Replicas are a `badge` (`×3`), never repeated boxes.
- Managed services (Postgres, S3, a queue) are `db` or icon nodes in the group of the account that owns them, not inside the network that reaches them.
- Edges are network paths labelled with protocol and port in `mono` (`TLS :5432`). A path that crosses a boundary takes `data-color="blue"`.
- `data-src` cites the manifest line that declares each node and port.

## Budget

≤ 3 boundaries, ≤ 6 nodes, ≤ 8 paths.

## Avoid

- The logical architecture with hostnames added: if no placement is visible, draw architecture instead.
- Two environments in one figure: one figure per environment.
