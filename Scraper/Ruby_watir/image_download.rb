require 'open-uri'
require 'csv'
require 'fileutils'


def create_directory(dirName)
  FileUtils::mkdir_p dirName
end

def download_image(playerName,imageName,imageUrl)
  begin
    open(imageName, 'wb') do |file|
       file << open(imageUrl).read
    end
  rescue
    puts 'No image availabe for ' + playerName
  end
end

def generate_csv(csvName)
  return CSV.read(csvName,'r', :headers => true)
end

def get_image_path(dirName,playerName)
  imageName = playerName.gsub(' ','_') + '.png'
  imagePath = dirName + '/' +imageName
  return imagePath
end

currentTime = DateTime.now
dirName = 'nbaPlayerimage_' + currentTime.strftime("%d_%m_%Y_%H:%M:%S")
create_directory(dirName)
players = generate_csv('nbaPlayerList.csv')
players.each do |row|
  playerName = row['playerName']
  imageLink = row['imageLink']
  imagePath = get_image_path(dirName,playerName)
  download_image(playerName,imagePath,imageLink)
end

