from kivymd.app import MDApp
from kivy.lang import Builder
from Dict import Dictionary
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineAvatarIconListItem, MDList, OneLineAvatarListItem, IRightBodyTouch
from kivymd.utils.fitimage import FitImage
from kivymd.uix.selectioncontrol import MDCheckbox


import os
import json
from plyer import tts

kv = '''
#: import StiffScrollEffect kivymd.effects.stiffscroll.StiffScrollEffect
<SearchToolbar>
	adaptive_height: True
	pos_hint: {'top': 1}
	md_bg_color: app.theme_cls.primary_color
	MDGridLayout:
		cols: 2
		adaptive_height: True
		id: bar
		padding: 0, 0, 0, 10
		MDBoxLayout:
			adaptive_height: True
			size_hint_x: .8
			padding: 65, 0, 0, 0
			MDTextField:
				id: text
				hint_text: 'Enter Word Here'
				mode: 'fill'
				color_mode: 'custom'
				line_color_focus: 1, 1, 1, 1
				on_text: app.showWord(self)
		MDBoxLayout:
			size_hint_x: .2
			adaptive_height: True
			padding: 20, 0, 0, 0
			MDIconButton:
				icon: 'magnify'
				theme_text_color: 'Custom'
				text_color: 1, 1, 1, 1
				pos_hint: {'x': 1}
				on_press: app.getsearchword()

<ContentDrawer@MDBoxLayout>
	orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"
    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height
        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "Images/images.jpg"
    MDLabel:
        text: "Gab's Mini Dictionary"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]
        theme_text_color: 'Custom'
        text_color: app.theme_cls.primary_dark
        bold: True
    MDLabel:
        text: "gabrieloranekwu@gmail.com"
        font_style: "Caption"
        size_hint_y: None
        theme_text_color: 'Custom'
        text_color: app.theme_cls.primary_dark
        height: self.texture_size[1]
        bold: True
    Widget:
    	size_hint_y: .1
	ScrollView:
		effect_cls: StiffScrollEffect
		MDList:
			OneLineAvatarIconListItem:
				text: 'Dark Theme'
				theme_text_color: 'Custom'
				text_color: app.theme_cls.primary_dark
				on_press:
					app.theme_cls.theme_style='Light' if theme.icon =='weather-sunny-off' else 'Dark'
					app.config.set('Appearance', 'theme', app.theme_cls.theme_style)
					app.config.update_config('main.ini')
				IconLeftWidget:
					id: theme
					icon: 'weather-sunny' if app.theme_cls.theme_style == 'Light' else 'weather-sunny-off'
					theme_text_color: 'Custom'
					text_color: app.additional_color
				ToggleBox:
					active: False if app.theme_cls.theme_style == 'Light' else True
					on_active:
						app.theme_cls.theme_style = 'Light' if theme.icon =='weather-sunny-off' else 'Dark'
			OneLineIconListItem:
				text: 'Home'
				on_press:
					app.changeOptionScreen('home', 'left')
					root.navmenu.set_state('close')
					app.changeMeaningScreen('default', 'left', False, 0) if app.root.ids.meaning_manager.current == 'default' else app.changeMeaningScreen('default', 'right', False, 0.4)
				IconLeftWidget:
					icon: 'home'
					theme_text_color: 'Custom'
					text_color: app.additional_color
			OneLineIconListItem:
				text: 'History'
				on_press:
					app.changeOptionScreen('history', 'left')
					root.navmenu.set_state('close')
				IconLeftWidget:
					icon: 'history'
					theme_text_color: 'Custom'
					text_color: app.additional_color
			OneLineIconListItem:
				text: 'Notes'
				on_press:
					app.changeOptionScreen('notes', 'left')
					root.navmenu.set_state('close')
				IconLeftWidget:
					icon: 'notebook'
					theme_text_color: 'Custom'
					text_color: app.additional_color
			OneLineIconListItem:
				text: 'Bookmark'
				on_press:
					app.changeOptionScreen('bookmark', 'left')
					root.navmenu.set_state('close')
				IconLeftWidget:
					icon: 'star-face'
					theme_text_color: 'Custom'
					text_color: app.additional_color
			OneLineIconListItem:
				text: 'About Us'
				on_press:
					app.changeOptionScreen('about us', 'left')
					root.navmenu.set_state('close')
				IconLeftWidget:
					icon: 'information'
					theme_text_color: 'Custom'
					text_color: app.additional_color
			OneLineIconListItem:
				text: 'Exit'
				on_press:
					root.navmenu.set_state('close')
					app.exit()
				IconLeftWidget:
					icon: 'exit-to-app'
					theme_text_color: 'Custom'
					text_color: app.additional_color
	Widget:
		size_hint_y: .1

<OneLineIconListItem>
	_no_ripple_effect: True
	theme_text_color: 'Custom'
	text_color: app.theme_cls.primary_dark

<CustomRound@MDFloatingActionButton>:
	md_bg_color: app.additional_color
	theme_text_color: 'Custom'
	text_color: 1, 1, 1, 1
	
<CustomListItem>
	on_press: app.root.ids.history.viewMeaning(self.text)
	IconRightWidget:
		icon: 'close'
		on_press:
			app.deleteAction(root.call, root.text)
	IconLeftWidget:
		icon: 'apps'

<CustomNoteItem>
	on_press:
		app.root.ids.notes.showNote(self.text)
	IconRightWidget:
		icon: 'close'
		on_press:
			root.parent.parent.parent.parent.deleteNote(root.text)
	IconLeftWidget:
		icon: 'apps'

<ScrollBox>
	orientation: 'vertical'
	RecycleView:
		effect_cls: StiffScrollEffect
        id: list
        key_viewclass: 'viewclass'
        key_size: 'height'

        RecycleBoxLayout:
            padding: dp(10)
            default_size: None, dp(48)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

MDFloatLayout:
	searchbar: searchbar
	MDNavigationLayout:
		ScreenManager:
			MDScreen:
				MDBoxLayout:
					orientation: 'vertical'
					MDToolbar:
						id: custnav
						title: 'PYCIFY DICTIONARY'
						bold: True
						font_style: 'Button'
						specific_text_color: [1, 1, 1, 1] if app.theme_cls.theme_style == 'Light' else [0, 0, 0, 1]
						font_size: '20dp'
						anchor_title: 'center'
						left_action_items: [['menu', lambda x: nav.set_state('toggle')]]
					ScreenManager:
						id: option_manager
						MDScreen:
							name: 'home'
							on_pre_enter:
								custnav.title = 'PYCIFY DICTIONARY'
							MDBoxLayout:
								orientation: 'vertical'
								MDBoxLayout:
									id: toolbar
									adaptive_height: True
									size_hint_y: None
									SearchToolbar
										id: searchbar
								BoxLayout:
									ScreenManager:
										id: meaning_manager
										DefaultScreen:
											name: 'default'
										MeaningScreen:
											name: 'meaning'
											main: app
											id: meaning
						HistoryScreen:
							name: 'history'
							main: app
							id: history
							on_pre_enter:
								self.loadScreen()
								custnav.title = self.name.upper()
							on_pre_leave:
								custnav.right_action_items = []
						BookmarkScreen:
							name: 'bookmark'
							id: bookmark
							main: app
							on_pre_enter:
								self.loadScreen()
								custnav.title = self.name.upper()
							on_pre_leave:
								custnav.right_action_items = []
						NotesScreen:
							name: 'notes'
							id: notes
							main: app
							on_pre_enter:
								self.loadScreen()
								custnav.title = self.name.upper()
							on_pre_leave:
								custnav.right_action_items = []
						AboutScreen:
							name: 'about us'
							on_pre_enter:
								custnav.title = self.name.upper()
		MDNavigationDrawer:
			id: nav
			ContentDrawer
				navmenu: nav
'''

