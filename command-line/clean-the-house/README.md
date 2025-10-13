# Clean the House

This is an exercise to practice using some basic command-line tools to manipulate files and
directories.


## Installation

You will need to have Conda avaialable on your system to create an environment.

```
conda create -n binf-training \
    -c conda-forge \
    python \
    rich-click \
    wget
```

Then activate the environment:

```
conda activate binf-training
```

Download the script and make it executable:

```
wget -O clean-the-house https://raw.githubusercontent.com/rpetit3/binf-training/refs/heads/main/command-line/clean-the-house/clean-the-house.py
chmod 755 clean-the-house
./clean-the-house --version
```

## Directions

The goal of this exercise is to use command-line tools to clean up a messy directory structure. When executing
the script it will create a few "rooms" (directories) and a lot of "items" (files) that need to be organized
into the correct rooms. You will need to use command-line tools to move the files into the correct directories.

Here is the mapping of rooms to items:

| Room        | Items                     |
|-------------|---------------------------|
| living_room | sofa, lamp, table         |
| kitchen     | plates, pans, food, trash |
| bedroom     | clothes, toys, books      |
| bathroom    | toothbrush, shampoo       |
| garage      | tools, car-parts          |

## Example Commands To Use

The cool thing about this exercise is that there are many ways to accomplish the same task. So, 
as long as you can answer the questions below, you are free to use any command-line tools. Here
are some commands that you might find useful:

- `ls` - list files
- `mv` - move files
- `mkdir` - make directories
- `find` - find files
- `grep` - search for text in files
- `wc` - word count
- `sort` - sort lines of text
- `uniq` - remove duplicate lines
- `head` - display the first lines of a file
- `tail` - display the last lines of a file
- `cat` - concatenate and display files
- `xargs` - build and execute command lines from standard input
- `tree` - display directory structure (may need to install)

## Round 1 - A clean house

```
./clean-the-house --outdir clean-house
```

This will create a directory called `clean-house` with a lot of files in it. Your goal is to
move the files into the correct directories.

### Questions to answer

1. How many items are in the house?
2. How many per-item are in the house?
3. How many items are in each room?

#### Round 2 - A messy house

```
./clean-the-house --outdir messier-house --messy
```

This will create a directory called `messier-house` with a lot of files in it. Your goal is to
move the files into the correct directories. **This time the items are a bit mixed up!**

### Questions to answer

1. How many items are in the house?
2. How many per-item are in the house?
3. How many items are in each room?

## Round 3 - A messier house

```
./clean-the-house --outdir messier-house --messier
```

This will create a directory called `messier-house` with a lot of files in it. Your goal is to
move the files into the correct directories. **This time the items are even more mixed up!

### Questions to answer

1. How many items are in the house?
2. How many per-item are in the house?
3. How many items are in each room?

## Round 4 - The messiest house

```
./clean-the-house --outdir messiest-house --messiest
```

This will create a directory called `messiest-house` with a lot of files in it. Your goal is to
move the files into the correct directories. **This time the items are completely mixed up!**

### Questions to answer

1. How many items are in the house?
2. How many per-item are in the house?
3. How many items are in each room?


## Bonus Round - Spring Cleaning 

Some items are old and need to be thrown out. You will need to read the contents of the files
to determine if they are old or not. If the file contains the word "remove" then it should
be put into the `trash-bin`.

We'll use the `clean-house` for this round.

1. Create a `trash-bin` in the `clean-house`
2. Move all items that should be removed into the `trash-bin`
