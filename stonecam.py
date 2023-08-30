import pandas as pd

COMMAND_LIST = """
Доступные команды:
- list - вывести список образцов в текущем активном месте хранения
- save - сохранить внесенные изменения
- help - вывести список доступных команд
- exit - завершить работу с программой"""

def GetUserInput():
    try:
        storage = input("Введите место хранения или команду: ")
    except Exception as err:
        print("Input failed")
        print("Text: ", err)
        print("Name: ", type(err).__name__)    
    else:
        return storage  

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
            
            
    df = pd.read_csv(filename, index_col='ID')
    storage_inventory = df[ df['MCHR'] == target_storage]
    
    
    return storage_inventory
    
def GetSize():
    sample_size_X=0 
    sample_size_Y=0
    sample_size_Z=0
    return sample_size_X, sample_size_Y, sample_size_Z
    
def GetWeight():
    sample_weight = 0
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
    user_input = GetUserInput()
    
    if user_input == 'exit':
        exit()
    elif user_input == 'list':
        # for sample in sample_list:
            # print(sample)
        if sample_list.empty:
            print(active_storage_name, 'is empty or does not exist')
        else:
            print(sample_list)
    elif user_input == 'help':
        print(COMMAND_LIST)
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
        
