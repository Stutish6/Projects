import csv
import os
import fontstyle
from rich.console import Console
from rich.table import Table
import sys
try:
    from term_image.image import AutoImage
    TERM_IMAGE_AVAILABLE = True
except:
    TERM_IMAGE_AVAILABLE = False

#File setup

FILE_NAME = 'anime_list.csv'
HEADERS = ['title','total_episodes','watched_episodes','status','image_path']

def intialized_file():
    "Create the CSV file with headers if it doesn't exist."
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w',newline='') as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
        print(f"Created new files: {FILE_NAME}")

    else:
        #Migrate existing CSV if image_path column is missing
        with open(FILE_NAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_headers = reader.fieldnames or []
            rows = list(reader)

        if 'image_path' not in existing_headers:
            print("Migrating CSV to add 'image_path' column...")
            for row in rows:
                row.setdefault('image_path', '') #This is used to merge the old csv with new csv,i.e. add the image_path as new column as new update,if it's already not added
            with open(FILE_NAME, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=HEADERS)
                writer.writeheader()
                writer.writerows(rows)
            print("Migration complete!")


#Read and write Helpers

def load_anime_list():
    "Read all anime from CSV and return as a list of dicts"

    anime_list = []
    with open(FILE_NAME, mode ='r',newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            #Convert numeric strings back to interger
            row['total_episodes'] = int(row['total_episodes'])
            row['watched_episodes'] = int(row['watched_episodes'])
            row.setdefault('image_path','')
            anime_list.append(row)
        return anime_list
    
def save_anime_list(anime_list):
    "Write the full anime list back to CSV."
    with open(FILE_NAME, mode='w', newline="") as file:
        writer = csv.DictWriter(file,fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(anime_list)

def get_status(watched, total):
    "Return a status string based on prograss"
    if watched == 0:
        return "Not Started"
    elif watched == total:
        return "Completed"
    elif 0< watched < total:
        return "Watching"
    else:
        print("The input number of episodes is higher then expected please check the value again!!!")
        return "ERROR"

# Core features

def open_image(image_path):
    "Open the image in the system default viewer"
    if not image_path:
        print("No image set for this anime")
        return
    if not os.path.exists(image_path):
        print(f"[Image not found: {image_path}]")
        return
    
    try:
        if sys.platform.startswith('win'): #It's used to indicate window OS and to open that file in the OS
            os.startfile(image_path)
        elif sys.platform == 'darwin': #It's used for mac system
            os.system(f"open {image_path}")
        else:
            os.system(f"xdg-open {image_path}") #It's for the linux system
        print(f"Opening image: {image_path}")
    except Exception as e:
        print(f"Could not open image: {e}")

def add_anime():
    "Add a new anime to the tracker"
    print("-"*40)
    print(fontstyle.apply("\t"'Add new Anime','bold/green'))
    print("-"*40)
    title = input("Anime title: ").strip()

    if not title:
        print("Title cannot be empty")
        return
    
    #Check for a Duplicate
    anime_list = load_anime_list()
    for anime in anime_list:
        if anime['title'].lower() == title.lower():
            print(f"{title} is already in the list")
            return
        
    #Get total episodes
    while True:
        try:
            total = int(input("Total episodes: "))
            if total <= 0:
                print("Must be greater than 0")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    #Get wathced episodes
    while True:
        try:
            watched = int(input("Episodes waatched so far (0 if not started): "))
            if watched < 0 or watched > total:
                print(f"Must be between 0 and {total}.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    image_path = ask_image_path()
    
    status = get_status(watched,total)
    new_anime = {
        "title": title,
        "total_episodes": total,
        "watched_episodes": watched,
        "status": status,
        "image_path": image_path
    }

    anime_list.append(new_anime)
    save_anime_list(anime_list)
    print(f"'{title}' added! Status: {status}")
    if image_path:
        print(f"Cover image saved: {image_path}")

def render_cover(image_path, width=18):
    "Render a cover image inline in the terminal using term-image"
    if not TERM_IMAGE_AVAILABLE:
        return False
    if not image_path or not os.path.exists(image_path):
        return False
    try:
        img= AutoImage(image_path)
        img.width = width
        img.draw()
        return True
    except Exception:
        return False
    
'''def view_all_anime():
    "Display all anime in a formatted table."
    anime_list = load_anime_list()

    if not anime_list:
        print("\n Your anime list is empty. Start by adding one!")
        return
    
    #old version to display the code
    #print("\n Your anime List")
    #print(f"{'S.No':<6} {'Title':<30} {'Progress':<15} {'Remaining':<12} {'Status'}")
    #print('-' *80)
    

    #console = Console()
    #Create table
    table = Table(title="Anime List",show_header =True,)

    #Add columns
    table.add_column("S.NO", justify='center' , width = 6)
    table.add_column("Title",justify='left', style='green', width = 35)
    table.add_column("Progress", justify='center',width=15)
    table.add_column("Remaining", justify='center',width = 12)
    table.add_column("Status", min_width=12, no_wrap=True)
    table.add_column("Image", justify='center', width=8)

    for i ,anime in enumerate(anime_list, start=1):
        title = anime["title"]
        total = anime["total_episodes"]
        watched = anime["watched_episodes"]
        remaining = total - watched
        status = anime['status']
        progress = f'{watched}/{total}'
        image_path = anime.get('image_path', '') #It is used as safety , when the following key is not present

        '''
        #old version
       # print(f"{i:<5} {title: <30} {progress:<15} {remaining:<12} {status}")

    #print("-"*80)
    #print(f"Total: {len(anime_list)} anime\n")'''
        
        #Color code status
        #status_color = {
           # "Watching": "[red]Watching[/red]",
           # "Completed": "[green]Completed[/green]"
        #}.get(status, status)

        #image_indicator = "[cyan]📷[/cyan]" if image_path and os.path.exists(image_path) else "[dim]-[/dim]"

        #table.add_row(str(i), title, progress, str(remaining), status_color, image_indicator)
    
    #Display
    #console.print(table)
    #console.print(f"\n[bold]Total Anime:[/bold] {len(anime_list)}")
    #console.print("[dim] 📷 = has cover image | Use 'open image' option to view[/dim]\n")'''
def view_all_anime():
    anime_list = load_anime_list()
    if not anime_list:
        print("\n Your anime list is empty. Start by adding one!")
        return
    
    console = Console()

    if not TERM_IMAGE_AVAILABLE:
        console.print("\n[yellow] pip install term-image[/yellow]\n")

    console.print("\n[bold cyan]******Anime List******[/bold cyan]")

    for i,anime in enumerate(anime_list, start=1):
        title = anime['title']
        total = anime['total_episodes']
        watched = anime['watched_episodes']
        remaining = total - watched
        status = anime['status']
        image_path = anime.get('image_path','')

        status_style = {
            "Completed": "bold green",
            "Watching": "bold yellow"
        }.get(status,"white")

        pct = watched / total if total else 0
        filled = int(pct * 20)
        bar = f"[cyan]{filled}[/cyan][dim]{''* (20 - filled)}[/dim]"

        console.print(f"[bold white]{i}.[/bold white] [bold green]{title}[/bold green]")

        has_image = image_path and os.path.exists(image_path)
        if has_image and TERM_IMAGE_AVAILABLE:
            render_cover(image_path, width=22)
        else:
            console.print("")

        console.print(
            f"Progress: {bar} [white]{watched}/{total}[/white]"
            f"Remaing:[white]{remaining}[/white]"
            f"Status: [{status_style}]{status}[/{status_style}]"
            )
        
        console.print("[dim]---------------------[/dim]")

    console.print(f"\n[bold]Total Anime:[/bold] {len(anime_list)}\n")

def ask_image_path():
    "Prompt uere to an local image path for you anime title cover"
    print("\n Anime title cover url ")
    image_path = input("Image path: ").strip().strip('"').strip("'")
    if image_path and not os.path.exists(image_path):
        print("Warning: File not found, please check the path!!!")
    return image_path

def open_anime_image():
    "Let user pick an anime and open it's cover image."
    anime_list = load_anime_list()
    if not anime_list:
        print("No anime in list.")
        return
    view_all_anime()

    while True:
        try:
            choice = int(input("Enter the S.No of the anime to open its iamge: "))
            if 1 <= choice <= len(anime_list):
                break
            print(f"Enter a number between 1 and {len(anime_list)}")
        except ValueError:
            print("Please enter a valid number.")

    anime = anime_list[choice -1]
    print(f"\nOpening image for: {anime['title']}")
    open_image(anime.get('image_path', ''))

def update_progress():
    "Update the watched episode count for an anime and Anime as well."
    anime_list = load_anime_list()

    if not anime_list:
        print("\n No anime to update")
        return
    
    view_all_anime()

    choice_update_name_count = fontstyle.apply("What do you want to update anime name or count: ","blod/blue")
    options = input(choice_update_name_count).lower().strip() #Just to display the input text in blue colour
    
    if options == "count":
        type_of_count = fontstyle.apply("What do you want to update total count or watch count(tc/wc): ","red/blue")
        count_option = input(type_of_count).lower().strip()
        if count_option == 'wc':
            while True:
                try:
                    choice = int(input("Enter the serial number of anime which you want to update: "))
                    if 1 <= choice <= len(anime_list):
                        break
                except ValueError:
                    print("Please enter a valid number.")

            anime = anime_list[choice-1]
            title = anime["title"]
            total = anime["total_episodes"]
            current = anime["watched_episodes"]

            print(f"\n Updating: {title}")
            print(f"Currently watched: {current}/{total}")

            while True:
                try:
                    new_watched = int(input(f"New episode count (1-{total}): "))
                    if 0 <= new_watched <=total:
                        if new_watched < current:
                            user_episode_count = input("Are you sure you want to reduce the episodes count form your original count!!! (yes/no): ").lower().strip()
                            if user_episode_count == 'yes':
                                print("User choice APPROVED!!!")
                                break
                            elif user_episode_count == 'no':
                                new_watched = int(input("Then please do re-enter you BAKA🤡: "))
                            
                        break
                    print(f"Must be between 0 and {total}.")

                except ValueError:
                    print("Please enter a valid number.")

            anime["watched_episodes"] = new_watched
            anime["status"] = get_status(new_watched,total)
            save_anime_list(anime_list)

            remaining = total - new_watched
            print(f"Updated! {remaining} episodes reaminning. Status: {anime['status']}")
        
        elif count_option == 'tc':
            while True:
                try:
                    choice = int(input("Enter the serial number of anime which you want to update: "))
                    if 1 <= choice <= len(anime_list):
                        break
                except ValueError:
                    print("Please enter a valid number.")

            anime = anime_list[choice-1]
            title = anime["title"]
            total = anime["total_episodes"]
            current = anime["watched_episodes"]

            print(f"\n Updating: {title}")
            print(f"Currently watched: {current}/{total}")

            while True:
                try:
                    new_watched_wc = int(input(f"New episode count (1-{total}): "))
                    if 0 <= new_watched_wc <=total:
                        if new_watched_wc < current:
                            user_episode_count = input("Are you sure you want to reduce the episodes count form your original count!!! (yes/no): ").lower().strip()
                            if user_episode_count == 'yes':
                                print("User choice APPROVED!!!")
                                break
                            elif user_episode_count == 'no':
                                new_watched_wc = int(input("Then please do re-enter you BAKA🤡: "))
                            
                        break
                    print(f"Must be between 0 and {total}.")

                except ValueError:
                    print("Please enter a valid number.")

            anime["total_episodes"] = new_watched_wc
            anime["status"] = get_status(current,new_watched_wc)
            save_anime_list(anime_list)

            print(f"Updated!!! episodes reaminning. Status: {anime['status']}")

        else:
            print("Invalid entery by the weeb so you wouldn't be able to update your changes!!!")

    elif options == 'name':
        while True:
            try:
                choice = int(input("Enter the serial number of anime which you want to update: "))
                if 1 <= choice <= len(anime_list):
                    break
            except ValueError:
                print("Please enter a valid number.")

        anime = anime_list[choice-1]
        title = anime["title"]
        total = anime["total_episodes"]
        current = anime["watched_episodes"]

        print(f"\n Current name of the anime is: {title}")
        print(f"Currently watched: {current}/{total}")

        update_title = fontstyle.apply("What do you want to update anime name as: ","blod/blue")
        current_title = input(update_title).strip()

        anime['title'] = current_title
        save_anime_list(anime_list)
        anime_title_current = fontstyle.apply(current_title,'bold/green')
        print(f"The updated anime title is: {anime_title_current}")

    else:
        print("Invalid entery by the weeb so you wouldn't be able to update your changes!!!") 
        
        

def delete_anime():
    "Remove an anime from the list"
    anime_list = load_anime_list()

    if not anime_list:
        print("No anime data found")

    view_all_anime()

    while True:
        try:
            choice = int(input("Enter the number of the anime to delete: "))
            if 1 <= choice <= len(anime_list):
                break
            print(f"Enter a number between 1 and {len[anime_list]}")
        except ValueError:
            print("Please enter a valid number")

    title = anime_list[choice-1]["title"]
    confirm = input(f"Are you sure you want to delete '{title}'? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        anime_list.pop(choice-1)
        save_anime_list(anime_list)
        print(f"{title} deleted")
    elif confirm == 'no':
        print("Deletion cancelled")
    else:
        print(f"Please enter valid input!!! '{confirm}' is not allowed")


def show_stats():
    "Show the summary of your watching anime"
    anime_list = load_anime_list()

    if not anime_list:
        print("Data not found")
        return
    
    total_anime = len(anime_list)
    completed = sum(1 for a in anime_list if a['status'] == 'Completed')
    watching = sum(1 for a in anime_list if a['status']== 'Watching')
    not_started = sum(1 for a in anime_list if a['status']== 'Not started')
    total_watched = sum(a["watched_episodes"] for a in anime_list)
    total_episodes = sum(a['total_episodes'] for a in anime_list)

    print("\n Your states")
    print(f"Total anime in list: {total_anime}")
    print(f"Completed: {completed}")
    print(f"Currently watching: {watching}")
    print(f"Not started: {not_started}")
    print(f"Total watched: {total_watched}")
    print(f"Total episodes watched: {total_episodes}")
    if total_episodes > 0:
        percent = (total_watched/total_episodes) * 100
        print(f"Overall program: {percent:.1f}")
    print()

#Main menu 

def show_menu():
    print("\n"+'='*40)
    print("Anime episode tracker")
    print("="*40)
    print("1. View all anime")
    print("2. Add new anime")
    print("3. Update anime details: ")
    print("4. Delete anime")
    print("5. View my stats")
    print("6. Open anime cover image")
    print("7. Exit")
    print("="*40)



def main():
    intialized_file()
    print("Welcome to your Anime Tacker!!!")

    while True:
        show_menu()
        choice = input('Choose an option (1-6): ').strip()

        if choice == '1':
            view_all_anime()
        elif choice == '2':
            add_anime()
        elif choice == '3':
            update_progress()
        elif choice == '4':
            delete_anime()
        elif choice == '5':
            show_stats()
        elif choice == '6':
            open_anime_image()      
        elif choice == '7':
            print("\n See you next episode!\n")
            break
        else:
            print('Invlaid choice. Pick 1-6.')

if __name__ == '__main__':
    main()