# telegramer
A terminal-based tool for using audio meta data to modify audio file properties


## From Github

```
git clone https://github.com/collinsuzebu/telegramer.git
cd telegramer	
```

## Usage

**Rename all audio files in current directory**

`$ python3 telegramer --rename`


**Rename all audio files in a specific directory**

`$ python3 telegramer --rename -d /path/to/directory/audiofiles`


**Group audio based on artist name**

`$ python3 telegramer --groupby artist -d /path/to/directory/audiofiles`


**Use `help` to get more options.**

`$ python3 telegramer --help`



## Development

### Test

Add `conftest.py` in the root directory. `conftest.py` is not tracked on git.

You can run test using `pytest` with the simple command:

`$ pytest telegramer`