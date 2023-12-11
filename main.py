import attempt1
import scraper
import re

"""
wiki = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower from 1887 to 1889.Locally nicknamed \"La dame de fer\" (French for \"Iron Lady\"), it was constructed as the centerpiece of the 1889 World's Fair, and to crown the centennial anniversary of the French Revolution. Although initially criticised by some of France's leading artists and intellectuals for its design, it has since become a global cultural icon of France and one of the most recognisable structures in the world. The tower received 5,889,000 visitors in 2022. The Eiffel Tower is the most visited monument with an entrance fee in the world: 6.91 million people ascended it in 2015. It was designated a monument historique in 1964, and was named part of a UNESCO World Heritage Site (\"Paris, Banks of the Seine\") in 1991. The tower is 330 metres (1,083 ft) tall,[8] about the same height as an 81-storey building, and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest human-made structure in the world, a title it held for 41 years until the Chrysler Building in New York City was finished in 1930. It was the first structure in the world to surpass both the 200-metre and 300-metre mark in height. Due to the addition of a broadcasting aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure in France after the Millau Viaduct.The tower has three levels for visitors, with restaurants on the first and second levels. The top level's upper platform is 276 m (906 ft) above the ground - the highest observation deck accessible to the public in the European Union. Tickets can be purchased to ascend by stairs or lift to the first and second levels. The climb from ground level to the first level is over 300 steps, as is the climb from the first level to the second, making the entire ascent a 600 step climb. Although there is a staircase to the top level, it is usually accessible only by lift. On this top, third level is a private apartment built for Gustave Eiffel's private use. He decorated it with furniture by Jean Lachaise and invited friends such as Thomas Edison."
#wiki = "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."
question_arr_relat=[]
question_arr_relat.append("Is the Eiffel Tower located in Paris?")#true
question_arr_relat.append("Is the Eiffel Tower nicknamed \"La dame de croissant\"?")#false
question_arr_relat.append("Does the Eiffel Tower have four levels")#false
question_arr_relat.append("Is the Eiffel Tower in China?")#false
question_arr_relat.append("Is it named after the engineer Gustave Eiffel")#true
"""

#'https://en.wikipedia.org/wiki/Python_(programming_language)'
# https://en.wikipedia.org/wiki/Eiffel_Tower

wiki = input("Provide wiki link: ")
print(f"You entered: {wiki}")
returned_from_scraper=scraper.download_wiki_page(wiki)
print(returned_from_scraper)
print("--------------------------")

returned_from_scraper_cleaned=re.sub(r'\[.*?\]', '', returned_from_scraper)#to remove stuff inside square brackets
returned_from_scraper_cleaned=returned_from_scraper_cleaned.replace('"', '\\"')
returned_from_scraper_cleaned=returned_from_scraper_cleaned.replace('\n', '')
print(returned_from_scraper_cleaned)

while True:
    question = input("Provide question: ")
    print(f"You entered: {question}")
    attempt1.ner_on_question(question,wiki)


"""
for question in question_arr_relat:
    attempt1.ner_on_question(question,wiki)
"""
