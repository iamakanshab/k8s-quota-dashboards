from k8s import client, config

def get_namespace_metrics(namespace):
    """Get resource usage metrics for a given namespace."""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    pods = v1.list_namespaced_pod(namespace)
    usage = {
        "cpu": 0,
        "memory": 0
    }
    
    for pod in pods.items:
        for container in pod.spec.containers:
            resources = container.resources.requests
            usage['cpu'] += int(resources['cpu'].replace('m', ''))  # Convert millicores
            usage['memory'] += int(resources['memory'].replace('Mi', ''))  # Convert MiB
    
    return usage

if __name__ == "__main__":
    namespace = "default"
    print(f"Metrics for {namespace}: {get_namespace_metrics(namespace)}")
