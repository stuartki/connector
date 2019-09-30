def file_finder(from_file = ""):
    from searcher import searcher
    import os
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

        if "." in w:
            file_type = w
            cur_directory = [n for n in cur_directory if file_type in n.name]
            aprint(cur_directory)
            continue

        if "back" == w:
            arr = path.split('/')
            if len(arr) > 1:
                path = "/".join(arr[:-1])
                print(path)
                cur_directory = reload_dir(path)
                aprint(cur_directory)
            else:
                aprint(cur_directory)
            continue

        if w == "path":
            print(path)
            continue
            
        
        else:
            s = searcher(w, [n.name for n in cur_directory])
            cur_directory = [n for n in cur_directory if n.name in s]
            if len(s) > 1:
                cur_directory = [n for n in cur_directory if n.name in s]
                aprint(cur_directory)
            elif cur_directory[0].is_file():
                aprint(cur_directory)
                i = input("load? ")
                if i == "y" or i == "yes":
                    return term_text_editor(cur_directory[0].path, from_file)
            else:
                path = cur_directory[0].path
                cur_directory = reload_dir(path)
                aprint(cur_directory)
def term_text_editor(path, from_file):
    from writer import writer
    import textract
    text = textract.process(path)
    pdf = text.decode('utf-8').replace('\n', ' ').split('.')
    i = ""
    walker = 0
    while i != "end" or walker < 0 or walker >= len(pdf):
        
        i = input(pdf[n] + '.' + '\n')
        if i == "end":
            continue
        if i == "sep":
            return_string = pdf[n]
    for n in range(len(pdf)):
        i = input(pdf[n] + '.')
        if i == "sep":
            epsilon = 0
            return_string = pdf[n]
            t = ""
            while t != "write":
                t = input(return_string + ": ")
                if t == "edit":
                    continue
                if t == "add":
                    pass
                if t == "write":
                    if from_file == "":
                        topic = input("topic: ")
                        writer(topic, init_description = return_string)
                    else:
                        writer(from_file, init_description = return_string)
                    continue
            









if __name__ == "__main__":
    topic = "test"
    term_text_editor('../pdfs/bailNetsNLP.pdf', from_file = topic)