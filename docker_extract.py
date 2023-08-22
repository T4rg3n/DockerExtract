logo_ascii = """
  _____             _             ______      _                  _   
 |  __ \           | |           |  ____|    | |                | |  
 | |  | | ___   ___| | _____ _ __| |__  __  _| |_ _ __ __ _  ___| |_ 
 | |  | |/ _ \ / __| |/ / _ \ '__|  __| \ \/ / __| '__/ _` |/ __| __|
 | |__| | (_) | (__|   <  __/ |  | |____ >  <| |_| | | (_| | (__| |_ 
 |_____/ \___/ \___|_|\_\___|_|  |______/_/\_\\__|_|  \__,_|\___|\__|
                                                                                                                                 
"""
version = "1.0"

class StartCheckError(Exception):
    pass

def check_docker_hub_connectivity():
    try:
        subprocess.run(["docker", "info"], check=True)
        print("Connected to Docker Hub.")
    except StartCheckError as e:
        print("Failed to connect to Docker Hub.")

def check_pull_images(image_names):
    for image_name in image_names:
        try:
            subprocess.run(["docker", "pull", image_name], check=True)
            print(f"Pulled image: {image_name}")
        except StartCheckError as e:
            print(f"Failed to pull image: {image_name}")

def check_docker_compose():
    try:
        subprocess.run(["docker-compose", "version"], check=True)
        print("docker-compose is working.")
    except StartCheckError as e:
        print("docker-compose is not working.")

def check_docker_run():
    try:
        subprocess.run(["docker", "run", "--rm", "hello-world"], check=True)
        print("Docker is able to run containers.")
    except StartCheckError as e:
        print("Docker is not able to run containers.")

def start_check():
  try:
    check_docker_hub_connectivity()
    image_names = ["hello-world"]
    check_pull_images(image_names)
    check_docker_compose()
    check_docker_run()
    os.system("cls")
    print(logo_ascii + "Version: " + version)
    print("All checks passed.")
  except StartCheckError as e:
    print("Failed checks.")
    exit()

def load_yaml(file):
  with open(file, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

def extract_images_name(yaml): 
  image_names = []
  
  for service_name, service_data in yaml.get("services", {}).items():
    image_name = service_data.get("image")
    if image_name:
        image_names.append(image_name)
  return image_names

def sanitize_image_name(image_name):
    translation_table = str.maketrans("/:", "__")
    sanitized_image_name = image_name.translate(translation_table)
    return sanitized_image_name

def main():
  print(logo_ascii + "Version: " + version)
  
  # Start checks
  print("\nDo you want to start the checks? (y/n)")
  answer = input()
  if answer == "y":
    print("Starting checks...")
    start_check()
  
  # Load docker-compose.yml
  try:
    yaml = load_yaml("docker-compose.yml")
  except:
    print("Failed to load docker-compose.yml \n Place it in the same directory as this script.")
    exit()
  image_names = extract_images_name(yaml)
  
  # Pull images
  print("\nImages found in file: ")
  for index, image_name in enumerate(image_names, start=1):
    print(f"{index}. {image_name}")
  
  print("\nDo you want to pull these images? (y/n)")
  answer = input()
  if answer == "y":
    print("Pulling images...")
    for image_name in image_names:
      print("Pulling image: " + image_name)
      os.system("docker pull " + image_name)
  else:
    print("Skipping...")
  
  # Extract image names from docker-compose.yml to tar files
  print("\nDo you want to extract the images to tar files? (y/n)")
  answer = input()
  if answer == "y":
    print("Extracting images...")
    for image_name in image_names:
      print("Extracting image: " + image_name)
      if not os.path.exists("images"):
        os.system("mkdir images")
      os.system("docker save " + image_name + " > " + "images/" + sanitize_image_name(image_name) + ".tar")
  else:
    print("Skipping...")
    
  # Make a command to load the tar files
  print("\nDo you want to make a command to load the tar files? (y/n)")
  answer = input()
  if answer == "y":
    print("Making command...")
    command = ""
    for image_name in image_names:
      command += "docker load -i " + sanitize_image_name(image_name) + ".tar && "
    print("Command: \n" + command[:-3])
  else:
    print("Skipping...")
  
if __name__ == "__main__":
  try:
    import yaml
    import os
    import subprocess
  except ImportError:
    print("One or more required packages are missing. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Required packages installed. You can now run the script.")
    exit(0)
  
  main()