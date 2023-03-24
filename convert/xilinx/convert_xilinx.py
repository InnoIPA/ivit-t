import sys, os, shutil, logging, time
from argparse import ArgumentParser, SUPPRESS
# Append to API
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]/"common"))
from logger import config_logger
from utils import read_json, write_json
from convert_cls import convert_cls
from convert_yolo import convert_yolo

# def cmd(command):
# 	logging.info(command.split())
# 	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=False)
# 	for line in iter(process.stdout.readline,b''):
# 		line = line.rstrip().decode()
# 		if line.isspace(): 
# 			continue
# 		else:
# 			logging.info(line)

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-c', '--config', required=True, help = "The path of model config")
    return parser

def main(args):
    # Read model_json
    model_dict = read_json(args.config)
    model_list = os.listdir(model_dict["train_config"]["save_model_path"])
    model_name = [best for best in model_list if "best" in best][0]
    input_model = model_dict["train_config"]["save_model_path"] +'/'+ model_name
    output_dir = model_dict["train_config"]["save_model_path"]+'/xilinx_model'
    export_dir = model_dict["train_config"]["save_model_path"].split("weights")[0]+'export'
    shape =  model_dict["model_config"]["input_shape"]
    shape_str = "{},{},{}".format(shape[0],shape[1],shape[2])
    project_name = args.config.split("project/")[-1].split("/")[0]
    start = time.time()

	# Create target Directory
    if os.path.isdir(export_dir):
        shutil.rmtree(export_dir)
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    try:
        os.makedirs(output_dir, exist_ok=True, mode=0o777)
        os.makedirs(export_dir, exist_ok=True, mode=0o777)

    except Exception as exc:
        logging.warn(exc)
        pass

    # tensorflow 2 convert		
    if "classification" in args.config:
        convert_cls(input_model, output_dir, export_dir, project_name, model_dict, args.config, shape, shape_str)

    elif "yolo" in args.config:
        convert_yolo(input_model, output_dir, export_dir, project_name, model_dict, args.config, shape, shape_str)

	# Computing time
    end = time.time()
    logging.info("Converting total time:{}".format(end - start))

if __name__ == '__main__':
    config_logger('./convert.log', 'a', "info")
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)


