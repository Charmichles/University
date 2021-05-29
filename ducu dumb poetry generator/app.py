from pygame.constants import WINDOWHITTEST
import dumb_poet
import pygame
pygame.init()
import sys
import pyttsx3
from dataclasses import dataclass


@dataclass
class Point:
    x : int
    y : int


@dataclass
class Button:
    left : int
    top : int
    right : int
    bottom : int
    
    def is_selected(self, click : Point):
        return click.x >= self.left and click.x <= self.right and click.y >= self.top and click.y <= self.bottom


# Taken from https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
def wrap_text(text, font, width):
    """Wrap text to fit inside a given width when rendered.

    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to.

    """
    text_lines = text.replace('\t', '    ').split('\n')
    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start+1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)

    return wrapped_lines


# Taken from https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
def render_text_list(lines, font, colour=(255, 255, 255)):
    """Draw multiline text to a single surface with a transparent background.

    Draw multiple lines of text in the given font onto a single surface
    with no background colour, and return the result.

    :param lines: The lines of text to render.
    :param font: The font to render in.
    :param colour: The colour to render the font in, default is white.

    """
    rendered = [font.render(line, True, colour).convert_alpha()
                for line in lines]

    line_height = font.get_linesize()
    width = max(line.get_width() for line in rendered)
    tops = [int(round(i * line_height)) for i in range(len(rendered))]
    height = tops[-1] + font.get_height()

    surface = pygame.Surface((width, height)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    for y, line in zip(tops, rendered):
        surface.blit(line, (0, y))

    return surface


def essay_loop(screen):
    margin = 20

    def draw_text(text, screen, font, color, top_last):
        surface = render_text_list(wrap_text(text, font, width - 4 * margin), font, color)
        rect = pygame.Rect(width//2 - surface.get_width()//2, top_last + margin, surface.get_width(), surface.get_height())
        screen.blit(surface, rect)
        return rect.top + surface.get_height()
    
    def draw_page(page, page_no, title, screen, font, color):
        screen.fill(black)
        top_last = draw_text(title, screen, font_title, color, 0)
        top_last = draw_text(f'Page {page_no}\n', screen, font_subtitle, color, top_last)
        for paragraph in page:
            top_last = draw_text(paragraph, screen, font, color, top_last)
        top_last = height - 100
        draw_text('Click HERE to go to the next page.', screen, font, red, top_last)
        pygame.display.update()

    screen.fill(black)

    essay_file = open('essay.txt', 'r')
    essay_lines = essay_file.readlines()
    essay_lines = list(filter(lambda line : line != '\n', essay_lines))

    pages = []
    for i in range(1, len(essay_lines), 2):
        if essay_lines[i] != 'Bibliography:\n':
            pages.append([essay_lines[i], essay_lines[i+1]])
        else:
            break
    pages.append([])
    while i != len(essay_lines):
        pages[-1].append(essay_lines[i])
        i += 1
    for page in pages:
        print(page)
    
    page_no = 0
    draw_page(pages[page_no], page_no + 1, essay_lines[0], screen, font_essay, white)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                page_no += 1
                if page_no == len(pages):
                    run = False
                    break
                draw_page(pages[page_no], page_no + 1, essay_lines[0], screen, font_essay, white)


# Constants
size = width, height = 1024, 1024
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
screen = pygame.display.set_mode(size, pygame.NOFRAME)
clock = pygame.time.Clock()

pygame.mixer.music.load('sounds/generate.ogg')
pygame.mixer.music.set_volume(0.3)

poem_data = dumb_poet.get_poem_data('poem_data_1')
poem = ' '
buttons = {'generate' : Button(375,95,500,190), 'info' : Button(565,120,635,170), 'exit': Button(630,60,675,90)}
images = {
    'normal': pygame.transform.scale(pygame.image.load('ui_images/Normal.png'), size),
    'generate_hover': pygame.transform.scale(pygame.image.load('ui_images/POEM_Hover.png'), size),
    'generate_press': pygame.transform.scale(pygame.image.load('ui_images/POEM_Press.png'), size),
    'info_hover': pygame.transform.scale(pygame.image.load('ui_images/Question_Hover.png'), size),
    'info_press': pygame.transform.scale(pygame.image.load('ui_images/Question_Press.png'), size),
    'exit_hover': pygame.transform.scale(pygame.image.load('ui_images/X_Hover.png'), size),
    'exit_press': pygame.transform.scale(pygame.image.load('ui_images/X_Press.png'), size),
}
maskrect = images['normal'].get_rect()

font_poem = pygame.font.Font('fonts/KREON-VARIABLEFONT_WGHT.TTF', 16)
font_info = pygame.font.Font('fonts/KREON-VARIABLEFONT_WGHT.TTF', 15)
font_title = pygame.font.Font('fonts/KREON-VARIABLEFONT_WGHT.TTF', 30)
font_subtitle = pygame.font.Font('fonts/KREON-VARIABLEFONT_WGHT.TTF', 25)
font_essay = pygame.font.Font('fonts/KREON-VARIABLEFONT_WGHT.TTF', 20)
font_fallback = pygame.font.SysFont('Courier New', 15, bold=True)

# Create poem display rectangle and info text surface.
poemrect = pygame.Rect(403, 540, 225, 420)
poem_surface = render_text_list(
    wrap_text(
        '''The poet is a program that generates nonsense poetry.\n
Press POEM to generate a new poem.\n
Press ? to view the essay.\n
Press X to exit.\n
WARNING: Once the poet starts speaking, you have to wait for it to finish.\n
If you don't want the poet to speak, you can click HERE.\n
Developed by Ducu Cernitoiu and Andrei Brihac.\n
© 2021.''',
        font_info,
        240),
    font_info,
    white
    )
tts_bttn = Button(370, 530, 625, 1000)

# Load images for background animation.
bgimages = []
for id in range(1, 12):
    bgimages.append(pygame.transform.scale(pygame.image.load(f'bg_animation/{id}.png'), size))
bgrect = bgimages[0].get_rect()
current_bgimg = 0

# Initialise text-to-speech engine.
spoke = False
ttsengine = pyttsx3.init()
ttsengine.setProperty('rate', 160)
tts_enabled = True

# Draw and speak intro quote.
ttsengine.say('If the world has absolutely no sense, who\'s stopping us from inventing one?')
quote_surface = render_text_list(wrap_text('"If the world has absolutely no sense, who\'s stopping us from inventing one?"', font_title, width), font_title, white)
author_surface = render_text_list(wrap_text('- Lewis Carroll, Alice\'s Adventures in Wonderland', font_subtitle, width), font_subtitle, white)
quoterect = pygame.Rect(width//2 - quote_surface.get_width()//2, height//2 - quote_surface.get_height()//2, quote_surface.get_width(), quote_surface.get_height())
authorrect = pygame.Rect(width//2 - author_surface.get_width()//2, height//2 - author_surface.get_height()//2 + 100, author_surface.get_width(), author_surface.get_height())
screen.blit(quote_surface, quoterect)
screen.blit(author_surface, authorrect)
pygame.display.update()
ttsengine.runAndWait()

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = Point(*pygame.mouse.get_pos())
            for button_name, button in buttons.items():
                if button.is_selected(mouse_pos):
                    if button_name == 'generate':
                        poem = dumb_poet.poem_str(dumb_poet.generate_poem(*poem_data))
                        poem_surface = render_text_list(wrap_text(poem, font_poem, 240), font_poem, white)
                        poem_data = dumb_poet.get_poem_data('poem_data_1')
                        spoke = False
                    # Play sound, freeze background animation, display text on poem surface when any button is pressed.
                    screen.fill(black)
                    pygame.mixer.music.play()
                    screen.blit(bgimages[current_bgimg], bgrect)
                    screen.blit(images[button_name + '_press'], maskrect)
                    screen.blit(poem_surface, poemrect)
                    pygame.display.update()
                    pygame.time.wait(1500)
                    if button_name == 'info':
                        essay_loop(screen)
                    if button_name == 'exit':
                        sys.exit()
            if tts_bttn.is_selected(mouse_pos):
                tts_enabled = False if tts_enabled else True
                ttsengine.say('I will not speak.' if not tts_enabled else 'I will speak.')
                ttsengine.runAndWait()

    # Hover event handle.
    mask_image = images['normal']
    mouse_pos = Point(*pygame.mouse.get_pos())
    for button_name, button in buttons.items():
        if button.is_selected(mouse_pos):
            mask_image = images[button_name + '_hover']
            break
    
    # Draw sequence for every frame.
    screen.fill(black)
    screen.blit(bgimages[current_bgimg], bgrect)  # background animation
    current_bgimg = (current_bgimg+1) % len(bgimages)  # background animation
    screen.blit(mask_image, maskrect)
    screen.blit(poem_surface, poemrect)
    if not spoke and tts_enabled:  # when poem is generated and tts is enabled, speak the poem and mark it as spoken
        ttsengine.say(poem)
        ttsengine.runAndWait()
        spoke = True
    pygame.display.update()