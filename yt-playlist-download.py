import os
import subprocess

from pytube import Playlist, YouTube

def run(pl):
    # get parent directory; VERY IMPORTANT!!
    # INCLUDE LAST SLASH AFTER FOLDER NAME
    # e.g. /home/username/Folder/ or C:\Users\Username\Folder\
    filepath = input("Please enter the filepath of the directory where this script is located:\n")
    # get linked list of links in the playlist
    links = pl.parse_links()
    # download each item in the list
    for l in links:
        # converts the link to a YouTube object
        yt = YouTube(l)
        # filters out all non-audio streams
        music = yt.streams.filter(only_audio=True).all()
        # gets the filename of the first audio stream
        default_filename = music[0].default_filename
        print("Downloading " + default_filename + "...")
        # downloads first audio stream
        music[0].download()
        # creates mp3 filename for downloaded mp4 file
        new_filename = default_filename[0:-3] + "mp3"
        print("Converting to mp3....")
        # converts mp4 audio to mp3 audio
        subprocess.run(['ffmpeg', '-i', 
            os.path.join(filepath, default_filename),
            os.path.join(filepath, new_filename)
        ])
    
    print("Download finished.")

if __name__ == "__main__":
    url = input("Please enter the url of the playlist you wish to download: ")
    pl = Playlist(url)
    run(pl)
