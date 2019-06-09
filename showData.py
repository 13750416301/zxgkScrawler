import json    

if __name__ == "__main__":
    #fileName = input("请输入您要查询信息的文件的名称：")
    #with open('json\\' + fileName, "r", encoding='utf-8') as jsonFile:
    '''
    with open('jsonPage17.json', "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    print(data)
    '''
    with open('jsonPage17.json', 'r', encoding='utf-8') as file:
        str = file.read()
    file.close()
    '''
    str = str.replace("\'", "\"")
    str = str.replace("None", "\"None\"")
    print(str)
    '''
    with open('jsonPage17.json', 'w', encoding='utf-8') as file:
        file.write(str)
    file.close()
    with open('jsonPage17.json', "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    #print(data[0])

    for key in data[0]:
        print(key + ': ' + data[0][key])
