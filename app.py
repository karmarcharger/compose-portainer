from flask import Flask, request, render_template
import yaml
import json
import gc

app = Flask(__name__)

def convert_docker_compose_to_portainer_template(compose_yml):
    try:
        compose_data = yaml.load(compose_yml, Loader=yaml.FullLoader)

        portainer_template = {
            "version": "2",
            "templates": []
        }

        for service_name, service_config in compose_data["services"].items():
            portainer_service = {
                "image": service_config.get("image", ""),
                "volumes": [],
                "environment": [],
                "networks": [],
                "labels": [],
                "ports": []
            }

            # Add volume mounts
            for volume in service_config.get("volumes", []):
                portainer_service["volumes"].append({
                    "bind": "/path/to/host/mount",  # Modify this path as needed
                    "container": volume
                })

            # Extract environment variables
            for env in service_config.get("environment", []):
                key, value = env.split('=')
                portainer_service["environment"].append({
                    "name": key,
                    "label": key,
                    "default": value,
                    "description": f"Environment variable for {key}"
                })

            # Add networks
            for network in service_config.get("networks", []):
                portainer_service["networks"].append(network)

            # Add labels
            for label in service_config.get("labels", []):
                key, value = label.split('=')
                portainer_service["labels"].append({"name": key, "value": value})

            # Add port mappings
            ports = service_config.get("ports", [])
            if ports:
                for port in ports:
                    portainer_service["ports"].append(port)

            # Extract or default the restart policy
            restart_policy = service_config.get("restart", "unless-stopped")

            # Create a Portainer template entry for the service
            template_entry = {
                "categories": ["Other", "Tools"],
                "env": portainer_service["environment"],
                "description": f"Description for {service_name}",
                "image": portainer_service["image"],
                "logo": "https://example.com/logo.png",  # Modify this URL
                "name": service_name,
                "platform": "linux",
                "ports": portainer_service["ports"],
                "restart_policy": restart_policy,
                "title": service_name,
                "type": 1,
                "volumes": portainer_service["volumes"],
                "note": "<b>Template created by Your Name</b><br><b>Additional notes here</b>"
            }

            portainer_template["templates"].append(template_entry)
            gc.collect()
        return json.dumps(portainer_template, indent=2)
    except Exception as e:
        gc.collect()
        return "Error parsing Docker Compose YAML"


@app.route("/", methods=["GET", "POST"])
def convert_compose_to_portainer():
    if request.method == "POST":
        compose_yml = request.form.get("compose_yml")
        if compose_yml:
            portainer_json = convert_docker_compose_to_portainer_template(compose_yml)
            return render_template("index.html", compose_yml=compose_yml, portainer_json=portainer_json)

    return render_template("index.html")

if __name__ == "__main__":

    app.run(host="0.0.0.0",debug=False, port=8082)