class ScrollBox(MDBoxLayout):
	pass
	
class CustomListItem(OneLineAvatarIconListItem):
	call = ObjectProperty()

class CustomNoteItem(OneLineAvatarIconListItem):
	pass

class CustomMeaningList(MDBoxLayout):
	text = StringProperty()
	number = StringProperty()

class HistoryScreen(MDScreen):
	main = ObjectProperty(None)
	no_content = FitImage(source='Images/empty.png')
	def loadScreen(self):
		if self.main.config.get('Data', 'history'):
			self.main.root.ids.custnav.right_action_items = [['delete', lambda x: self.deleteAll(x)]]
		else:
			self.main.root.ids.custnav.right_action_items = []
		self.clear_widgets()
		self.container = ScrollBox()
		if self.main.config.get('Data','history'):
			for words in tuple(self.main.config.get('Data', 'history').split(',')):
				self.container.ids.list.data.append(
					{
					"viewclass": "CustomListItem",
                    "text": words,
                    "call": self,
					}
					)
			self.add_widget(self.container)
		else:
			self.md_bg_color = [1, 1, 1, 1] if self.main.theme_cls.theme_style == 'Light' else [0, 0, 0, 0]
			self.add_widget(self.no_content)

	def deleteAll(self, can):
		def delete(call):
			self.main.config.set('Data', 'history', '')
			self.main.config.update_config('main.ini')
			self.loadScreen()
			can.right_action_items = []
			call.dismiss()
		clearAll = MDDialog(title='Do You Want To Delete All Saved History?',
						auto_dismiss=True,
						buttons=[
				     	MDFlatButton(text='CANCEL', on_press=lambda x:clearAll.dismiss()),
						MDRaisedButton(text='PROCEED', on_press=lambda x: delete(clearAll))])
		clearAll.open()

	def viewMeaning(self, text):
		self.main.changeOptionScreen('home', 'down', True)
		self.main.searchword = text
		self.main.searchMeaning(text)

