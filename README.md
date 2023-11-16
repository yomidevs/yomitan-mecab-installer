# Yomitan MeCab Installer

Installs the files required to run [MeCab](https://taku910.github.io/) in [Yomitan](https://github.com/TheMoeWay/yomitan/).
Python and MeCab have to be installed separately.

## Installation

If you are running Mac, first install [Homebrew](https://brew.sh/), as it is used to install the dependencies.

1. Install Python
    - **Windows**: https://www.python.org/downloads/
    - **Mac**: Run `brew install python3`
    - **Linux**: Python is usually included with a Linux distribution
1. Install MeCab
    - **Windows**: https://taku910.github.io/mecab/#download (mecab-x.xxx.exe:ダウンロード)
    - **Mac**: run `brew install mecab`
    - **Linux**: package managers usually include MeCab. You don't need to install a dictionary package from the package manager, this script downloads the required dictionaries for you
1. [Download](https://github.com/starxeras/yomitan-mecab-installer/archive/master.zip) and extract this repository
to the location where you wish to install the files. `~/Downloads` might not be the best place
1. Run `install_mecab_for_yomitan.py` and follow the instructions
2. Go to the Yomitan settings page in the browser you selected.
3. Click `Advanced` in the bottom left corner.
4. Go to `Text Parsing`
5. Enable `Parse sentences using MeCab`
6. To check if you installed it correctly, click the `More...` button and select `Test`. If it returns "Connection was successful", MeCab is now installed for Yomitan.

Some things to note:
- If you try to run the installer for use on multiple browsers, it will not work. Only one browser can use the MeCab for Yomitan installation.
- If you wish to use MeCab on another browser, close the browser that has MeCab for Yomitan installed. If you do not do this, you will get a `Permission denied` error when running the script. 

![demo video](demo.gif)

You can move the install directory later, but you have to run the install again if you do that.
