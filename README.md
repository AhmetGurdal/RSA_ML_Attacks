RSA ML Attacks
===
## Thesis
- Title:  `Investigating the Attacks on the RSA Encryption Algorithm using Maching Learning`
- Author:  `Ahmet Gürdal`
<!-- - Paper: [https://arxiv.org/abs/xx]() -->

## Install & Dependence
- requirements.txt

## Locations
| Type | Location |
| ---  | ---      |
| Datasets | `./data/groups` |
| Processed Data | `./data/processed` |
| Models | `./data/models` |
| Graphs | `./data/figures` |

## Usage (CLI mode)

**_NOTE:_** In CLI mode, application can be stopped by entering "q" when a user input is requested!
- Start the application (CLI mode)
  ```
  python main.py
  ```
  To get detailed usage run
  ```
  python main.py -h|--help
  ```
- Select one of the dataset creating options
  - Create new dataset
  - Load processed dataset
- Select one of the listed unprocessed dataset group.
- Select data configuration type (You can also create your custom data processing type under `./src/dataConfigurations/` folder. )
- At the end of the dataset preparation process, you can save the processed data to later use.
- Select one of the model topology options
  - Train a new model with one of models listed ( You can also create your custom training model under `./src/topologies/` folder). After training with the selected topology, model can be saved under the 'Models' location
  - Load a pretrained model.
- After testing you can select to create and save the graph of falsely predicted bit positions and it will be under 'Graphs' location

## Training with GPU in Windows
- Install WSL2 linux distro
- Install CUDA and CUDNN
- Install docker in wsl2, [link](https://docs.docker.com/engine/install/ubuntu/)
- Apply docker nvidia configurations
```
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update

sudo apt-get install -y nvidia-container-toolkit

sudo nvidia-ctk runtime configure --runtime=docker

sudo systemctl restart docker
```
- Run the script in the project inside the distro (this will create the required container and install python dependencies needed.)
```
./docker.sh
```
- Connect to container and relocate to the project folder
```
docker exec -it gpu-test sh
cd /root/project
```

<!-- ## Pretrained model
| Model | Download |
| ---     | ---   |
| Model-1 | [download]() |
| Model-2 | [download]() |
| Model-3 | [download]() |

## Code Details -->

### Tested Platform
- software
  ```
  OS: Ubuntu 24.04 LTS
  Python: 3.11.0rc1
  numpy==1.26.4
  pandas==2.2.2
  matplotlib==3.9.0
  tensorflow==2.17.0
  ```
- hardware
  ```
  CPU: AMD Ryzen 5 5600
  GPU: Nvidia RTX4060 
  ```
<!-- ### Hyper parameters
```
```
  
## License -->

