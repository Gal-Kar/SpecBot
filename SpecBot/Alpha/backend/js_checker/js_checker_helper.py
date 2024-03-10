non_alphanumeric_chars = [ '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']


def check_pattern(p1,p2,pos):
    #p1 is tested template p2 is the block and pos is the start position in the block
    for i in p1:
        if i != "<>":
            # print(p2[pos])
            if not p2[pos]:
                return False
            if i != p2[pos]:
                return False
        elif p2[pos] in non_alphanumeric_chars:
            return false;

        pos+=1
    # print(p1)
    return True

def change_var(block,pos):
    separator = ' '
    result_block = block.split(separator)
    result_block.insert(pos,"[*]")
    return separator.join(result_block) + "\n~~~~ var should be replaced with const or let ~~~"

def change_error(block,pos):
    # check if after catch(error) the error is being used
    result_block = block.split(' ')
    for i in range(pos,len(result_block)):
        if '}' in result_block[i]:
            result_block.insert(pos, "[*]")
            return separator.join(result_block) + "\n~~~~ you never used the error you can remove it (catch {...}) ~~~"


def change_nullish_coalescing_operator(block,pos):
    #check if is from type var __ = __ || ___ and if is change to var __ = __ ?? __
    separator = ' '
    result_block = block.split(separator)
    if '==' in [result_block[pos-1],result_block[pos-2]] or '=' not in [result_block[pos-1],result_block[pos-2]]:
        return
    template1 = ["<>","=","<>","||","<>"]
    template2 = ["<>=","<>","||","<>"]
    template3 = ["<>=<>","||","<>"]
    template4 = ["<>","=<>","||","<>"]
    if check_pattern(template1,result_block,pos-3) or check_pattern(template2,result_block,pos-2) or check_pattern(template3,result_block,pos-1) or check_pattern(template4,result_block,pos-2):
        result_block.insert(pos,"[*]")
        return separator.join(result_block) + "\n~~~~ _ = _ || _ ; should be replaced with _ = _ ?? _ ; ~~~"

def change_optional_chaining_operator(block,pos):
    # check if is from type var __ = __ ? __ : null; and if is change to var __ = __ ?? __
    separator = ' '
    result_block = block.split(separator)
    if result_block[pos+1] == ":null" or result_block[pos+2] == "null":
        result_block.insert(pos,"[*]")
        return separator.join(result_block) + "\n~~~~ _ = _ ? _  : null; should be replaced with _ = _ ?. _ ; ~~~"
    return

