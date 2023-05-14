#!/usr/bin/python

import argparse
import os

'''
Usage:
example 1
visit-filter.py [URL/URLs string or file] -f [Filter through visited URLS (default True)] 

'''

class Filter:
    def __init__(self, url_input, path_to_dir, target):
        if isinstance(url_input, list):
            self.urls = []
            self.islist = True
            for elem in url_input:
                self.urls.append(elem)
        else:
            self.islist = False
            self.urls = url_input
        self.target = target
        self.path_to_dir = path_to_dir
        self.path_to_target_file = f"{path_to_dir}/{target}"
        self.urls_to_visit = []


    def save_to_visit_list(self):
        with open(f"./{self.path_to_dir}/{self.target}-urls_to_visit", 'a') as file:
            for item in self.urls_to_visit:
                file.write(f"{item}\n")
        file.close()


    def add_url_to_visit(self, url):
        with open(f"./{self.path_to_dir}/{self.target}-urls_to_visit", 'a') as file:
            file.write(f"{url}\n")
        file.close()

    def check_if_visited(self, url):
        visited_urls_list = open_visited(self.path_to_target_file)
        if url in visited_urls_list:
            response = input(f"[INFO] URL {url} was already visited. Do you want to add to to-visit list? [y/n] ")
            if response.lower() == 'y':
                self.urls_to_visit.append(url)
        else:
            response = input(f"[INFO] URL {url} was not yet visited. Do you want to save as visited? [y/n] ")
            if response.lower() == 'y':
                save_visited(url, self.path_to_target_file)
            else:
                print(f"[INFO] Adding {url} to urls_to_visit file.")
                self.add_url_to_visit(url)


    def update_files(self):
        with open(f"./{self.path_to_dir}/{self.target}-urls_to_visit", 'r') as f1, open(self.path_to_target_file) as f2:
            urls_visited = f2.readlines()
            urls_to_visit = f1.readlines()

        urls_to_visit = [url for url in urls_to_visit if url not in urls_visited]

        with open(f"./{self.path_to_dir}/{self.target}-urls_to_visit", 'w') as f:
            f.writelines(urls_to_visit)
        
        f1.close()
        f2.close()
        f.close()

        self.remove_duplicate()
        self.remove_duplicate(mode=1)


    def mark_as_visited(self):
        response = input("Do you want to mark all URLs in urls_to_visit file as visited? [y/n] ")
        if response.lower() == "yes":
            with open(f"{self.path_to_dir}/{self.target}-urls_to_visit", 'r') as not_visited_file, open(self.path_to_target_file, 'a') as visited_file:
                lines = not_visited_file.readlines()
                lines = [line.strip() for line in lines]
                for url in lines:
                    visited_file.write(url+'\n')
            not_visited_file.close()
            visited_file.close()
        
        self.update_files()
        print('[INFO] All URLs marked as visited.')



    def smart_add(self):
        urls = self.urls
        response = input("Do you want to save not visited URLs as to-visit [s] or mark them as visited [v]? ")
        if response.lower() == "s":
            with open(f"{self.path_to_dir}/{self.target}-urls_to_visit", 'a') as file, open(self.path_to_target_file, 'r') as visited_file:
                lines = visited_file.readlines()
                lines = [line.strip() for line in lines]
                for url in urls:
                    if url not in lines:
                        file.writelines(url+'\n')
            file.close()
        elif response.lower() == "v":
            with open(self.path_to_target_file, 'a') as file:
                for url in urls:
                    file.writelines(url+'\n')

        self.update_files()
        print('[INFO] Smart add finished.')


    def remove_duplicate(self, mode=0):
        if mode == 0:
            file_to_update = f"{self.path_to_dir}/{self.target}-urls_to_visit"
        elif mode == 1:
            file_to_update = f"{self.path_to_target_file}"
        else:
            return 
        with open(file_to_update, 'r') as file:
            lines = file.readlines()

        unique_lines = {}
        for line in lines:
            line = line.strip()
            if line not in unique_lines:
                unique_lines[line] = True

        file.close()

        with open(file_to_update, 'w') as file:
            file.writelines([line+'\n' for line in unique_lines])

        file.close()


    def filter_visited(self):
        if not self.islist:
            print('[ERR] URL input is not a list of urls.')
            exit(0)
        visited_urls_list = open_visited(self.path_to_target_file)
        filtered_ans = []
        for url_in in self.urls:
            if url_in in visited_urls_list:
                filtered_ans.append(url_in)
        
        return filtered_ans
    
    
    def filter_not_visited(self):
        if not self.islist:
            print('[ERR] URL input is not a list of urls.')
            exit(0) 
        visited_urls_list = open_visited(self.path_to_target_file)
        filtered_ans = []
        for url_in in self.urls:
            if url_in not in visited_urls_list:
                filtered_ans.append(url_in)

        return filtered_ans
    

    def print_to_view_urls(self):
        with open(f"./{self.path_to_dir}/{self.target}-urls_to_visit", 'r') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        for line in lines:
            print(line)
        file.close()


