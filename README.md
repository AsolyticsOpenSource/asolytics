<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Telegram][telegram-shield]][telegram-url]
[![Downloads month][month-download-shield]][month-download-url]
[![Downloads week][week-download-shield]][week-download-url]
[![Downloads day][day-download-shield]][day-download-url]


<br />
<div align="center">
  <a href="https://github.com/AsolyticsOpenSource/asolytics">
    <img src="https://github.com/AsolyticsOpenSource/asolytics/raw/main/logo.svg" alt="Logo" width="80" height="80">
  </a>

   <h3 align="center">Asolytics is an open source tool for ASO</h3>

  <p align="center">
    Instructions for installing and using the software
    <br />
    <a href="https://pypi.org/project/asolytics/"><strong>Page PyPi »</strong></a>
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
pip3 install asolytics
```
or
```sh
pip install asolytics
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. To view a list of available Asolytics software features, use the `--help` key 
```sh
asolytics --help
```

[![Asolytics ASO Tool Help][help-screenshot]](https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-help.png)

2. To specify a country code and language, use the `--gl` and `--hl` keys. To specify the country, use the two-character <a href="https://www.iso.org/obp/ui/#search">ISO country code</a>. To specify the language code, use the code from this <a href="https://support.google.com/googleplay/android-developer/table/4419860?hl=uk">table</a>. Example: `--gl AU --hl en` (country: Australia, language: English)

3. To start the Google Play suggest parsing function, use the `--key`. Specify a search keyword as the parameter, the software will analyze the suggests and generate a table with all the derived keywords. The table will calculate the relative popularity of each derived keyword. To specify the country and language, use the `--gl` and `--hl` keys.
```sh
asolytics --key workout --gl AU --hl en
```

[![Asolytics ASO suggest parsing][key-screenshot]](https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-key.png)

4. To identify the most popular keywords on Google Play, use the parameter `--trends`. To specify country and language, use `--gl` and `--hl` parameters. The table will display the trending search terms and their relative popularity
```sh
asolytics --trends --gl AU --hl en
```
[![Asolytics ASO Google Play trends][trends-screenshot]](https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-trends.png)

5. You can get a lot of additional information about your competitors on Google Play by using the --average option with the bundle ID of the app you want to analyze.
```sh
asolytics --average com.moymer.falou --gl AU
```

You will get the following data:
* The total number of ratings on Google Play;
* The number of installations in Google Play;
* Average number of installations of the app per day;
* Average number of ratings per day;
* Revenue of the app for the last month;
* Countries from which the app gets the most traffic;
* The country of the app's origin;

[![Asolytics ASO app analysis][average-screenshot]](https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-average.png)

6. The software allows you to track an app's position in a Google Play search using specified keywords. To run this function, use the `--tracker` key. The keywords are passed as a parameter, with a semicolon (example `'workout at home;fitness;fitness plans'`). In addition, keywords can be loaded from a file, to do this, use key `--file`, at that the path to the file with the keywords should be passed as a parameter `--tracker`. As the `--id` parameter, pass the bundleID of the app whose positions you want to track To specify the country and language, use the `--gl` and `--hl` keys.
```sh
asolytics --tracker 'workout at home;fitness;fitness plans' --id com.fiton.android --gl US --hl en 
```
[![Asolytics ASO tracker keywords][tracker-screenshot]](https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-tracker.png)

Use this command to load keywords from a file
```sh
asolytics --tracker '/path/keywords.txt' --file --id com.fiton.android --gl US --hl en 
```

In the `keywords.txt` file each keyword must be on a new line.<br />
Example of file content<br />
`workout at home`<br />
`fitness`<br />
`fitness plans`<br />

7. You can extract keywords which are used in the metadata of any app. To do this you need to use the `--extract` key and pass the bundleID of the app you want to analyze as a parameter. Asolytics will use artificial intelligence to recognize keywords in the app title, short description, full description and user reviews. In the table will be displayed the position of the app in the Google Play search for all the keywords found. To specify country and language use `--gl` and `--hl` keys
```sh
asolytics --extract com.fiton.android --gl US --hl en 
```

[![Asolytics ASO extract keywords][extract-screenshot]](https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-extract.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Make instructions for use
- [x] Suggest parser
- [x] Trend analysis on Google Play
- [x] App info
    - [ ] Tracking app positions in categories
- [x] Tracking positions in Google Play searches
- [x] Extracting keywords from app metadata using artificial intelligence
- [ ] Add multilingual localization of the software
- [x] Website
    - [ ] Make graphics for website
    - [ ] Translate website into English

See the [open issues](https://github.com/AsolyticsOpenSource/asolytics/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Website - [asolytics.app](https://asolytics.app)

Telegram Channels: [@asolytics](https://t.me/asolytics)

Telegram Chat: [@asolytics_chat](https://t.me/asolytics_chat)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

If you are new to ASO you should read the following materials. These links should be useful to you

* [App store optimization (ASO)](https://en.wikipedia.org/wiki/App_store_optimization)
* [Get discovered on Google Play search](https://support.google.com/googleplay/android-developer/answer/4448378?hl=en)
* [A Complete Guide to App Store Optimization](https://medium.com/udonis/a-complete-guide-to-app-store-optimization-e39d9abeca7b)
* [ASO Google Play: Google Play Keyword Optimization](https://medium.com/android-news/aso-google-play-google-play-keyword-optimization-ed5540bfe3b1)

If you have a few dollars, please support the Ukrainian people's fight for freedom and democracy. Today the Ukrainian people are defending all of Europe and Western values from evil and darkness!

Use for this purpose:
* [UNITED24](https://u24.gov.ua)
* [Come Back Alive](https://savelife.in.ua/en)

Or use another volunteer organization!<br />Glory to Ukraine 🇺🇦

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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

[day-download-shield]: https://img.shields.io/pypi/dd/asolytics?style=for-the-badge
[day-download-url]: https://pypi.org/project/asolytics

[month-download-shield]: https://img.shields.io/pypi/dm/asolytics?style=for-the-badge
[month-download-url]: https://pypi.org/project/asolytics

[week-download-shield]: https://img.shields.io/pypi/dw/asolytics?style=for-the-badge
[week-download-url]: https://pypi.org/project/asolytics

[product-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/macbook.png

[help-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-help.png

[key-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-key.png

[trends-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-trends.png

[average-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-average.png

[tracker-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-tracker.png

[extract-screenshot]: https://github.com/AsolyticsOpenSource/asolytics/raw/main/screen-extract.png