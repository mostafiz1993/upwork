require 'rubygems'
require 'watir'
require 'csv'
require 'watir-scroll'


def find_nth_occurrence(var, substring, n)
  position = -1
  if n > 0 && var.include?(substring)
    i = 0
    while i < n do
      position = var.index(substring, position+substring.length) if position != nil
      i += 1
    end
  end
  return position != nil && position != -1 ? position + 1 : -1
end


def generate_hash(playerName,playerNumber,position,height,weight,team,imagePath)
  hashOfEachPlayer = Hash.new
  hashOfEachPlayer['name'] = playerName
  hashOfEachPlayer['number'] = playerNumber
  hashOfEachPlayer['position'] = position
  hashOfEachPlayer['height'] = height
  hashOfEachPlayer['weight'] = weight
  hashOfEachPlayer['team'] = team
  hashOfEachPlayer['image_link'] = imagePath
  return hashOfEachPlayer
end

def write_to_csv(playerName,playerNumber,position,height,weight,team,imagePath,csv)
  csv << [playerName,playerNumber,position,height,weight,team,imagePath]
end


browser = Watir::Browser.new
browser.window.resize_to(1920, 1280)
browser.goto 'http://www.nba.com/players'
browser.scroll.to :bottom
sleep(3)
i = 0
while i < 28000  do
  browser.scroll.to [0, i]
  i +=20
end
output = CSV.open("nbaPlayerListn  .csv", "a+",:write_headers=> true,
                  :headers => ["playerName","playerNumber","Position","Height","Weight","Team","imageLink"])


players = browser.elements(:xpath => "//section[starts-with(@class,'nba-player-index__trending-item')]")

playerList = []
players.each do |eachPlayer|
  begin
    playerName =  eachPlayer.a.title
  rescue
    playerName = 'N/A'
  end
  begin
    playerNumber = eachPlayer.span(:class => 'nba-player-trending-item__number').text
  rescue
    playerNumber = 'N/A'
  end
  begin  # "try" block
    positionHeightWeigth = eachPlayer.div(:class => 'nba-player-index__details').text
  rescue
    position = ''
    height = ''
    weight = ''
  end
  begin
    position = positionHeightWeigth[0,positionHeightWeigth.index(positionHeightWeigth[/\d+/])]
  rescue
    position = 'N/A'
  end
  begin
    height = positionHeightWeigth[positionHeightWeigth.index(positionHeightWeigth[/\d+/]),
                                positionHeightWeigth.index('|')-positionHeightWeigth.index(positionHeightWeigth[/\d+/])-1]
  rescue
    height = 'N/A'
  end
  begin
    weight = positionHeightWeigth[positionHeightWeigth.index('|')+2,positionHeightWeigth.length - positionHeightWeigth.index('|')]
  rescue
    weight = 'N/A'
  end
  begin
    teamLink = eachPlayer.a(:class => 'nba-player-index__team-image').attribute_value('href')
    teamStartIndex = find_nth_occurrence(teamLink,'/',4)
    team = teamLink[teamStartIndex,teamLink.length - teamStartIndex - 1]
  rescue
    team = 'N/A'
  end
  begin
    imagePath =   eachPlayer.img(:class => 'lazyloaded').attribute_value('data-src')
  rescue
    imagePath = ''
  end
  puts 'https:' + imagePath
  write_to_csv(playerName,playerNumber,position,height,weight,team,'https:' + imagePath,output)
  eachPlayerHash = generate_hash(playerName,playerNumber,position,height,weight,team,'https:' + imagePath)
  playerList.push(eachPlayerHash)
end


browser.close
puts playerList.size
output = JSON.generate(playerList)
puts output


