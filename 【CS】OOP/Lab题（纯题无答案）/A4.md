# Assignment04 Personal Diary

**Requirements**

The Personal Diary is a CLI (Command Line Interface) software which consists of four programs:

```
pdadd 
pdlist [ ]
pdshow 
pdremove 
```

- **`pdadd`** is used to add an entity to the diary for the date. If an entity of the same date is in the diary, the existing one will be replaced. pdadd reads lines of the diary from the stdin, line by line, until a line with a single `'.'` character or the `EOF` character (`Ctrl-D` in Unix and `Ctrl-Z` in Windows).
- **`pdlist`** lists all entities in the diary ordered by date. If the `start` and the `end` date are provided through command line parameters, it lists entities between the start and the end only. This program lists to the stdout.
- **`pdshow`** prints the content of the entity specified by the date to the stdout.
- **`pdremove`** removes one entity of the date. It returns 0 on success and -1 on failure.

The software stores the diary in one data file, and reads it to the memory at the beginning of each program, and stores it back to the file at the end of the process.

**Evaluation standard**

1. c++ code quality (clean, compact and reasonable)
2. comments quality
3. common classes and functions should be shared between programs
4. these programs are physically independent so direct interaction is not permitted
5. these programs are able to work together by means of redirection
6. these programs are able to be used in a shell/batch script

**Files to submit**

Please prepare a .zip package including the following items：

1. the source code
2. a shell/batch script with several use cases for your software (cover all programs)

