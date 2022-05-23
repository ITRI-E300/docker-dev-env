import argparse
import requests
import json
import os
import sys 
from pprint import pprint
from getpass import getpass
from loguru import logger
assert sys.version_info >= (3,5)
from pathlib import Path

def arg_parser_error_handler(message):
    print(message,"\n")
    print("use --help to check avaliable command")
    print("more info: https://github.com/ITRI-E300/docker-dev-env")

parser = argparse.ArgumentParser(add_help=True,usage='%(prog)s action\nmore info: https://github.com/ITRI-E300/docker-dev-env')
parser.add_argument("action", help="select one of: {list|create|update}")
parser.add_argument('--dry-run','-d',action='store_true')
parser.error = arg_parser_error_handler
args = parser.parse_args()
# print(args)


if not os.path.isfile(os.path.join(Path.home(),'.denv.conf.json')):
    logger.warning(f'`.denv.conf.json` not detect under `{Path.home()}`')
    conf = {}
else:
    with open(os.path.join(Path.home(),'.denv.conf.json'),'r',encoding='utf-8') as f:
        conf = json.load(f)
    # pprint(conf)
    # print()

def get_image_infos():
    r = requests.get('https://registry.hub.docker.com/v2/repositories/e300nlp/dev-env/tags')
    return json.loads(r.text),r.status_code

def list_image_tags():
    images_tags = []
    images,_ = get_image_infos()
    images = images.get('results',[])
    for image in images:
        last_updater_username = image['last_updater_username']
        image_name = image['name']
        # print("%s/%s"%(last_updater_username,image_name))
        images_tags.append("%s/dev-env:%s"%(last_updater_username,image_name))
    return images_tags

def create_container():
    user_options = {}
    #
    image_tags = list_image_tags()
    for i,image_tag in enumerate(image_tags):
        print("[%d] %s"%(i+1,image_tag))
    select_image_id = int(input("Select base image:"))
    select_image_tag = image_tags[select_image_id-1]
    user_options['select_image_tag'] = select_image_tag
    
    #
    use_gpu = input("Enable GPUs? y/n:")
    if(use_gpu == 'y'):
        use_gpu = True
    else:
        use_gpu = False
    user_options['use_gpu'] = use_gpu
    if(use_gpu):
        gpu_ids = input("Assign GPUs for container (by GPU id) e.g. 0 or 0,1 or all:")
        assert gpu_ids != ''
        user_options['gpu_ids'] = gpu_ids

    # user account
    user_options['username'] = input('username:')
    user_options['password'] = getpass('password:')

    # service
    ssh_port = input("ssh port:")
    user_options['ssh_porting'] = '-p %s:22'%ssh_port
    jupyter_port = input("jupyter port:")
    user_options['jupyter_porting'] = '-p %s:8888'%jupyter_port
    vscode_port = input("vscode port:")
    user_options['vscode_porting'] = '-p %s:8080'%vscode_port

    # create volume
    is_create_volume = input('create volume? (mount at /user_data) y/n:')
    if(is_create_volume == 'y'):
        is_create_volume = True
        print('volume name will same as your username, and mount at /user_data')
        create_volume(user_options['username'])
    else:
        is_create_volume = False
    user_options['create_volume'] = is_create_volume

    # auto restart
    auto_restart = input('container auto restart? y/n:')
    if(auto_restart == 'y'):
        auto_restart = True
    else:
        auto_restart = False
    user_options['auto_restart'] = auto_restart 

    # docker run options
    docker_run_options = input('any other options for images? e.g "-p 1234:1234 -p 1235:1235":')
    user_options['docker_run_options'] = docker_run_options
    print(user_options)

    # create docker run cmd
    _docker_run_options = ''
    if(user_options['use_gpu'] == True):
        _docker_run_options+='--gpus %s '%user_options['gpu_ids']
    if(user_options['create_volume'] == True):
        _docker_run_options+='-v %s:/user_data '%user_options['username']
    if(user_options['auto_restart'] == True):
        _docker_run_options+='--restart=always '
    #
    _docker_run_options += '--name=%s '%(user_options['username'])
    _docker_run_options += '-e"NAME"=%s '%(user_options['username'])
    _docker_run_options += '-e"PASSWORD"=%s '%(user_options['password'])

    docker_run_cmd = "docker run -itd %s %s %s %s %s %s"%(\
        _docker_run_options,\
        user_options['docker_run_options'],\
        user_options['ssh_porting'],\
        user_options['jupyter_porting'],\
        user_options['vscode_porting'],\
        user_options['select_image_tag']
    )

    if args.dry_run:
        print("$",docker_run_cmd)
    else:
        print("$",docker_run_cmd)
        os.system(docker_run_cmd)
    

def create_volume(volume_name=None):    
    # step 1: setect device (depend on conf)
    candidate_device = conf.get('device',{})
    print("Select device (where to save volume)")
    print("[0]","* docker default *")

    for i,(d_name,d_path) in enumerate(candidate_device.items()):
        print(f"[{i+1}]",d_name,d_path)

    select_device = int(input("Select a device:"))

    if select_device != 0:
        select_device_name,select_device_path = list(candidate_device.items())[select_device-1]
        # print(f"pick: {select_device_path}")

    # step 2: assign volume name
    if volume_name is None:
        volume_name = input("Set a volume name:")
    
    if select_device !=0:
        new_volume_path = os.path.join(select_device_path,volume_name)
        assert not os.path.isdir(new_volume_path),'dir already exist, please use another `volume_name` or change device'
        os.makedirs(new_volume_path,exist_ok=True)
        
        docker_run_cmd = f"docker volume create --name {volume_name} --opt type=none --opt device={new_volume_path} --opt o=bind"
        print("$",docker_run_cmd)
        if not args.dry_run:
            os.system(docker_run_cmd)
    else:
        docker_run_cmd = f"docker volume create --name {volume_name} --opt type=none --opt o=bind"
        print("$",docker_run_cmd)
        if not args.dry_run:
            os.system(docker_run_cmd)

    return volume_name
    
def update_images():
    image_tags = list_image_tags()
    for i,image_tag in enumerate(image_tags):
        print("[%d] %s"%(i+1,image_tag))
    update_image_id =  int(input('which image to update?'))-1

    docker_run_cmd = 'docker pull %s'%image_tags[update_image_id]
    if args.dry_run:
        print("$",docker_run_cmd)
    else:
        print("$",docker_run_cmd)
        os.system(docker_run_cmd)

def main():
    if(args.action == 'list'):
        image_tags = list_image_tags()
        for tag in image_tags:
            print(tag)

    elif(args.action == 'create'):
        create_container()
    
    elif(args.action == 'create_volume'):
        create_volume()
    
    elif(args.action == 'update'):
        update_images()