class BookmarkScreen(MDScreen):
	main = ObjectProperty(None)
	no_content = FitImage(source='Images/empty.png')
	def loadScreen(self):
		if self.main.config.get('Data', 'bookmark'):
			self.main.root.ids.custnav.right_action_items = [['delete', lambda x: self.deleteAll(x)]]
		else:
			self.main.root.ids.custnav.right_action_items = []
		self.clear_widgets()
		self.container = ScrollBox()
		if self.main.config.get('Data','bookmark'):
			for words in tuple(self.main.config.get('Data', 'bookmark').split(',')):
				self.container.ids.list.data.append(
					{
					"viewclass": "CustomListItem",
                    "text": words,
                    "call": self,
					}
					)
			self.add_widget(self.container)
		else:
			self.md_bg_color = [1, 1, 1, 1] if self.main.theme_cls.theme_style == 'Light' else [0, 0, 0, 0]
			self.add_widget(self.no_content)

	def deleteAll(self, can):
		def delete(call):
			self.main.config.set('Data', 'bookmark', '')
			self.main.config.update_config('main.ini')
			self.loadScreen()
			can.right_action_items = []
			call.dismiss()
		clearAll = MDDialog(title='Do You Want To Delete All Saved Bookmarks?',
						auto_dismiss=True,
						buttons=[
				     	MDFlatButton(text='CANCEL', on_press=lambda x:clearAll.dismiss()),
						MDRaisedButton(text='PROCEED', on_press=lambda x: delete(clearAll))])
		clearAll.open()

	def viewMeaning(self, text):
		self.main.changeOptionScreen('home', 'down', True)
		self.main.searchword = text
		self.main.searchMeaning(text)

class NotesScreen(MDScreen):
	main = ObjectProperty()
	no_content = FitImage(source='Images/empty.png')
	def loadScreen(self):
		if self.main.config.options('Notes'):
			self.main.root.ids.custnav.right_action_items = [['delete', lambda x: self.deleteAll(x)]]
		else:
			self.main.root.ids.custnav.right_action_items = []

		self.clear_widgets()
		self.container = ScrollBox()
		if len(list(self.main.config['Notes'])) != 0:
			for note in self.main.config['Notes']:
				self.container.ids.list.data.append(
						{
						"viewclass": "CustomNoteItem",
	                    "text": note,
						}
						)
			self.add_widget(self.container)
		else:
			self.md_bg_color = [1, 1, 1, 1] if self.main.theme_cls.theme_style == 'Light' else [0, 0, 0, 0]
			self.add_widget(self.no_content)

	def deleteNote(self, note):
		self.main.config.remove_option('Notes', note)
		self.loadScreen()
		self.main.config.update_config('main.ini')
		if len(list(self.main.config['Notes'])) == 0:
			self.main.root.ids.custnav.right_action_items = []
		toast(f'Deleted "{note}" Successfully...')

	def deleteAll(self, can):
		def delete(call):
			self.main.config.remove_section('Notes')
			self.main.config.update_config('main.ini')
			self.clear_widgets()
			self.loadScreen()
			can.right_action_items = []
			call.dismiss()
		clearAll = MDDialog(title='Do You Want To Delete All Saved Notes?',
						auto_dismiss=True,
						buttons=[
				     	MDFlatButton(text='CANCEL', on_press=lambda x:clearAll.dismiss()),
						MDRaisedButton(text='PROCEED', on_press=lambda x: delete(clearAll))])
		clearAll.open()

	def showNote(self, text):
		note = self.main.config['Notes'][text]
		reveal = MDDialog(auto_dismiss=True,
						  title=text,
						  text=note,
						  buttons=[
					     	MDFlatButton(text='CLOSE', on_press=lambda x:reveal.dismiss())]
						  )
		reveal.open()

