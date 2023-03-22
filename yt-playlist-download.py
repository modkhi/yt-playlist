import os, shutil, subprocess
from pytube import Playlist, YouTube

def run(pl):
    # insert the downloads destination (optional)
    # e.g. C:\Users\Username\Folder
    filepath = input("Downloads destination (optional): ")
    
    # get linked list of links in the playlist
    links = pl.video_urls
    
    # download each item in the list
    for l in links:
        os.system("cls")
        
        # converts the link to a YouTube object
        yt = YouTube(l)
        
        # takes first stream; since ffmpeg will convert to mp3 anyway
        # changes: added filter with file extension of mp4
        music = yt.streams.filter(file_extension="mp4").first()
        
        # gets the filename of the first video stream
        default_filename = music.default_filename
        print(default_filename)
        print("Downloading " + default_filename + "...")
        
        # downloads first video stream and rename the first video stream
        music.download()
        default_filename_remove_spaces = default_filename.replace(" ", "")
        try:
            # if its already renamed then pass
            os.rename(default_filename, default_filename_remove_spaces)
        except:
            pass
            
        # replaces mp4 with mp3 for ffmeg output
        new_filename = default_filename.replace("mp4", "mp3")
        new_filename_remove_spaces = new_filename.replace(" ", "")
        print("Converting to mp3....")
        
        # converts mp4 video to mp3 audio and moving the audio to folder input
        # NOTE: MUST HAVE "ffmpeg.exe" DOWNLOADED AND PLACED INSIDE THE DIRECTORY
        subprocess.call(f"ffmpeg -i {default_filename_remove_spaces} {new_filename_remove_spaces}", shell=True)
        # if exception then create download folder if not exists and store the downloaded audios
        try:
            # if filepath is empty then create download if not exists and store the downloaded audios
            if filepath == "":
                shutil.move(new_filename_remove_spaces, os.path.join(os.path.abspath("./Downloads"), new_filename_remove_spaces))
            else:
                shutil.move(new_filename_remove_spaces, os.path.join(os.path.abspath(filepath), new_filename_remove_spaces))
        except:
            if os.path.exists("./Downloads"):
                shutil.move(new_filename_remove_spaces, os.path.join(os.path.abspath("./Downloads"), new_filename_remove_spaces))
            else:
                os.makedirs("./Downloads")
                shutil.move(new_filename_remove_spaces, os.path.join(os.path.abspath("./Downloads"), new_filename_remove_spaces))
        os.remove(default_filename_remove_spaces)
        
        # Old Code
        """
        subprocess.run(['ffmpeg', '-i', 
            os.path.join(filepath, default_filename),
            os.path.join(filepath, new_filename)
        ])
        """
        
    print("Download finished.")

if __name__ == "__main__":
    url = input("Please enter the url of the playlist you wish to download: ")
    pl = Playlist(url)
    run(pl)
