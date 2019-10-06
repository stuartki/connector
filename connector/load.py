def file_finder():
    from searcher import searcher
    import os

    SUPPORTED_FILE_TYPES = ['.pdf', '.txt']
    w = ""
    path = os.getcwd()
    def reload_dir(path):
        with os.scandir(path) as dire:
            cur_directory = [n for n in dire]
        return cur_directory
    cur_directory = reload_dir(path)
    def aprint(array, tab = '\t'):
        for n in array:
            if isinstance(n, os.DirEntry):
                print(tab + n.name)
            else:
                print(tab + n)

    while w != "end":
        w = input("load: ")
        if w == "end":
            continue
        
        if w == "ls":
            aprint(cur_directory)
            continue

        if w == "":
            cur_directory = reload_dir(path)
            aprint(cur_directory)
            continue

        if w in SUPPORTED_FILE_TYPES:
            file_type = w
            cur_directory = [n for n in cur_directory if file_type in n.name]
            aprint(cur_directory)
            continue

        if "cd .." == w or ".." == w:
            arr = path.split('/')
            if len(arr) > 1:
                path = "/".join(arr[:-1])
                print(path)
                cur_directory = reload_dir(path)
                aprint(cur_directory)
            else:
                aprint(cur_directory)
            continue
        if "cd" in w:

            if w[3:] in [n.name for n in cur_directory]:
                path += "/"+w[3:]
                cur_directory = reload_dir(path)
                aprint(cur_directory)
            else:
                print("/"+w[3:] + " NOT IN DIRECTORY")
            continue

        if w == "path":
            print(path)
            continue
            
        
        else:
            s = searcher(w, [n.name for n in cur_directory])
            if len(s) == 0:
                print("NO SIMILAR FILES")
                aprint(cur_directory)
                continue
            cur_directory = [n for n in cur_directory if n.name in s]
            if len(s) > 1:
                cur_directory = [n for n in cur_directory if n.name in s]
                aprint(cur_directory)
            elif cur_directory[0].is_file():
                aprint(cur_directory)
                i = input("load? ")
                if i == "y" or i == "yes":
                    path = cur_directory[0].path
                    break
                    #term_text_editor(path, from_topic = "")
            else:
                path = cur_directory[0].path
                cur_directory = reload_dir(path)
                aprint(cur_directory)
    return path

def pdf_loader(path):
    import textract
    text = textract.process(path)
    pdf = text.decode('utf-8').replace('\n', ' ').split('. ')
    return pdf

def txt_loader(path):
    with open(path, 'r') as cur_file:
        data = str(cur_file.read()).replace('\n', ' ')
    import nltk

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    data = [n[:-1] for n in tokenizer.tokenize(data)]
    return data

def term_text_editor(data, init_index = 0, from_topic = ""):
    from writer import writer
    
    from searcher import searcher
    from mapper import interface
    
    i = ""
    
    walker = init_index
    return_string = ""
    if walker == 0:
        print("LOADING")
        print("PRESS ENTER TO CONTINUE")
        input()


    while i != "end" or (walker > 0 and walker < len(data)):
        cur_sentence = str(data[walker])
        i = input(cur_sentence + '.' + '\n')
        if i == "end":
            continue
        if "add" in i:
            if i[:-1] == "-":
                return_string = cur_sentence + return_string + ". "
            else:
                return_string += cur_sentence + ". "
            print("ADDED")
            print()
            walker += 1

        if i == "" or "+" in i:
            try:
                num = int(i.replace("+", ""))
            except:
                num = 1
            
            walker += num
            continue
        if i == "-" or i == "back":
            try:
                num = int(i.replace("+", ""))
            except:
                num = 1
            walker -= num
            print()
            continue
        if i == "ls":
            print(return_string)
            print()
        
        if i == "search":
            search = input("search: ")
            list_search = searcher(search, data, index = True)
            if len(list_search) > 0:
                print(str(len(list_search)) + " ITEMS FOUND")
                for n in list_search:
                    s = input(data[n] + ": \n")
                    if s == "jump":
                        walker = n
                        break
                    if s == "end":
                        break

        if i == "write":
            if from_topic == "":
                topic = input("topic: ")
                writer(topic, init_description = return_string)
            else:
                writer(from_topic, init_description = return_string)
            continue
        if i == "interface" or i == "map":
            break

    return walker
    # for n in range(len(data)):
    #     i = input(data[n] + '.')
    #     if i == "sep":
    #         epsilon = 0
    #         return_string = data[n]
    #         t = ""
    #         while t != "write":
    #             t = input(return_string + ": ")
    #             if t == "edit":
    #                 continue
    #             if t == "add":
    #                 pass
    #             if t == "write":
    #                 if from_topic == "":
    #                     topic = input("topic: ")
    #                     writer(topic, init_description = return_string)
    #                 else:
    #                     writer(from_topic, init_description = return_string)
    #                 continue
            









if __name__ == "__main__":
    topic = "test"
    path = file_finder()
    if ".txt" in path:
        data = txt_loader(path)
    if ".pdf" in path:
        data = pdf_loader(path)
    term_text_editor(data, from_topic = topic)