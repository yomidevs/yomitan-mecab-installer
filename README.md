# Yomitan MeCab Installer

🇯🇵 *This is for Japanese only.*

[MeCab](https://taku910.github.io/) is a third-party program which uses its own dictionaries and parsing algorithm to decompose Japanese sentences into individual words. MeCab may produce more accurate parsing results than Yomitan’s own internal parser.

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
        <small>Note: these aren't tested commands, as I don't use Linux personally. If there are any problems with the commands, please submit an issue or a PR.</small>
3. [Download](https://github.com/themoeway/yomitan-mecab-installer/archive/master.zip) and extract this repository to the location you wish to install the files.
    - *Important*: Your downloads folder might not be the best place, as the dictionary files are stored in the same directory.
4. Open the directory in a terminal and run `py install_mecab_for_yomitan.py` and follow the instructions.
    - ❗If you are using Firefox or built Yomitan from source, please refer to the **How to find your extension ID.** header below.
5. Go to the Yomitan settings page on your browser.
6. Enable advanced options by clicking the toggle switch in the bottom left corner.
7. Go to `Text Parsing`.
8. Enable `Parse sentences using MeCab` and click `More...`.
9. Click the `Test` button to see if MeCab was installed correctly.
    - `Connection was successful.` - MeCab is now installed, congratulations.
    - `Could not connect to native MeCab component` - Something went wrong. Please refer to the **Notes** section and the **FAQ**.

## ❓ How to find your extension ID.

If you are a Firefox user and/or have built Yomitan from source, you need to obtain the extension ID for Yomitan. If you reinstall Yomitan, MeCab may no longer work for you in this case.
- Chrome/Chromium/Edge:
    - Open up your Yomitan settings page. The URL should look something like this:
    - ![image](https://github.com/user-attachments/assets/4f87be39-6cb4-45df-a9a7-09fb9a177c1d)
    - (Note: On Edge, the prefix will be `extension://`. **Make sure to change this to `chrome-extension://`, otherwise it will not work.**)
    - Copy everything before `settings.html`. For example: `chrome-extension://mbclianmdhnmblbfecpefmgjhajbioip/`.
    - ❗***Make sure to remember the `chrome-extension://` AND the `/` at the end of the ID!!***
    - Then, rerun the script as seen above and when it displays `Add more extension IDs`, paste the extension ID URL that you got. It should work. Continue with the tutorial.
- Firefox:
    - Open up your Yomitan settings page. The URL should look like this:
    - ![image](https://github.com/user-attachments/assets/618f262e-ce3c-47eb-a1e4-d60dd684adaa)
    - Now, copy everything in between `moz-extension://` and `/settings.html`. For example: `9ed7d4a5-f8cd-4285-9977-e6389a91fd72`.
    - Next, put the line of numbers and letters in between brackets: `{9ed7d4a5-f8cd-4285-9977-e6389a91fd72}`. That is your Extension ID. Copy it.
    - Rerun the script as seen above and when it displays `Add more extension IDs`, paste the extension ID **with the brackets** in the input. It should work. Continue with the tutorial.

## FAQ

*Why is firefox different?*: 
    - That's because, from what I've seen, Firefox gives a unique extension ID for every user, instead of one global one like in the Chrome store. This makes it much trickier to install MeCab.

## Notes
- If you try to run the installer for use on multiple browsers, it will not work. Only one browser can use the MeCab for Yomitan installation.
- If you wish to use MeCab on another browser, close the browser that has MeCab for Yomitan installed. If you do not do this, you will get a Permission denied error when running the script.
- Try to reopen and close your browser if it isn't showing `Connection was successful.`.

- If you have any particular issues with installing MeCab, make an issue request. I'll try to help you as fast as possible. If you don't want to bother making a Github account, just shoot me a DM on Discord -- `koiyakiya`

