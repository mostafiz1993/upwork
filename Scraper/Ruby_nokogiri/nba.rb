require 'nokogiri'
require 'open-uri'
require 'json'


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

html_data = open('http://www.nba.com/players').read
nokogiriObject = Nokogiri::HTML(html_data)
players = nokogiriObject.xpath("//section[starts-with(@class,'nba-player-index__trending-item')]")

playerList = []
players.each do |eachPlayer|
  playerName = eachPlayer.css("a")[0].attr('title')
  playerNumber = eachPlayer.css("span[@class='nba-player-trending-item__number']").text
  positionHeightWeigth = eachPlayer.css("div[@class='nba-player-index__details']").text
  position = positionHeightWeigth[0,positionHeightWeigth.index(positionHeightWeigth[/\d+/])]
  height = positionHeightWeigth[positionHeightWeigth.index(positionHeightWeigth[/\d+/]),
                                positionHeightWeigth.index('|')-positionHeightWeigth.index(positionHeightWeigth[/\d+/])-1]
  weight = positionHeightWeigth[positionHeightWeigth.index('|')+2,positionHeightWeigth.length - positionHeightWeigth.index('|')]
  teamLink  = eachPlayer.css("a[class='nba-player-index__team-image']").attr('href').text
  teamStartIndex = find_nth_occurrence(teamLink,'/',2)
  team = teamLink[teamStartIndex,teamLink.length - teamStartIndex - 1]
  imagePath = 'https:' + eachPlayer.css("img[@class='lazyload']").attr('data-src')
  eachPlayerHash = generate_hash(playerName,playerNumber,position,height,weight,team,imagePath)
  playerList.push(eachPlayerHash)
end
output = JSON.generate(playerList)
puts output