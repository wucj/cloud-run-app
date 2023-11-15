#!/usr/bin/env python
import optparse
import os
import subprocess


def _get_version():
    prev_version, new_version = 1, 1
    if os.path.exists("./app/version"):
        with open("./app/version", "r") as f:
            temp = f.readline()
            if temp:
                prev_version = int(temp)
                new_version = prev_version + 1
            f.close()

    with open("./app/version", "w+") as f:
        f.write(str(new_version))
        f.close()
    return prev_version, new_version


def build_and_push_image(
    repo_address, project_name, repo_name, app_name, version, service_account
):
    run_command = f"docker build -t {repo_address}/{project_name}/{repo_name}/{app_name}:v{version} app"
    subprocess.call(run_command, shell=True)

    run_command = f"gcloud auth print-access-token --impersonate-service-account  {service_account} | docker login -u oauth2accesstoken --password-stdin https://{repo_address}"
    subprocess.call(run_command, shell=True)

    run_command = (
        f"docker push {repo_address}/{project_name}/{repo_name}/{app_name}:v{version}"
    )
    subprocess.call(run_command, shell=True)


def check_and_get_env_vars():
    is_valid = True
    project_name = os.environ.get("GCP_PROJECT_NAME")
    if not project_name:
        print("Please set up GCP_PROJECT_NAME")
        is_valid = False
    service_account = os.environ.get("GCP_AR_EDITOR")
    if not service_account:
        print("Please set the service account name for docker image upload.")
        is_valid = False
    region_name = os.environ.get("GCP_REGION")
    if not region_name:
        print("Please set up the GCP region.")
        is_valid = False
    repo_address = os.environ.get("GCP_AR_LOCATION")
    if not repo_address:
        print(
            "Please add location of GCP Artifact Registry, ex: us-east1-docker.pkg.dev"
        )
        is_valid = False
    repo_name = os.environ.get("GCP_AR_NAME")
    if not repo_name:
        print("Please set the repo name, ex: calculator")
        is_valid = False
    app_name = os.environ.get("APP_NAME")
    if not app_name:
        print("Please set the image name, ex: webapp")
        is_valid = False

    return (
        is_valid,
        project_name,
        service_account,
        region_name,
        repo_address,
        repo_name,
        app_name,
    )


def build_and_deploy():
    (
        is_valid,
        project_name,
        service_account,
        region_name,
        repo_address,
        repo_name,
        app_name,
    ) = check_and_get_env_vars()
    if not is_valid:
        return

    prev_version, new_version = _get_version()

    build_and_push_image(
        repo_address, project_name, repo_name, app_name, new_version, service_account
    )

    run_command = f"sed -i 's/v{prev_version}/v{new_version}/g' service.yaml"
    subprocess.call(run_command, shell=True)

    run_command = f"gcloud run services replace service.yaml --project={project_name}"
    subprocess.call(run_command, shell=True)


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option(
        "-d",
        "--deploy",
        dest="deploy",
        default="",
        action="store_true",
        help="Deploy cloud run services",
    )

    options, remainder = parser.parse_args()

    if options.deploy:
        if options.deploy == "image":
            build_and_push_image()
        elif options.deploy == "all":
            build_and_deploy()
        else:
            print("Options should be (all or image)")
