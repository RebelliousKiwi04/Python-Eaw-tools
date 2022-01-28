import lxml.etree as et
import sys
from gameObject.GameObjectRepository import *
from gameObject.TextHandler import *
print("Running")
eawxText = TextFile('''C:\Program Files (x86)\Steam\SteamApps\common\Star Wars Empire at War\corruption\Mods\EmpireAtWarExpanded\Data''', 'dict')
teststring = '''	<Planet Name="Abregado_Rae">
 		<Zoomed_Terrain_Index>0</Zoomed_Terrain_Index>
		<Text_ID>TEXT_OBJECT_STAR_SYSTEM_ABREGADORAE</Text_ID>
		<Loop_Idle_Anim_00>Yes</Loop_Idle_Anim_00>
		<Always_Instantiate_Galactic>yes</Always_Instantiate_Galactic>
		<Galactic_Model_Name>W_planet_Temperate01.alo</Galactic_Model_Name>
		<Destroyed_Galactic_Model_Name>W_planet_Asteroids.alo</Destroyed_Galactic_Model_Name>
		<GUI_Model_Name>W_planet_Temperate01.alo</GUI_Model_Name>
		<Mass>1.0</Mass>
		<Scale_Factor>0.9</Scale_Factor>
		<Mouse_Collide_Override_Sphere_Radius> 19.77 </Mouse_Collide_Override_Sphere_Radius>
		<Show_Name>Yes</Show_Name>
		<Name_Adjust>-12, -12, 0.1</Name_Adjust>
		<Behavior>SELECTABLE, PLANET, PRODUCTION</Behavior>
		<Pre_Lit>no</Pre_Lit>
		<Political_Control>0</Political_Control>
		<Camera_Aligned>yes</Camera_Aligned>
		<Facing_Adjust>0.0, 0.0, 0.0</Facing_Adjust>
		<Terrain>Temperate</Terrain>
		<Planet_Credit_Value>70</Planet_Credit_Value>
		<Planet_Destroyed_Credit_Value>6</Planet_Destroyed_Credit_Value>
		<Galactic_Position>-43.0, -143.0, 10.0</Galactic_Position>
		<Special_Structures_Land>3</Special_Structures_Land>
		<Special_Structures_Space>2</Special_Structures_Space>
		<Max_Space_Base>4</Max_Space_Base>
		<The_Force>Neutral</The_Force>
		<Force_Strength>0.0</Force_Strength>
		<Planet_Surface_Accessible> Yes </Planet_Surface_Accessible>
		<Land_Tactical_Map> _Land_Planet_AbregadoRae_02.ted </Land_Tactical_Map>
		<Space_Tactical_Map>_Space_Planet_AbregadoRae_01.ted</Space_Tactical_Map>
		<Destroyed_Space_Tactical_Map/>

		<Describe_Population>TEXT_PLANET_ABREGADORAE_INFO_POP</Describe_Population>
		<Describe_Wildlife>TEXT_PLANET_ABREGADORAE_INFO_WL</Describe_Wildlife>
		<Describe_Terrain>TEXT_PLANET_ABREGADORAE_INFO_TER</Describe_Terrain>
		<Describe_Weather>TEXT_PLANET_ABREGADORAE_INFO_WEA</Describe_Weather>
		<Describe_Tactical>TEXT_PLANET_ABREGADORAE_ENCYC_01</Describe_Tactical>
		<Describe_Advantage>TEXT_PLANET_ABREGADORAE_INFO_ADV_01</Describe_Advantage>
		<Describe_History>TEXT_PLANET_ABREGADORAE_INFO_HIS_01</Describe_History>

		<Planet_Ability_Name> TEXT_PLANET_ABREGADORAE_INFO_ADV_01 </Planet_Ability_Name>
		<Planet_Ability_Description> TEXT_PLANET_ABREGADORAE_ENCYC_01 </Planet_Ability_Description>

		<Encyclopedia_Text>TEXT_PLANET_ABREGADORAE_ENCYC_01</Encyclopedia_Text>
		<Encyclopedia_Weather_Icon>i_pa_weather_rain.tga</Encyclopedia_Weather_Icon>
		<Encyclopedia_Weather_Name>TEXT_WEATHER_NAME_RAIN</Encyclopedia_Weather_Name>
		<Encyclopedia_Weather_Info>TEXT_TACTICAL_WEATHER_OBJECTIVE_RAIN</Encyclopedia_Weather_Info>
		<Planet_Ability_Icon>i_pa_galactic_production_boost.tga</Planet_Ability_Icon>
		<Native_Icon_Name>load_swamp.tga</Native_Icon_Name>

		<Additional_Population_Capacity>50</Additional_Population_Capacity>

	</Planet>'''