class AboutScreen(MDScreen):
	shown = False
	def on_pre_enter(self):
		if not self.shown:
			with open('Store/About.txt')as file:
				self.shown = file.read()
			self.ids.about_lbl.text = self.shown

class ToggleBox(IRightBodyTouch, MDCheckbox):
    pass


class MakeNote(MDBoxLayout):
	text = StringProperty()

class MeaningScreen(MDScreen):
	main = ObjectProperty()
	searchword = StringProperty()

	def on_pre_enter(self):
		self.loadScreen()
		
	def loadScreen(self):
		try:
			self.searchword = self.main.searchword
		except ValueError:
			pass
		self.ids.container.data = []
		if self.searchword in self.main.config.get('Data', 'bookmark'):
			self.ids.star.text_color = [0,1,0,1]
		else:
			self.ids.star.text_color = self.main.additional_color
		for number, meaning in enumerate(self.main.meaning):
			self.ids.container.data.append(
			{
			'viewclass': 'CustomMeaningList',
			'text': meaning,
			'number': str(number+1)
			}
			)

	def starMarker(self, star, word):
		bookmarks = self.main.config.get('Data', 'bookmark')
		if star.text_color == [0,1,0,1]:
			star.text_color = self.main.additional_color
			if ',' in bookmarks:
				bookmarks = bookmarks.replace(word+',', '')
			else:
				bookmarks = bookmarks.replace(word, '')
			self.main.config.set('Data', 'bookmark', bookmarks)
			toast('Unstarred...')
		else:
			star.text_color = 0,1,0,1
			if len(bookmarks) == 0:
				self.main.config.set('Data', 'bookmark', bookmarks+word)
			else:
				self.main.config.set('Data', 'bookmark', bookmarks+','+word)
			toast('Starred...')
		if word not in self.main.config.get('Data', 'bookmark'):
			self.main.config.update_config('main.ini')

	def say(self, word):
		tts.speak(word)

	def addToNotes(self, word):
		def addNote(word, text):
			if 0 < len(text) <= 50:
				self.main.config.set('Notes', word, text)
				self.main.config.update_config('main.ini')
				toast('Saved Note !...')
			makenote.dismiss()

		makenotecontent = MakeNote()
		makenote =  MDDialog(title=word,
							auto_dismiss=True,
							type='custom',
							content_cls=makenotecontent,
							buttons=[
				     	MDFlatButton(text='CANCEL', on_press=lambda x:makenote.dismiss()),
						MDRaisedButton(text='SAVE', on_press=lambda x: addNote(word, makenotecontent.ids.note.text))])
		makenote.open()

class DefaultScreen(MDScreen):
	pass

class SearchToolbar(MDBoxLayout):
	pass

