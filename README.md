
# vurl (visited url)

## Introduction

vurl is a Python script that provides some simple filtering capabilities for URLs. The script allows the user to filter a list of URLs to show which ones have been visited, which ones have not been visited, or to remove duplicates.

The project was created in order to help organize URL visits when performing a Bug Bounty examination on the URLs. It is common (for me, at least) to get lost on which URLs I have visited and the ones I haven't.

## Installation

1) Git clone the file

```
git clone https://github.com/buschinelli-joao/vurl
```

2) To install vurl, you need to first make the script executable by running the following command:

```
chmod +x vurl.py
```

3) Rename the file:

```
mv vurl.py vurl
```
4) Finally, copy the script to a directory on your $PATH variable. For example:

```
sudo mv vurl /etc/local/bin
```

## Usage

The script can be used by running the following command:

```
vurl [OPTION] [FLAGS]
```

### Initializating the tracking of URLs in your directory

Inside the directory where you are storing the URLs enumerated that you intend to visit, run

```
vurl start --target [name-of-your-target]
```

This will create a directory inside the current one, called 'target', as well as a file inside it called, in this case, name-of-your-target. This file is the one that you have all the urls you have visited.

If you don't provide --target flag, it will just create the ./target dir.

### Adding a single URL to to-visit or visited files

If you want to add a single URL to the to-visit file (in order to keep track of the urls you want to visit in the future), you run:

```
vurl add --target [name-of-your-target] -u [url-string]
```

This will create a file called name-of-your-target-urls_to_visit, where it will save the url-string you passed in the -u flag.

### Adding a list of URLs

If you want, you can pass a file containing a list of URLs line by line that you want to add to the to-visit file. In this case, you run the same code above, but passing the filename using the -u flag instead of the url-string.

### Removing duplicates & Updating files

If you happen to have duplicate URLs inside the passed url-string or the file, you can run

```
vurl update --target [name-of-your-target]
```

This will update your name-of-your-target and url_to_visit files, also deleting urls in url_to_visit file that are also inside of the name-of-your-target file. 

### Smart add

If you don't want to manually check and add files to either one of the visited or not visited files, you can use the --smart-add flag. 

```
vurl add --target [name-of-your-target] -u [url] --smart-add
```

This will add all the urls in your url file that are not in the name-of-your-target file, adding it to urls_to_visit file.

### Marking all as visited

When you finish your assesment, you can mark all urls inside urls_to_visit as visited, i.e., sending them to name-of-your-target file.

```
vurl mark-all-visited --target [name-of-your-target]
```

## Support

If you encounter any issues or have any questions about using vurl, please open an issue on GitHub.