mod_dir = """C:\Program Files (x86)\Steam\SteamApps\common\Star Wars Empire at War\corruption\Mods\Chelmod\Data"""
repository = ModRepository(mod_dir, open('logfile', 'w'))
root = et.Element('Planets')
for planet in repository.planets:
	planetroot = et.fromstring(teststring)
	planetroot.set('Name', planet.name)
	for i in planetroot:
		if i.tag == 'Galactic_Position':
			i.text = f'{planet.x}, {planet.y}, 10.0'
		if i.tag == 'Max_Space_Base':
			i.text = planet.max_space_base
		if i.tag == 'Galactic_Model_Name':
			i.text = planet.galactic_model
		if i.tag == 'Destroyed_Galactic_Model_Name':
			i.text = planet.destroyed_model
		if i.tag == 'Zoomed_Terrain_Index':
			i.text = planet.terrain_index
		if i.tag =='Land_Tactical_Map':
			if planet.land_map not in os.listdir('''C:\Program Files (x86)\Steam\SteamApps\common\Star Wars Empire at War\corruption\Mods\Chelmod\Data\Art\Maps'''):
				i.text =='_Land_Planet_AbregadoRae_02.ted'
		if i.tag =='Space_Tactical_Map':
			if planet.space_map not in os.listdir('''C:\Program Files (x86)\Steam\SteamApps\common\Star Wars Empire at War\corruption\Mods\Chelmod\Data\Art\Maps'''):
				i.text == '_Space_Planet_AbregadoRae_01.ted'
		if i.tag == 'Text_ID':
			i.text = 'TEXT_OBJECT_STAR_SYSTEM_'+planet.name.upper()
	root.append(planetroot)

campaignFilesET = et.ElementTree(root)
campaignFilesET.write('testfile2.xml',xml_declaration=True, encoding='UTF-8',pretty_print=True)

# planetRepo = et.parse('testfile2.xml')

# planetRepoRoot = planetRepo.getroot()

# newPlanets = et.parse('testfile2.xml')
# newPlanetsRoot = newPlanets.getroot()


# for i in planetRepoRoot:
# 	for j in i:
# 		if j.tag =='Galactic_Position':
# 			entry = j.text
# 			print(entry)
# 			entry = entry.replace(',',' ')
# 			entry = entry.split()
# 			newentry = []
# 			for i in entry:
# 				i = float(i)*3
# 				newentry.append(i)
# 			print(newentry)
# 			j.text = f'{newentry[0]}, {newentry[1]}, 10.0'
# Tree = et.ElementTree(planetRepoRoot)
# Tree.write('TestingAgain.xml',xml_declaration=True, encoding='UTF-8',pretty_print=True)


# for x in planetRepoRoot:
# 	name = x.get('Name').replace(' ','_')
# 	nam3 = name.replace("'",'')
# 	namE2 = nam3.replace('-','_')
# 	x.set('Name', namE2)
# 	for j in newPlanetsRoot:
# 		if name == j.get('Name'):
# 			print(name)
# 			for i in j:
# 				if i.tag == 'Max_Space_Base':
# 					x.find('Max_Space_Base').text = i.text
# 				if i.tag == 'Galactic_Model_Name':
# 					x.find('Galactic_Model_Name').text = i.text
# 				if i.tag == 'Destroyed_Galactic_Model_Name':
# 					x.find('Destroyed_Galactic_Model_Name').text = i.text
# 				if i.tag == 'Zoomed_Terrain_Index':
# 					x.find('Zoomed_Terrain_Index').text = i.text
# 				if i.tag =='Land_Tactical_Map':
# 					x.find('Land_Tactical_Map').text = i.text
# 				if i.tag =='Space_Tactical_Map':
# 					x.find('Space_Tactical_Map').text = i.text
# 				if i.tag == 'Text_ID':
# 					x.find('Text_ID').text = i.text
# Tree = et.ElementTree(planetRepoRoot)
# Tree.write('PlanetsTestFile.xml',xml_declaration=True, encoding='UTF-8',pretty_print=True)
