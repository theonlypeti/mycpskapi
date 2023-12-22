
# MyCpSkAPI

MyCpSkAPI (name pending haha) is a Python-based application that interacts with the cp.sk API to fetch and display train route information. It provides detailed information about train routes including departure and arrival times, delays, train types, and distances.

## Features

- Fetches train route information from cp.sk.
- Provides detailed information about each route including departure and arrival times, delays, train types, and distances.
- Supports command-line arguments for easy usage.
- Includes autocorrect and search for station names.
- Debug and profiling modes for detailed logging and performance analysis.

## Requirements

- Python
- pip

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using pip:
   ```
   pip install -r requirements.txt
   ```

## Usage

You can run the program with command-line arguments. Here's an example:

```bash
python main.py --depart "Bratislava" --to "Podhajska" --date 13.01.2024 --time 12:00 --autocorrect
```

## Command-line Arguments

- `--depart`: The departure city (required).
- `--to`: The destination city (required).
- `--date`: The date of departure in the format dd.mm.yyyy.
- `--time`: The time of departure in the format hh:mm.
- `--force`: Forces the program to use the exact station names provided by the user, even if they contain potential typos or mismatches.
- `--autocorrect`: Enables the program to automatically correct the station names provided by the user by guessing the most likely correct names.
- `--debug`: Enable debug mode.
- `--profiling`: Measures the runtime and outputs it to profile.prof.
- `--logfile`: Logs to a file.

## Disclaimer

This project is a free time endeavor, created for the purpose of programming practice and learning. It is not intended for commercial use or profit. Please note that using this application may be against cp.sk's Terms of Service. Use this application responsibly and at your own risk. 

[cp.sk ToS](https://cp.hnonline.sk/zmluvne-podmienky/#:~:text=s%20mobiln%C3%BDmi%20oper%C3%A1tormi.-,2.%20Vyu%C5%BE%C3%ADvanie%20CP.sk,-2.1.%20Bez%20s%C3%BAhlasu)

## Acknowledgments

While this project is largely self-made, we would like to acknowledge the [python-cpsk-api](https://github.com/Adman/python-cpsk-api/tree/master/cpsk) project for providing some inspiration during the development process.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
