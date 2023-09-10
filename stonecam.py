import pandas as pd
import re

COMMAND_LIST = {
'list' : 'вывести список образцов в текущем активном месте хранения',
'edit' : 'работать с текущим активным местом хранения',
'skip' : 'пропустить измерения текущего образца',
'cancel' : 'отменить изменения образцов в текущем месте хранения',
'save' : 'сохранить внесенные изменения',
'help' : 'вывести список доступных команд',
'y'     : '\tДа',
'n'     : '\tНет',
'exit' : 'завершить работу с программой'
}

def PrintHelp():
    print('\nДоступные команды:')
    for key in COMMAND_LIST.keys():
        print(f"   {key} \t{COMMAND_LIST[key]}")    
        
def IsValid(command):
    p = re.compile('\d_[\d]{1,7}')


    if command in COMMAND_LIST.keys():
        return True
    elif p.match(command):
        return True
    else:    
        return False

def GetUserInput(prompt):
    while True:
        try:
            command = input(prompt)
        except Exception as err:
            print("Input failed")
            print("Text: ", err)
            print("Name: ", type(err).__name__)    
        else:
            if IsValid(command):
                return command
            else:
                print("Некорректная команда. Введите 'help', чтобы вывести список доступных команд")

def GetStorageInventory(filename="in.csv", target_storage="0_0"):
# returns a list / dataframe of samples in the given storage from the file
    with open(filename, 'r') as f_in:
        lines_list = f_in.readlines()
    
    # storage_inventory = []
    # for line in lines_list:
        # current_storage = line.split(',\t')[0].strip()
        # if current_storage == target_storage:
            # storage_inventory.append(line.strip().split(',\t'))
        # else:
            # pass
            #print(line.split()[0])
            
            
    #df = pd.read_csv(filename, index_col='ID')
    df = pd.read_csv(filename)
    storage_inventory = df[ df['MCHR'] == target_storage]
    
    
    return storage_inventory
    
def GetSize():
    #input('Press Enter to measure sample size')
    sample_size_X=20
    sample_size_Y=15
    sample_size_Z=10
    print(f"{sample_size_X}x{sample_size_Y}x{sample_size_Z} см")
    return sample_size_X, sample_size_Y, sample_size_Z
    
def GetWeight():
    #input('Press Enter to measure sample weight')
    sample_weight = 700
    print(sample_weight, "г")
    return sample_weight
    
def TakePhoto():
# takes pictures using webcam
    return 0
    
def EnhancePhoto(pic):
    return 0
    
def SavePhoto(sample_code = "0_000000"):
# saves photo to a folder with the same name as the sample_code
    pic = TakePhoto()
    enhanced_pic = EnhancePhoto(pic)
    pass
    
def EditStorage(sample_list):
    updated_samples = []
    if sample_list.empty:
        print('Место хранения пусто')
    else:
        for ind, row in sample_list.T.items():
            print("\nОбразец:\t", row['ID'])
            user_input = GetUserInput("Нажмите Enter для измерения образца, введите 'skip' или 'cancel' для пропуска или отмены\t")
            if user_input == 'skip':
                continue
            elif user_input == 'cancel':
                break
            sample_weight = GetWeight()
            sample_size_X, sample_size_Y, sample_size_Z = GetSize()
            SavePhoto(row['ID'])
            df = pd.DataFrame({'ID':row['ID'], 'MCHR':row['MCHR'], 'Weight':sample_weight, 
                            'Size_X':sample_size_X, 'Size_Y':sample_size_Y, 'Size_Z':sample_size_Z}, index=[ind])
            updated_samples.append(df)
            
    user_input = GetUserInput("Добавить образцы в данное место хранения (y/n)?\t")
    if user_input.lower == 'y':
        pass
    else:
        pass
    if updated_samples:
        updated_df = pd.concat(updated_samples)
        print(updated_df.T)
    else:
        print('Изменений не внесено')

def AddSampleToRecord(df,
                    sample_code="0_000000", 
                    sample_storage="0_0",
                    sample_weight=0, 
                    sample_size_X=0, 
                    sample_size_Y=0, 
                    sample_size_Z=0):
    pass
    
def WriteRecordToCSV(output_file, df):
    pass
    
user_input = ''
active_storage_name = ''
sample_list = []
    
while True:
    print("Активное место хранения:", active_storage_name)
    user_input = GetUserInput("\nВведите место хранения или команду: ")
    
    if user_input == 'exit':
        exit()
    elif user_input == 'list':
        # for sample in sample_list:
            # print(sample)
        if sample_list.empty:
            print(active_storage_name, 'пусто или не существует')
        else:
            print(sample_list)
    elif user_input == 'edit':
        EditStorage(sample_list)
        
    elif user_input == 'save':
        pass
    elif user_input == 'help':
        PrintHelp()
    else:
        try:
            sample_list = GetStorageInventory(target_storage=user_input)
        except Exception as err:
            print("Could not get the sample list for the storage given")
            print("Text: ", err)
            print("Name: ", type(err).__name__)
        else:
            active_storage_name = user_input
            print(f"Найдено записей: {len(sample_list)}")
        
