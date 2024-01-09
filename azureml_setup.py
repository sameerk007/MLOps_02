import argparse
from tqdm import tqdm
from pprint import pprint
from azureml.core import Workspace
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.compute_target import ComputeTargetException


def main():
    parser = argparse.ArgumentParser(
        description="A command-line script to handle AzureML resources."
    )
    parser.add_argument(
        "-c",
        "--create",
        help="USE : --create <name> Create A compute resurce with <name>",
    )
    parser.add_argument(
        "-d",
        "--delete",
        help="USE : --delete <name> Delete A compute resurce with <name>",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="Lists all the compute target available in the workspace",
    )

    args = parser.parse_args()

    
    if args.list:
        with tqdm(total=2, desc="Fetching") as pbar:
            ws = Workspace.from_config()
            pbar.update(1)
            compute_targets = ws.compute_targets
            pbar.update(1)
        pprint(str(compute_targets))


    if args.delete:
        cpu_cluster_name = args.delete
        try : 
            ws = Workspace.from_config()
            cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
            cpu_cluster.delete()
            pprint(f"{cpu_cluster_name} is beign deleted.")
        except ComputeTargetException as e:
            print(e.message)


        

    if args.create:
        cpu_cluster_name = args.create
        try:
            ws = Workspace.from_config()
            cpu_cluster = ComputeTarget(workspace=ws, name=cpu_cluster_name)
            pprint(f"Found existing cluster '{cpu_cluster_name}', Use it.")
        except ComputeTargetException:
            compute_config = AmlCompute.provisioning_configuration(
                vm_size="STANDARD_D2_V2",
                min_nodes=0,
                max_nodes=4,
                idle_seconds_before_scaledown=2400,
            )
            cpu_cluster = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

            cpu_cluster.wait_for_completion(show_output=True)




if __name__ == "__main__":
    main()
