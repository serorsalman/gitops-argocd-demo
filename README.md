# gitops-argocd-demo

> **Portfolio demonstration project.** This is not affiliated with any employer and contains no employer code or data. It was built to showcase GitOps, Argo CD, and Kustomize skills.

A tiny Flask app deployed the GitOps way: the desired state lives in this repo, Kustomize builds one overlay per environment, and Argo CD syncs each overlay into the cluster automatically.

## How the flow works

```
git push
  └─ Argo CD notices the change (HEAD of main)
       ├─ k8s/overlays/dev     → namespace demo-dev     (1 replica)
       ├─ k8s/overlays/staging → namespace demo-staging (2 replicas)
       └─ k8s/overlays/prod    → namespace demo-prod    (3 replicas)
```

- `k8s/base` holds the shared Deployment and Service.
- Each overlay adds its namespace, name prefix, `env` label, replica count, image tag, and the `ENVIRONMENT` variable — nothing is duplicated.
- `argocd/*.yaml` are Argo CD `Application` manifests with automated sync, prune, and self-heal enabled.

## The app

`app/` is a trivial Flask service with two endpoints:

- `GET /` returns a hello message and the environment name.
- `GET /healthz` is the liveness/readiness probe.

## Run it locally (kind)

```bash
# 1. Start a local cluster
kind create cluster --name gitops-demo

# 2. Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Build and load the app image into kind
docker build -t ghcr.io/serorromero/gitops-demo-app:dev ./app
kind load docker-image ghcr.io/serorromero/gitops-demo-app:dev --name gitops-demo

# 4. Point Argo CD at this repo and apply the dev application
kubectl apply -f argocd/dev.yaml

# 5. Watch it sync, then curl the service
kubectl -n demo-dev get pods
kubectl -n demo-dev port-forward svc/dev-demo-app 8080:80
curl localhost:8080/
```

Promoting a change is a normal Git workflow: edit the base or an overlay, commit, push — Argo CD picks it up and syncs it. To promote the same image through the environments, update the `newTag` in each overlay's `kustomization.yaml`.

## Files

| Path | Purpose |
|---|---|
| `app/` | Flask demo app + Dockerfile |
| `k8s/base/` | Shared Deployment, Service, Kustomization |
| `k8s/overlays/{dev,staging,prod}/` | Per-environment Kustomize overlays |
| `argocd/` | Argo CD Application manifests (one per environment) |
