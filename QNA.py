import requests
import time
from bs4 import BeautifulSoup
import PyPDF2 as pdf

# each site gets its own function to keep it simple

file = open('QNA.txt', 'w')
flashcard_dir = ['common-tcp-and-udp-ports', 'comptia-cable-and-medium-types', 'comptia-security-plus-acronyms', 'comptia-security-plus-protocols', 'ip-addressing', 'osi-model', 'windows-command-line']
porfessor_dict = {'PA' : [10, 44], 'PAE' : [48, 144], 'PB' : [137, 180], 'PBE' : [182, 274], 'PC' : [276, 307], 'PCE' : [310, 402]}

def crucialexams_practice_tests():
    print('Starting crucialexams practice tests extraction')
    for x in range(1, 4):
        time.sleep(1) #Cooldown, preventing block.
        r = requests.get(f"https://crucialexams.com/study/tests/comptia/sy0-501/comptia-security-plus-sy0-501-test-{x}/")
        soup = BeautifulSoup(r.text, 'html.parser')
        for i in range(1, 21):
            div = soup.find('div', {'data-question' : f'{i}'})
            question = div.p.get_text().strip(f'{i})').strip()
            answeres = div.find_all('a', {'class' : 'ungraded'})
            a = answeres[0].get_text().replace('  ', '').strip().strip('A)').strip()
            b = answeres[1].get_text().replace('  ', '').strip().strip('B)').strip()
            c = answeres[2].get_text().replace('  ', '').strip().strip('C)').strip()
            d = answeres[3].get_text().replace('  ', '').strip().strip('D)').strip()
            block = question + '\nA)' + a + '\nB)' + b + '\nC)' + c + '\nD)' + d + '\n##########\n'
            file.write(block)
    print('crucialexams Tests 1-3 saved!')

def crucialexams_flash_cards():
    print('Starting crucialexams flash card extraction')
    for x in flashcard_dir:
        time.sleep(1)
        r = requests.get(f'https://crucialexams.com/study/flashcards/{x}/')
        soup = BeautifulSoup(r.text, 'html.parser')
        div = soup.find_all('div', {'class' : 'card'})
        for i in div:
            card = i.get_text().strip().split('\n')
            block = card[0] + ' : ' + card[1] + '\n##########\n'
            file.write(block)
    print('Flash Cards Saved!')

def netwrix():
    n = 0
    print('Starting Netwrix Quiz extraction')
    r = requests.get("https://blog.netwrix.com/2019/02/05/getting-ready-comptia-security-practice-test/")
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find_all('div', {'wpProQuiz_question_text'})
    li = soup.find_all('li', {'class' : 'wpProQuiz_questionListItem'})
    for i in div:
        question = i.get_text().strip()
        file.write('\n##########\n' + question)
        for i in range(n, n + 4):
            file.write('\n' + li[i].get_text().strip() + '\n')
        n += 4
    print('Netwrix quizes Saved!')

def professor_messer():
    print('Starting professor messer practice exam pdf extraction')
    try:
        professor = open('PATH TO PROFESSER MESSER PRACTICE QUESTIONS PDF', 'rb')
    except:
        print('Professor messer practice questions pdf not found, skipping... \n\nPlease paste the path to the pdf in the script\n')
        return None
    read_pdf = pdf.PdfFileReader(professor)
    for i in porfessor_dict.keys():
        for x in range(porfessor_dict[i][0], porfessor_dict[i][1]):
            page = read_pdf.getPage(x)
            page_content = page.extractText()
            block = page_content + '\n##########\n'
            file.write(block)
    professor.close()
    print('Professor messer Practice exams saved!')

if __name__ == '__main__':
    print('Creating QNA.txt')
    crucialexams_practice_tests()
    crucialexams_flash_cards()
    netwrix()
    professor_messer()


file.close()
