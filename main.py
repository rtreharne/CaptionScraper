from canvasapi import Canvas
import getpass
import tqdm
import os
import shutil


import warnings

warnings.filterwarnings('ignore', 'SettingWithCopyWarning')
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    print(
"""
                      ░▓▓░   ░░                             
                       ░░    ▓▓                             
                   ░░       ░██░       ░░                   
                 ░░█▒░  ░██████████░  ░▒█░░                 
            ░▒░  ░░█▒░░     ░██░      ░▒█░░ ░░▒░            
             ▒     ░░        ▓▓        ░░    ░▒             
                    ░░░      ░░      ░░░                    
                 ▓███████▓░      ░▓███████▓                 
        ░▒▒░   ▒██▒░░░  ▒██▒░  ░▒██▒░░▒ ░▒██▒   ░▒▒░        
        ░███▓ ░██░░█▒    ░██░░░░██░░▓▓░▒█░░██░ ▓███░        
        ░▓░▓█▒▒█▒░▓░      ▒██████▒░█░░█░░  ▒█▒▒█▓░▓░        
         ░ ▒█▓░██░        ▓█▒░░▒█▓░░▓▓░   ░██░▓█▓ ░         
          ░▓██░▓█▓░     ░▒██░  ░▓█▓░     ░▓█▓░██▓░          
          ░████░░███▓▓▓███▒░    ░▒███▓▓▓███░░████░          
          ▒▒▒██░  ░▒▓▓▓▒░░        ░░▒▓▓▓▒░  ░██▒▒▒          
           ░███░       ░░░░      ░░░░       ░███░           
           ▒███░     ▒██████▒  ▒██████▒     ░███▒           
          ░██▒░    ▒████████████████████▒    ░▒██░          
         ░▓█████▓███████████▒░░▒███████████▓▓████▓░         
         ░███████████████▓░      ░▒███████████████░         
         ▓██▓███░░░░░░░     ░▓▓░     ░░░░░░░███▓██▓░        
        ░▓█░▓█████▓▓▓▓▓ ░  ▒████▒  ░ ▓▓▓▓▓█████▓░█▓░        
         ▒▓░███████████░▓░░██████░░█░███████████░▓▒         
          ░ █████████████▓▒██████▒▓█████████████ ░          
            ░██▒████████████████████████████▒██░            
             ▓█░████████████████████████████░█▓░            
             ░▓░▒██████████████████████████▒░▓░             
                 ▓██▒▓████████████████▓▒██▓                 
                 ░██▒░███▓▓███████▓███▒▒██░                 
                   ▒█░▒██▓▒██████▓▒██▒░█▒                   
                    ░░░░██░▓█████░▓█░ ░░                    
                         ▒▒░▓███░▒▒░                        
                             ▒▓                                             
""" )
    print("")
    print("www.canvaswizards.org.uk")
    print("")
    print("Welcome to the Canvas Assignment Submissions Download (SubDown) Tool!")
    print("By Robert Treharne, University of Liverpool. 2024")
    print("")

    # if config.py exists, import it
    try:
        from config import CANVAS_URL, CANVAS_TOKEN
    except ImportError:
        CANVAS_URL = input('Enter your Canvas URL: ')
        print("")
        CANVAS_TOKEN = getpass.getpass('Enter your Canvas token: ')
        print("")

    # if course_id in config.py, use it
    try:
        from config import course_id
    except ImportError:
        course_id = int(input('Enter the course ID: '))
        print("")

    # if assignment_id in config.py, use it
    try:
        from config import assignment_id
    except ImportError:
        assignment_id = int(input('Enter the assignment ID: '))
        print("")

    canvas = Canvas(CANVAS_URL, CANVAS_TOKEN)

    print("Getting submissions...")

    parent_dir = f"course_{course_id}_assignment_{assignment_id}_submissions"

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)


    submissions = get_submissions(canvas, course_id, assignment_id)

    os.chdir(parent_dir)

    for submission in tqdm.tqdm(submissions):
        student_dir = f"{submission.user['sortable_name'].replace(", ", "_")}"

        if not os.path.exists(student_dir):
            os.makedirs(student_dir)
        
        download_submission(submission, student_dir)

    # change back to parent directory
    os.chdir("..")

    # create a zipped directory
    shutil.make_archive(parent_dir, 'zip', parent_dir)
    
def download_submission(submission, dir):

    # get cwd
    cwd = os.getcwd()

    # create directory if it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    # change to directory
    os.chdir(dir)
    try:
        file = submission.attachments[-1]
        
        # download file to directory dir
        file.download(f"{file}")
    except:
        pass

    # change back to cwd
    os.chdir(cwd)


def get_submissions(canvas, course_id, assignment_id):
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    submissions = [x for x in assignment.get_submissions(include=['user'])]
    return submissions[:10]


if __name__ == "__main__":
    main()