# Yomitan MeCab Installer

🇯🇵 *This is for Japanese only.*

[MeCab](https://taku910.github.io/) is a third-party program which uses its own dictionaries and parsing algorithm to decompose Japanese sentences into individual words. MeCab may produce more accurate parsing results than Yomitan’s own internal parser.

##❗ **Note** ❗
MeCab is only used on the search page of Yomitan and is therefore mostly useless. Back in the stone ages of Yomichan, there was no internal parser for the search page and thus MeCab was the only option. In the modern era, there is little to no reason to install it, but it is an option nonetheless!

## ⏬ Installation

Note: [Homebrew](https://brew.sh/) is required for Mac devices.

1. Install Python.
    - Windows: https://www.python.org/downloads/ 
         - [Chocolately](https://chocolatey.org/): `choco install python`
    - Mac: Run `brew install python3`
    - Linux: Python is usually included with your distribution.
2. Install MeCab.
    - Windows: https://taku910.github.io/mecab/#download (In the `Binary package for MS-Windows` header.)
    - Mac: Simply run `brew install mecab`.
    - Linux: It depends on your distribution, but most package managers have mecab as a package. Search around for your specific distribution. Make sure to install the dictionary that comes with it, though.
        - Ubuntu: `sudo apt install mecab mecab-ipadic-utf8`
        - Fedora: `sudo dnf install mecab mecab-ipadic`
        - Arch: `sudo pacman -S mecab-git mecab-ipadic`
3. [Download](https://github.com/yomidevs/yomitan-mecab-installer/archive/master.zip) and extract this repository to the location you wish to install the files.
    - ❗Your downloads folder might not be the best place, as the dictionary files are stored in the same directory.
4. Open the directory in a terminal and run `python -m venv .venv`
5. Then, you must source into the virtual environment
   - For Windows, run `.\.venv\Scripts\activate.bat` in the terminal.
   - For Linux and probably macOS too, run `source .venv/bin/activate`.
6. Now that you're sourced into the venv, install the requirements: `pip install -r requirements.txt`
7. And with that, run the script! `python install_mecab_for_yomitan.py` Proceed with the instructions given.
   - ❗❗ **If you use Firefox or have built Yomitan from source, please refer to the [How to find your extension ID](README.md#-how-to-find-your-extension-id) section below.**
8. Go to the Yomitan settings page on your browser.
9. Enable advanced options by clicking the toggle switch in the bottom left corner.
10. Go to `Text Parsing`.
11. Enable `Parse sentences using MeCab` and click `More...`.
12. Click the `Test` button to see if MeCab was installed correctly.
    - `Connection was successful.` - MeCab is now installed, congratulations.
    - `Could not connect to native MeCab component` - Something went wrong. Please refer to the [Notes](README.md#notes) section and the [FAQ](README.md#faq).

## ❓ How to find your extension ID

If you are a Firefox user and/or have built Yomitan from source, you need to obtain the extension ID for Yomitan. If you reinstall Yomitan, MeCab may no longer work for you in this case.
- Chrome/Chromium/Edge:
    - Open up your Yomitan settings page. The URL should look something like this:
    - ![image](https://github.com/user-attachments/assets/4f87be39-6cb4-45df-a9a7-09fb9a177c1d)
    - (Note: On Edge, the prefix will be `extension://`. **Make sure to change this to `chrome-extension://`, otherwise it will not work.**)
    - Copy everything before `settings.html`. For example: `chrome-extension://mbclianmdhnmblbfecpefmgjhajbioip/`.
    - ❗***Make sure to remember the `chrome-extension://` AND the `/` at the end of the ID!!***
    - Then, rerun the script as seen above and when it displays `Add more extension IDs`, paste the extension ID URL that you got. It should work. Continue with the tutorial.
- Firefox:
    - Go to `about:debugging`, then select `This Firefox` at the sidebar.
    - Scroll until you find Yomitan. It should look like this:
    - ![image](https://github.com/user-attachments/assets/f4522553-d1cf-46dd-b1cf-e75efd3089ed)
    - Now, copy the `Extension ID`. For example: `{2d13e145-294e-4ead-9bce-b4644b203a00}`.
    - Rerun the script as seen above and when it displays `Add more extension IDs`, paste the extension ID **with the brackets** in the input. It should work. Continue with the tutorial.

## FAQ

*Why is firefox different?* 

- That's because, from what I've seen, Firefox gives a unique extension ID for every user, instead of one global one like in the Chrome store. This makes it much trickier to install MeCab.

## Notes
- If you try to run the installer again for use on multiple browsers, it will not work. You have to duplicate the repository folder. 
- If you wish to use MeCab on another browser (replacing the old one, same folder), close the browser that has MeCab for Yomitan installed. If you do not do this, you will get a Permission denied error when running the script.
- Try to close and reopen your browser if it isn't showing `Connection was successful.`.

- If you have any particular issues with installing MeCab, make an issue request. I'll try to help you as fast as possible.