class Main(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.additional_color = [255/255, 141/255, 0, 1]
		self.meaning_manager_screens = ['default']
		self.option_manager_screens = ['home']
		self.dictionary = Dictionary('Store/words.json')
		self.allmeaning = JsonStore('words.json')
		self.searchword = StringProperty()
		self.image = 'Images/images.jpg'
		self.meaning = []
		self.addtostore = False
		self.close_words = MDDropdownMenu(width_mult=2.3)

	def open_settings(self):
		self.root.ids.nav.set_state('toggle')

	def build_config(self, config):
		config.setdefaults('Appearance', {'theme': 'Light'})
		config.setdefaults('Data', {'bookmark': ''})
		config.setdefaults('Data', {'history': ''})
		config.add_section('Notes')
	
	def build(self):
		#self.history = HistoryScreen()
		self.theme_cls.primary_palette = 'LightBlue'
		for screens in os.listdir('Screens'):
			Builder.load_file(os.path.join('Screens', screens))
		Window.bind(on_keyboard=self.event)
		return Builder.load_string(kv)

	def on_start(self):
		self.theme_cls.theme_style = self.config.get('Appearance', 'theme')
		
	def only(self, lis):
	 	new = []
		for i in lis:
			if i in new:
				pass
			else:
				new.append(i)
		return new

	def showWord(self, word):
		pass
		# if len(word.text) != 0:
		# 	self.close_words.dismiss()
		# 	self.close_words.caller = word
		# 	print(word.text)
		# 	self.close_words.items = [{"text": f"{i}"} for i in word.text]
		# 	self.close_words.open()
		# else:
		# 	self.close_words.dismiss()
		
	def changeMeaningScreen(self, name, direction, add=True, duration=0.4):
		self.root.ids.meaning_manager.transition.direction = direction
		self.root.ids.meaning_manager.transition.duration= duration
		if name == 'meaning':
			self.root.ids.meaning_manager.current = 'default'
			self.root.ids.meaning_manager.current = 'meaning'
		elif name == 'default':
			self.root.ids.meaning_manager.current = 'meaning'
			self.root.ids.meaning_manager.current = 'default'
		if add:
			self.meaning_manager_screens.append(name)
		self.meaning_manager_screens = self.only(self.meaning_manager_screens)

	def changeOptionScreen(self, name, direction, add=True):
		#back is False, front is True
		self.root.ids.option_manager.transition.direction = direction
		self.root.ids.option_manager.current = name
		if add:
			self.option_manager_screens.append(name)
		self.option_manager_screens = self.only(self.option_manager_screens)
		if self.option_manager_screens[-1] != 'home' and self.root.ids.option_manager.current == 'home':
			self.option_manager_screens.pop()
		
	def backMeaning(self, clear):
		#back is False, front is True
		self.meaning_manager_screens.pop()
		self.changeMeaningScreen(self.meaning_manager_screens[-1], 'right', False)
		if clear:		
			self.root.searchbar.ids.text.text = ''

	def backOption(self):
		self.option_manager_screens.pop()
		self.changeOptionScreen(self.option_manager_screens[-1], 'right', False)

	def event(self,window,key,*args):
		if key == 13:
			self.searchword = self.root.ids.searchbar.ids.text.text
			self.addtostore = True
			self.searchMeaning(self.searchword)
		if key in (1001, 27):
			if self.root.ids.option_manager.current == 'home':
				if self.root.ids.meaning_manager.current == 'default':
					self.exit()
				else:
					self.backMeaning(True)
			else:
				self.backOption()
		return True

	def exit(self):
		leave = MDDialog(title='Do You Want To Leave?',
						auto_dismiss=True,
						buttons=[
				     	MDFlatButton(text='CANCEL', on_press=lambda x:leave.dismiss()),
						MDRaisedButton(text='QUIT', on_press=lambda x: self.stop())])
		leave.open()
	
	def getsearchword(self):
		if self.root.ids.searchbar.ids.text.text:
			self.searchword=self.root.ids.searchbar.ids.text.text
			self.addtostore = True
			self.searchMeaning(self.searchword)
			
	def getrandomword(self):
		self.searchword = self.dictionary.getRandom()
		self.addtostore = False
		self.searchMeaning(self.searchword)
		
	def searchMeaning(self, word):
		self.meaning = self.dictionary.meaning(word)
		if len(self.meaning) != 0:
			if self.addtostore:
				if word not in self.config.get('Data', 'history'):
					if len(self.config.get('Data', 'history')) == 0:
						self.config.set('Data', 'history', word)
					else:
						history = self.config.get('Data', 'history')
						self.config.set('Data', 'history', history+','+word)
					self.config.update_config('main.ini')
			self.changeMeaningScreen('meaning', 'left')

	def deleteAction(self, screen, text):
		if screen.name == 'history':
			history = self.config.get('Data', 'history')
			if history[0:len(text)] == text:
				if ',' in history:
					history = history.replace(text+',', '')
				else:
					history = history.replace(text, '')
			else:
				history = history.replace(','+text, '')
			self.config.set('Data', 'history', history)
			self.config.update_config('main.ini')
			screen.loadScreen()
			toast(f'Deleted "{text}" Successfully...')

		elif screen.name == 'bookmark':
			bookmarks = self.config.get('Data', 'bookmark')
			if bookmarks[0:len(text)] == text:
				if ',' in bookmarks:
					bookmarks = bookmarks.replace(text+',', '')
				else:
					bookmarks = bookmarks.replace(text, '')
			else:
				bookmarks = bookmarks.replace(','+text, '')
			self.config.set('Data', 'bookmark', bookmarks)
			self.config.update_config('main.ini')
			screen.loadScreen()
			toast(f'Deleted "{text}" Successfully...')
		
Main().run()