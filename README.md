# braille-machine
This academic project implements an application to convert Braille images to speech and Speech to Braille text.

## Installation
1. Clone the GitHub repository:
```
git clone git@github.com:hgky95/braille-machine.git
```

2. Open your command line and run below command to create virtual environment:
```
cd braille-machine
python -m venv .venv
```

3. Activate the virtual environment

- On windows:
```
.venv/Scripts/activate
```

- On Unix/Mac:
```
source .venv/bin/activate
```

4. Install library dependencies:
```
pip install -r requirements.txt
```

5. Run the application:
```
python main.py
```

## Acknowledgement
This project is developed based on the [Braille from AaditT](https://github.com/AaditT/braille) 
and [Braille from MarynaLongnickel](https://github.com/MarynaLongnickel/Braille) with some customization to fit with the scope of the project.

## Identified issues on Braille Image to Braille Text:
- Requires precise dimensions and alignment in input images for accurate translation.
- Adjustments to tolerance levels and image size may be necessary, depending on image
resolution and braille dot size.
