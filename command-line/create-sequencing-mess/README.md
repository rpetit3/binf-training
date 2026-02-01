# Create Sequencing Mess

Okie doke, here's an exercise to help you practice organizing sequencing files. When it comes
to bioinformatics, half the time your job is just organizing datasets! So, the goal here is
to force you to practice basic unix commands by creating a mess you get to clean up.

> [!TIP]
> If you take one thing away from this exercise, let it be: _"There's many right ways to do things,
> especially on the command-line."_ Share your ideas with others, so you can learn new ways of
> doing things!

## Installation

For this exercise, I'm assuming you already have Conda installed, if not please see the miniforge
[installation instructions](https://github.com/conda-forge/miniforge?tab=readme-ov-file#requirements-and-installers).


With conda available, create a new environment:

```
conda create -n binf-training \
    -c conda-forge \
    python \
    rich-click \
    tree \
    wget
```

Then activate the environment:

```
conda activate binf-training
```

Finally, let's download the `create-sequencing-mess` script and make it executable:

```
wget -O create-sequencing-mess https://raw.githubusercontent.com/rpetit3/binf-training/refs/heads/main/command-line/create-sequencing-mess/create-sequencing-mess.py
chmod 755 create-sequencing-mess
./create-sequencing-mess --version
```

## Exercise Overview

The script `create-sequencing-mess` will generate a set of dummy sequencing files that you 
will be organizing into specific folder structures based on the exercises below.

Here is the basic format of the files that will be generated:

```
{SAMPLE_ID}-{ORGANISM}-{ORG}-{YEAR}_{TECHNOLOGY}[_R1|_R2].fastq.gz
```

Where:
- `SAMPLE_ID` is a unique identifier for the sample (e.g., `SA001`, `SA002`, etc.)
- `ORGANISM` is the organism being sequenced (e.g., `FLU`, `COVID`, `RSV`, etc.)
- `ORG` is the organization that submitted the sample (e.g., `WPHL`, `CDC`, etc.)
- `YEAR` is the year the sample was collected (e.g., `2023`, `2024`, etc.)
- `TECHNOLOGY` is the sequencing technology used (`ILLUMINA`, `ONT`, `PACBIO`)
- `_R1` and `_R2` are used for paired-end Illumina reads

> [!NOTE]
> **Reproducibility:** The script uses `--seed 42` by default, so we'll all get the same files!
>
> **Starting fresh:** Messed up? No worries! Use `--force` to regenerate the data:
> ```
> ./create-sequencing-mess --chaos low --samples 15 -o round1-reads --force
> ```

## Commands You Might Use

There are many ways to accomplish these tasks. Here are some commands you may (_or may not!_) find useful:

- `ls` - list files
- `mv` - move files
- `cp` - copy files
- `mkdir` - make directories
- `rm` - remove files
- `pwd` - print working directory
- `cd` - change directory
- `wc` - word/line count
- `grep` - search for patterns
- `cat` - display file contents
- `touch` - create empty files
- `sort` - sort lines of text
- `uniq` - remove duplicate lines
- `find` - find files and directories
- `xargs` - build and execute command lines from standard input
- `tree` - display directory structure (handy for checking your work!)

**Wildcards:**
- `*` - matches any characters (e.g., `ls *.fastq.gz`)
- `?` - matches a single character

---

## Round 1 - Single-Level Organization

```
./create-sequencing-mess --chaos low --samples 15 -o round1-reads
```

Round 1! We're going to kick this off with some simple organization. We'll be organizing into
single-level folders (e.g. organize by year). Let's kick off this warm-up round.

### Task 1A: Group by Technology

Create folders for each sequencing technology and move files accordingly.

```
round1-reads/
├── illumina/
├── nanopore/
└── pacbio/
```

> [!TIP]
> Consider checking your work with the `tree` command:
> ```
> tree round1-reads
> ```

### Task 1B: Group by Organization

Start fresh and organize by organization instead.

```
round1-reads/
├── aphl/
├── cdc/
├── uw/
├── wphl/
├── wslv/
└── wy/
```

### Task 1C: Group by Organism

Start fresh and organize by organism.

```
round1-reads/
├── covid/
├── flu/
├── meas/
├── mpox/
└── rsv/
```

### Task 1D: Group by Year

Start fresh and organize by year.

```
round1-reads/
├── 2019/
├── 2020/
├── 2021/
├── 2022/
├── 2023/
├── 2024/
└── 2025/
```

---

## Round 2 - Two-Level Organization

```
./create-sequencing-mess --chaos low --samples 20 -o round2-reads
```

Ok, now that you're warmed up let's kick it up a notch! Now we're going to add another level
to our organizing! For example, grouping by year then by technology. 

### Task 2A: Group by Technology, then Year

```
round2-reads/
├── illumina/
│   ├── 2023/
│   ├── 2024/
│   └── 2025/
├── nanopore/
│   ├── 2023/
│   ├── 2024/
│   └── 2025/
└── pacbio/
    ├── 2023/
    ├── 2024/
    └── 2025/
```

### Task 2B: Group by Organization, then Year

```
round2-reads/
├── aphl/
│   ├── 2023/
│   └── 2024/
├── cdc/
│   ├── 2022/
│   ├── 2023/
│   └── 2024/
└── ...
```

### Task 2C: Group by Organism, then Year

```
round2-reads/
├── covid/
│   ├── 2023/
│   └── 2024/
├── flu/
│   ├── 2022/
│   └── 2023/
└── ...
```

---

## Round 3 - Three-Level Organization (Medium Chaos)

```
./create-sequencing-mess --chaos medium --samples 25 -o round3-reads
```

You should be getting the hang of this by now! So, let's make it a bit more challenging by
(_yes! you guessed it!_) adding another level of organization. Additionally, add some chaos!

We'll be adding `--chaos medium` which will introduce case variations in the file naming.

### Task 3A: Group by Year, then Organism, then Technology

```
round3-reads/
├── 2023/
│   ├── covid/
│   │   ├── illumina/
│   │   ├── nanopore/
│   │   └── pacbio/
│   ├── flu/
│   │   ├── illumina/
│   │   └── nanopore/
│   └── ...
├── 2024/
│   └── ...
└── 2025/
    └── ...
```

### Task 3B: Group by Year, then Organization, then Organism

```
round3-reads/
├── 2023/
│   ├── aphl/
│   │   ├── covid/
│   │   ├── flu/
│   │   └── rsv/
│   ├── cdc/
│   │   ├── covid/
│   │   └── mpox/
│   └── ...
├── 2024/
│   └── ...
└── 2025/
    └── ...
```

---

## Round 4 - Four-Level Organization (Medium Chaos)

```
./create-sequencing-mess --chaos medium --samples 30 -o round4-reads
```

OK, just like before, let's make these directories even more nested! This time, we're going
four levels deep!

### Task 4: Group by Organization, then Year, then Organism, then Technology

```
round4-reads/
├── aphl/
│   ├── 2023/
│   │   ├── covid/
│   │   │   ├── illumina/
│   │   │   └── nanopore/
│   │   └── flu/
│   │       └── pacbio/
│   └── 2024/
│       └── ...
├── cdc/
│   ├── 2023/
│   │   └── ...
│   └── 2024/
│       └── ...
└── ...
```

---

## Round 5 - For the lolz

```
./create-sequencing-mess --chaos high --samples 40 -o round5-reads
```

This time, it's the same as round 4, but with `--chaos high` which will introduce shuffling 
of the metadata order and mixed separators. Have fun!

```
round5-reads/
├── aphl/
│   ├── 2023/
│   │   ├── covid/
│   │   │   ├── illumina/
│   │   │   └── nanopore/
│   │   └── flu/
│   │       └── pacbio/
│   └── 2024/
│       └── ...
├── cdc/
│   ├── 2023/
│   │   └── ...
│   └── 2024/
│       └── ...
└── ...
```

_While it's possible, this one would be annoying to do by hand!_

---

## Bonus Challenges

### Challenge 1: Paired-End Verification

For Illumina data, every R1 file should have a matching R2 file. Write commands to verify
all pairs are present.

### Challenge 2: Counting Summary

Create a summary that counts files by technology, organization, or organism.

### Challenge 3: Undo and Redo

Practice removing directories and starting fresh with different organization schemes.

---

## Conclusion

Congrats on completing the sequencing file organization exercise! (_Or, just coming here
to read the conclusion!_) In this exercise, you should have practiced using a variety of
basic unix commands to manipulate files and directories. 

P.S. _Example solutions are provided in the hints section below, but remember there's many
ways to accomplish these tasks!_

---

<details>
<summary>Hints and Example Commands (click to expand)</summary>

### General Tips

```bash
# Count all files
ls round1-reads/*.fastq.gz | wc -l

# Count files matching a pattern
ls round1-reads/*ILLUMINA* | wc -l

# Create a directory
mkdir round1-reads/illumina

# Move files one at a time
mv round1-reads/SA001-FLU-CDC-2024_ILLUMINA_R1.fastq.gz round1-reads/illumina/

# Move files with wildcards
mv round1-reads/*ILLUMINA* round1-reads/illumina/

# Create nested directories
mkdir -p round2-reads/illumina/2024

# Start fresh
rm -r round1-reads/
./create-sequencing-mess --chaos low --samples 15 -o round1-reads
```

### Handling Case Sensitivity (Round 3+)

```bash
# Match CDC regardless of case
ls *[Cc][Dd][Cc]*

# Or use multiple moves
mv *CDC* cdc/
mv *cdc* cdc/
mv *Cdc* cdc/
```

### Bonus Challenge Solutions

**Paired-End Verification:**
```bash
for f in round1-reads/illumina/*R1*; do
    r2="${f/R1/R2}"
    if [ ! -f "$r2" ]; then
        echo "Missing pair: $r2"
    fi
done
```

**Counting Summary:**
```bash
echo "Illumina: $(ls round1-reads/*ILLUMINA* 2>/dev/null | wc -l)"
echo "ONT: $(ls round1-reads/*ONT* 2>/dev/null | wc -l)"
echo "PacBio: $(ls round1-reads/*PACBIO* 2>/dev/null | wc -l)"
```

</details>
