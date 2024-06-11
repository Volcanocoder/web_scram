from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

class BlogScraperApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.url_input = TextInput(hint_text='Enter blog page URL', size_hint_y=None, height=50)
        layout.add_widget(self.url_input)

        self.filepath_input = TextInput(hint_text='Enter directory path', size_hint_y=None, height=50)
        layout.add_widget(self.filepath_input)

        self.save_button = Button(text='Save to CSV', size_hint_y=None, height=50)
        self.save_button.bind(on_release=self.save_to_csv)
        layout.add_widget(self.save_button)

        self.status_label = Label(text='', size_hint_y=None, height=50)
        layout.add_widget(self.status_label)

        return layout

    def save_to_csv(self, instance):
        url = self.url_input.text.strip()
        directory_path = self.filepath_input.text.strip()

        if not url:
            self.status_label.text = 'Please enter the blog page URL.'
            return

        if not directory_path:
            self.status_label.text = 'Please enter the directory path.'
            return

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extracting blog content
            blog_content = ''
            for paragraph in soup.find_all('p'):
                blog_content += paragraph.get_text() + '\n'

            # Generating filename based on current date and time
            current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = f'{current_datetime}.csv'

            # Writing content to CSV file
            filepath = f'{directory_path}/{filename}'
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Blog Content'])
                csvwriter.writerow([blog_content])

            self.status_label.text = f'Content saved to {filepath}'
        except requests.exceptions.RequestException as e:
            self.status_label.text = f'Error fetching blog content: {e}'
        except Exception as e:
            self.status_label.text = f'Error: {e}'

if __name__ == '__main__':
    BlogScraperApp().run()



#myenv\Scripts\activate
