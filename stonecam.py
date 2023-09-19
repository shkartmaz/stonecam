import pandas as pd
import re
import os
from datetime import date

EXIT_CODE_OK, EXIT_CODE_SKIP, EXIT_CODE_CANCEL = 11, 22, 33

COMMAND_LIST = {
'list' : 'вывести список образцов в текущем активном месте хранения',
'edit' : 'работать с текущим активным местом хранения',
'skip' : 'пропустить измерения текущего образца',
'cancel' : 'отменить изменения образцов в текущем месте хранения',
'save' : 'сохранить внесенные изменения',
'help' : 'вывести список доступных команд',
'y'     : '\tДа',
'n'     : '\tНет',
''      : '\tНажимайте Enter для подтверждения',
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
    
def IsEmpty(list):
    if len(list) == 0:
        return True
    for element in list:
        if element is not None:
            return False
    return True

def EditSample(sample_ID, sample_MCHR, sample_index):
    print("\nОбразец:\t", sample_ID)
    user_input = GetUserInput("Нажмите Enter для измерения образца, введите 'skip' или 'cancel' для пропуска или отмены\t")
    if user_input == 'skip':
        return None, EXIT_CODE_SKIP
    elif user_input == 'cancel':
        return None, EXIT_CODE_CANCEL
    sample_weight = GetWeight()
    sample_size_X, sample_size_Y, sample_size_Z = GetSize()
    SavePhoto(sample_ID)
    
    df = pd.DataFrame({'ID':sample_ID, 'MCHR':sample_MCHR, 'Weight':sample_weight, 
                            'Size_X':sample_size_X, 'Size_Y':sample_size_Y, 'Size_Z':sample_size_Z}, index=[sample_index])
    return df, EXIT_CODE_OK
    
def EditStorage(sample_list, active_storage):
    updated_samples = []
    if sample_list.empty:
        print('Место хранения пусто')
    else:
        for ind, row in sample_list.T.items():
            df, exit_code = EditSample(row['ID'], row['MCHR'], ind)
            updated_samples.append(df)
            if exit_code == EXIT_CODE_CANCEL:
                break
    
    while True:
        user_input = GetUserInput("Добавить образцы в данное место хранения (y/n)?\t")
        if 'y' in user_input:
            sample_ID = GetUserInput('Введите номер образца:\t')
            sample_index = int(sample_ID.replace('_',''))
            df, exit_code = EditSample(sample_ID, active_storage, sample_index)
            updated_samples.append(df)
            if exit_code == EXIT_CODE_CANCEL:
                break
        else:
            break
    if IsEmpty(updated_samples):
        print('Изменений не внесено')
    else:
        updated_df = pd.concat(updated_samples)
        print(updated_df.T)
        WriteRecordToCSV(updated_df)

def AddSampleToRecord(df,
                    sample_code="0_000000", 
                    sample_storage="0_0",
                    sample_weight=0, 
                    sample_size_X=0, 
                    sample_size_Y=0, 
                    sample_size_Z=0):
    pass
    
def WriteRecordToCSV(df):
    filename = 'measurements/' + str(date.today()) + '.csv'
    if os.path.exists(filename):
        df.to_csv(filename, header=False, index=False, mode='a')
    else:
        os.makedirs('measurements', exist_ok=True)
        df.to_csv(filename, header=True, index=False, mode='w')
    
user_input = ''
active_storage = ''
sample_list = []
    
while True:
    print("Активное место хранения:", active_storage)
    user_input = GetUserInput("\nВведите место хранения или команду: ")
    
    if user_input == 'exit':
        exit()
    elif user_input == 'list':
        # for sample in sample_list:
            # print(sample)
        if sample_list.empty:
            print(active_storage, 'пусто или не существует')
        else:
            print(sample_list)
    elif user_input == 'edit':
        EditStorage(sample_list, active_storage)
        
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
            active_storage = user_input
            print(f"Найдено записей: {len(sample_list)}")
        
