<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Telegram][telegram-shield]][telegram-url]



<br />
<div align="center">
  <a href="https://github.com/AsolyticsOpenSource/asolytics">
    <img src="logo.svg" alt="Logo" width="80" height="80">
  </a>

   <h3 align="center">Asolytics is an open source tool for ASO</h3>

  <p align="center">
    Instructions for installing and using the software
    <br />
    <a href="https://pypi.org/project/test-test-test/"><strong>Page PyPi »</strong></a>
    <br />
    <br />
    <a href="https://github.com/AsolyticsOpenSource/asolytics/pulls">Pull requests</a>
    ·
    <a href="https://github.com/AsolyticsOpenSource/asolytics/issues">Report Bug</a>
    ·
    <a href="https://github.com/AsolyticsOpenSource/asolytics/issues">Request Feature</a>
  </p>

</div>

<!-- TABLE OF CONTENTS -->
<summary>Table of Contents</summary>
<ol>
<li>
    <a href="#about-the-project">About The Project</a>
    <ul>
    <li><a href="#built-with">Built With</a></li>
    </ul>
</li>
<li>
    <a href="#getting-started">Getting Started</a>
    <ul>
    <li><a href="#prerequisites">Prerequisites</a></li>
    <li><a href="#installation-asolytics">Installation Asolytics</a></li>
    </ul>
</li>
<li><a href="#usage">Usage</a></li>
<li><a href="#roadmap">Roadmap</a></li>
<li><a href="#contributing">Contributing</a></li>
<li><a href="#license">License</a></li>
<li><a href="#contact">Contact</a></li>
<li><a href="#acknowledgments">Acknowledgments</a></li>
</ol>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Asolytics ASO Tool Screen Shot][product-screenshot]](https://en.wikipedia.org/wiki/Command-line_interface)

In the world there are many ASO services which solve different tasks related to search engine optimization in mobile app stores. All of them have advantages and disadvantages, one of the main drawbacks is closed algorithms for data analysis, ASO specialist has no access to raw data, in most services is unknown how the popularity of keywords is formed, there is no way to check the correctness of the algorithm, and therefore difficult to trust the data and make serious conclusions.

We want to create an open source service for ASO experts, so that each user could have full access to all data and algorithms, could offer their own functions or add their own code. This promotes the ASO community and improves the professionalism of specialists. 

Here's why:

* Your time should be focused on creating something amazing. A project that solves a problem and helps others;
* You should always have a wealth of information to make decisions;
* You should always be able to check the source of the data and the algorithm for calculating it;

Of course, no one software will fit all tasks related to ASO, because your needs may be different. So I will add more functions in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

All major frameworks/libraries and software that the Asolytics.app project uses during installation and operation. This list may be updated periodically

* <img src="https://img.shields.io/badge/firefox-000000?style=for-the-badge&logo=firefox&logoColor=white" alt="firefox"> Just a lightning fast browser
* <img src="https://img.shields.io/badge/python-20232A?style=for-the-badge&logo=python&logoColor=61DAFB" alt="Python"> Python is a programming language that lets you work quickly and integrate systems more effectively
* <img src="https://img.shields.io/badge/selenium-35495E?style=for-the-badge&logo=selenium&logoColor=4FC08D" alt="Selenium"> Automates browsers
* <img src="https://img.shields.io/badge/yake-DD0031?style=for-the-badge&logoColor=white" alt="Yake"> Unsupervised Approach for Automatic Keyword Extraction using Text Features.
* <img src="https://img.shields.io/badge/PrettyTable-4A4A55?style=for-the-badge&logoColor=FF3E00" alt="PrettyTable"> A simple Python library for easily displaying tabular data in a visually appealing ASCII table format
* <img src="https://img.shields.io/badge/argparse-FF2D20?style=for-the-badge&logoColor=white" alt="Argparse"> Parser for command-line options, arguments and sub-commands

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

To install and run your local copy of the software, follow these simple steps.

### Prerequisites

To use Asolytics, you need to install the scarce components and software

* Install or update the Firefox browser on your computer (<a href="https://www.mozilla.org/en-US/firefox/">Download Firefox</a>)
* Install Python3 on your computer. On some systems it is installed by default (<a href="https://www.python.org/downloads/">Download Python</a>)

### Installation Asolytics

To install Asolytics, open a terminal and run the following command. 

Installation is from the PyPi repository
```sh
pip3 install aso
```
or
```sh
pip install aso
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. To view a list of available Asolytics software features, use the `--help` key 
```sh
asolytics --help
```

[![Asolytics ASO Tool Help][help-screenshot]]()

2. To specify a country code and language, use the `--gl` and `--hl` keys. To specify the country, use the two-character <a href="https://www.iso.org/obp/ui/#search">ISO country code</a>. To specify the language code, use the code from this <a href="https://support.google.com/googleplay/android-developer/table/4419860?hl=uk">table</a>. Example: `--gl AU --hl en` (country: Australia, language: English)

3. To start the Google Play suggest parsing function, use the `--key`. Specify a search keyword as the parameter, the software will analyze the suggests and generate a table with all the derived keywords. The table will calculate the relative popularity of each derived keyword. To specify the country and language, use the `--gl` and `--hl` keys
```sh
asolytics --key workout --gl AU --hl en
```

<!-- LINKS & IMAGES asolytics -->
[contributors-shield]: https://img.shields.io/github/contributors/AsolyticsOpenSource/asolytics.svg?style=for-the-badge
[contributors-url]: https://github.com/AsolyticsOpenSource/asolytics/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/AsolyticsOpenSource/asolytics.svg?style=for-the-badge
[forks-url]: https://github.com/AsolyticsOpenSource/asolytics/network/members

[stars-shield]: https://img.shields.io/github/stars/AsolyticsOpenSource/asolytics.svg?style=for-the-badge
[stars-url]: https://github.com/AsolyticsOpenSource/asolytics/stargazers

[issues-shield]: https://img.shields.io/github/issues/AsolyticsOpenSource/asolytics.svg?style=for-the-badge
[issues-url]: https://github.com/AsolyticsOpenSource/asolytics/issues

[license-shield]: https://img.shields.io/github/license/AsolyticsOpenSource/asolytics.svg?style=for-the-badge
[license-url]: https://github.com/AsolyticsOpenSource/asolytics/blob/master/LICENSE.txt

[telegram-shield]: https://img.shields.io/badge/-Telegram-black.svg?style=for-the-badge&logo=telegram&colorB=555
[telegram-url]: https://t.me/asolytics

[product-screenshot]: macbook.png

[help-screenshot]: screen-help.png
