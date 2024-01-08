def get_secret_pod_mapping(pod_list):
    """Create a mapping between secret names and the pods that use them 
    in a given list of pod.
    This function iterates through a list of Kubernets pods and extracts information 
    about the secrets each pod uses.
    
    Args:
        pod_list (Kubernetes obj): A list of Kubernetes pod objects.
         
    Returns:
        dict: A dictionary where keys are secret names and values are lists of pod 
             names that use the corresponding secret. """
    secretName_to_pod_mapping = {}
    for pod in pod_list.items:
        for container in pod.spec.containers:
            if container.env:
             for env_var in container.env:
                 if env_var.value_from and env_var.value_from.secret_key_ref:
                     secret_name = env_var.value_from.secret_key_ref.name
                     if secret_name in secretName_to_pod_mapping:
                        # Each pod uses the same secret for different configuration. To remove duplicates pod 
                        # check if the pod already exist in the secret_to_pod_mapping[secret_name] list
                        if pod.metadata.name not in secretName_to_pod_mapping[secret_name]:
                         secretName_to_pod_mapping[secret_name].append(pod.metadata.name)
                     else:
                         secretName_to_pod_mapping[secret_name] = [pod.metadata.name]
    return secretName_to_pod_mapping