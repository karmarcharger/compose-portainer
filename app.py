from flask import Flask, request, render_template
import yaml
import json
import gc

app = Flask(__name__)

def convert_docker_compose_to_portainer_template(compose_yml, note, logo, description, name, categories):
    try:
        compose_data = yaml.load(compose_yml, Loader=yaml.FullLoader)

        # Split user-provided categories by commas if input is not empty
        category_list = [c.strip() for c in categories.split(',')] if categories else []

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
                parts = volume.split(':')
                if len(parts) == 2:
                    container_path = parts[1]
                else:
                    container_path = volume

                portainer_service["volumes"].append({
                    "bind": f"/portainer/Files/AppData/Config/{service_name}",  # Use the service_name in bind path
                    "container": container_path  # Use the second value when split by ":"
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

            # Use the provided name or default to the service_name
            service_name = name if name else service_name

            # Create a Portainer template entry for the service
            template_entry = {
                "categories": category_list,
                "env": portainer_service["environment"],
                "description": description,
                "image": portainer_service["image"],
                "logo": logo,
                "name": service_name,
                "platform": "linux",
                "ports": portainer_service["ports"],
                "restart_policy": restart_policy,
                "title": service_name,
                "type": 1,
                "volumes": portainer_service["volumes"],
                "note": note
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
        note = request.form.get("note")
        logo = request.form.get("logo")
        description = request.form.get("description")
        name = request.form.get("name")
        categories = request.form.get("categories")
        if compose_yml:
            portainer_json = convert_docker_compose_to_portainer_template(compose_yml, note, logo, description, name, categories)
            return render_template("index.html", compose_yml=compose_yml, portainer_json=portainer_json)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8082)