def print_list(l):
    for item in l:
        print(item)


'''
This functions is responsible to create a txt file that should
then contain all urls for the specific target_name
'''
def create_target_history_file(target_name, path_name):
    file_path = os.path.join(path_name, f'{target_name}')
    if os.path.isfile(file_path):
        overwrite = input(f"[PROMPT] A file for this target ({target_name}) already exists. Do you want to overwrite it? [y/n] ")
        if overwrite.lower() == 'n':
            return
        elif overwrite.lower() == 'y':
            with open(file_path, 'w') as file:
                file.write('')
                print(f'[INFO] {target_name}.txt created successfully')
        else:
            print('[ERR] Invalid option. Quitting...')
            exit(0)
    else:
        with open(file_path, 'w') as file:
            file.write('')
            print(f'[INFO] {target_name} created successfully')

'''
This function is responsible for creating the directory
where the target visisted urls are going to be stored
'''
def create_targets_path(path_name="targets"):
    if not os.path.exists(path_name):
        os.makedirs(path_name)


'''
Saves visisted url that is passed as parameter
'''
def save_visited(url, path_to_target_file):
    with open(path_to_target_file, 'a') as file:
        file.write(f"\n{url}")
    file.close()

'''
Opens target file and reads through it line by line
'''
def open_visited(path_to_target_file):
    with open(path_to_target_file, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    file.close()
    return lines


def parse_input(input_str):
    # If the input is a file path, read the contents of the file
    if os.path.isfile(input_str):
        with open(input_str, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
        return lines
    # Otherwise, return the input string
    return input_str


def main():
    parser = argparse.ArgumentParser(usage="visit-filter.py [POSITIONAL...] [OPTIONS...]")
    parser.add_argument('option', choices=['check', 'to-visit', 'start', 'filter-visited', 'filter-not-visited', 'update', 'mark-all-visited'], help='Select the mode to run the program.')
    parser.add_argument('--target', help='Specify target name')
    parser.add_argument('-u', '--url', type=parse_input, help='Specify URL to perform action.')
    parser.add_argument('--smart-add', help="Specify a smart add of url file. Asks user it want to add all not visited urls to urls_to_visit file.", action="store_true")
    args = parser.parse_args()
    option, target, url, smart_add = args.option, args.target, args.url, args.smart_add
    target_dir = "target"


    url_filter = Filter(url, f"./{target_dir}", target)

    if target is None or (url is None and (option != 'update' and option != 'mark-all-visited')):
        print("[ERR] URL and/or target not passed")
        parser.print_help()
        exit(0)

    if option == 'start':
        create_targets_path(f"./{target_dir}")
        if target is not None:
            create_target_history_file(target, f"./{target_dir}")
    elif option == 'check':
        if not url_filter.islist:
            url_filter.check_if_visited(url)
        else:
            if not smart_add:
                for u in url:
                    url_filter.check_if_visited(u)
                url_filter.save_to_visit_list()
            else:
                url_filter.smart_add()
    elif option == "to-visit":
        url_filter.print_to_view_urls()
    elif option == "filter-visited":
        visited = url_filter.filter_visited()
        print_list(visited)
    elif option == "filter-not-visited":
        not_visited = url_filter.filter_not_visited()
        print_list(not_visited)
    elif option == 'update':
        print('[INFO] Files updated.')
        url_filter.update_files()
    elif option == "mark-all-visited":
        url_filter.mark_as_visited()



if __name__ == '__main__':
    main()