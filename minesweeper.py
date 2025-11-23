import pygame
import random
import time
import sys
import json
import os
import math
import struct

# --- DİL VE METİN AYARLARI ---
LOCALES = {
    "EN": {
        "GAME_BTN": "GAME",
        "NEW": "New Game (F2)",
        "BEG": "Beginner",
        "INT": "Intermediate",
        "EXP": "Expert",
        "CUST": "Custom...",
        "SCORES": "High Scores",
        "EXIT": "Exit",
        "SOUND": "Sound",
        "PARTICLES": "Particles",
        "QMARK": "Question Mark",
        "SAFE": "Safe Start",
        "NOGUESS": "No Guessing",
        "TUTORIAL": "Tutorial Mode",
        "THEME": "Theme",
        "SCALE": "Zoom",
        "ANALYSIS": "Analysis Helper",
        "ON": "ON",
        "OFF": "OFF",
        "MSG_READY": "System Ready.",
        "MSG_WIN": "Victory! Clear.",
        "MSG_BOOM": "Boom! Game Over.",
        "MSG_LUCK": "Pure luck move.",
        "MSG_ERR_FULL": "Error! Neighbors full.",
        "MSG_HARD": "Tricky position.",
        "TIT_CUST": "Custom Board",
        "TIT_SCORE": "NEW RECORD!",
        "LBL_W": "Width (9-50):",
        "LBL_H": "Height (9-30):",
        "LBL_M": "Mines:",
        "LBL_NAME": "Name:",
        "PAUSED": "PAUSED"
    },
    "TR": {
        "GAME_BTN": "OYUN",
        "NEW": "Yeni Oyun (F2)",
        "BEG": "Başlangıç",
        "INT": "Orta Seviye",
        "EXP": "Uzman",
        "CUST": "Özel...",
        "SCORES": "Skorlar",
        "EXIT": "Çıkış",
        "SOUND": "Sesler",
        "PARTICLES": "Efektler",
        "QMARK": "Soru İşareti",
        "SAFE": "Güvenli Başlangıç",
        "NOGUESS": "Şanssız Mod",
        "TUTORIAL": "Eğitim Modu",
        "THEME": "Tema",
        "SCALE": "Boyut",
        "ANALYSIS": "Analiz Asistanı",
        "ON": "AÇIK",
        "OFF": "KAPALI",
        "MSG_READY": "Sistem Hazır.",
        "MSG_WIN": "Zafer! Temiz iş.",
        "MSG_BOOM": "Güm! Oyun Bitti.",
        "MSG_LUCK": "%100 Şans hamlesiydi.",
        "MSG_ERR_FULL": "Hata! Çevresi dolu.",
        "MSG_HARD": "Zor pozisyon.",
        "TIT_CUST": "Özel Harita",
        "TIT_SCORE": "YENİ REKOR!",
        "LBL_W": "Genişlik (9-50):",
        "LBL_H": "Yükseklik (9-30):",
        "LBL_M": "Mayın:",
        "LBL_NAME": "İsim:",
        "PAUSED": "DURAKLATILDI"
    }
}

THEMES = {
    'CLASSIC': {
        'bg': (192, 192, 192), 'white': (255, 255, 255), 'gray_dark': (128, 128, 128),
        'black': (0, 0, 0), 'red': (255, 0, 0), 'yellow': (255, 255, 0), 'blue_h': (0, 0, 128),
        'overlay_safe': (0, 255, 0, 100), 'overlay_mine': (255, 0, 0, 100), 'overlay_risk': (255, 200, 0, 100)
    },
    'DARK': {
        'bg': (60, 60, 60), 'white': (100, 100, 100), 'gray_dark': (30, 30, 30),
        'black': (200, 200, 200), 'red': (255, 80, 80), 'yellow': (200, 200, 0), 'blue_h': (100, 149, 237),
        'overlay_safe': (0, 255, 0, 80), 'overlay_mine': (255, 0, 0, 80), 'overlay_risk': (255, 200, 0, 80)
    },
    'XP': {
        'bg': (236, 233, 216), 'white': (255, 255, 255), 'gray_dark': (172, 168, 153),
        'black': (0, 0, 0), 'red': (255, 0, 0), 'yellow': (255, 200, 0), 'blue_h': (49, 106, 197),
        'overlay_safe': (0, 255, 0, 100), 'overlay_mine': (255, 0, 0, 100), 'overlay_risk': (255, 165, 0, 100)
    },
    'MATRIX': {
        'bg': (0, 20, 0), 'white': (0, 255, 0), 'gray_dark': (0, 100, 0),
        'black': (0, 255, 0), 'red': (200, 0, 0), 'yellow': (200, 255, 200), 'blue_h': (0, 100, 0),
        'overlay_safe': (0, 255, 0, 100), 'overlay_mine': (255, 0, 0, 100), 'overlay_risk': (200, 200, 0, 100)
    },
    'HOTDOG': {
        'bg': (255, 0, 0), 'white': (255, 255, 0), 'gray_dark': (128, 0, 0),
        'black': (255, 255, 255), 'red': (0, 0, 0), 'yellow': (255, 255, 0), 'blue_h': (0, 0, 0),
        'overlay_safe': (255, 255, 255, 100), 'overlay_mine': (0, 0, 0, 100), 'overlay_risk': (255, 255, 0, 100)
    }
}

C = THEMES['CLASSIC']
C_NUMBERS = {1:(0,0,255), 2:(0,128,0), 3:(255,0,0), 4:(0,0,128), 5:(128,0,0), 6:(0,128,128), 7:(0,0,0), 8:(128,128,128)}

BASE_CELL_SIZE = 16
BORDER_W = 3
TOP_UI_H = 32
MENU_H = 24
FACE_SIZE = 24
ANALYSIS_WIDTH_BASE = 200

DIFFICULTY = {
    'BASLANGIC': {'w': 9, 'h': 9, 'mines': 10},
    'ORTA': {'w': 16, 'h': 16, 'mines': 40},
    'UZMAN': {'w': 30, 'h': 16, 'mines': 99}
}

# --- EFEKT SİSTEMİ ---
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -2)
        self.color = color
        self.life = 1.0
        self.gravity = 0.2

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 0.02
        return self.life > 0

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life * 255)
            s = pygame.Surface((3, 3), pygame.SRCALPHA)
            s.fill((*self.color[:3], alpha))
            surface.blit(s, (int(self.x), int(self.y)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.enabled = True

    def emit(self, x, y, color, count=10):
        if not self.enabled: return
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

# --- SES MOTORU ---
class SoundManager:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.sounds = {}
            self.generate_retro_sounds()
        except:
            self.enabled = False

    # RAM üzerinde kare dalga üretimi (Synthesizer)
    def generate_square_wave(self, freq, duration, volume=0.5):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        period = max(1, sample_rate // freq)
        for i in range(n_samples):
            value = 32000 if (i // (period // 2)) % 2 else -32000
            value = int(value * volume)
            buf += struct.pack('<h', value)
        return pygame.mixer.Sound(buffer=buf)

    def generate_noise(self, duration, volume=0.5):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            value = random.randint(-32000, 32000)
            value = int(value * volume)
            buf += struct.pack('<h', value)
        return pygame.mixer.Sound(buffer=buf)

    def generate_retro_sounds(self):
        if not self.enabled: return
        self.sounds['click'] = self.generate_square_wave(800, 0.05, 0.3)
        self.sounds['flag'] = self.generate_square_wave(400, 0.05, 0.3)
        self.sounds['qmark'] = self.generate_square_wave(600, 0.05, 0.2)
        self.sounds['win'] = self.generate_square_wave(1000, 0.1, 0.4)
        self.sounds['boom'] = self.generate_noise(0.4, 0.6)

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

# --- SKOR YÖNETİMİ ---
class ScoreManager:
    def __init__(self):
        self.file = "highscores.json"
        self.scores = self.load_scores()

    def load_scores(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    return json.load(f)
            except: pass
        return {k: [] for k in DIFFICULTY.keys()}

    def save_scores(self):
        with open(self.file, 'w') as f:
            json.dump(self.scores, f)

    def add_score(self, difficulty, name, time_val, stats=None):
        if difficulty not in DIFFICULTY: return
        if difficulty not in self.scores: self.scores[difficulty] = []
        entry = {'name': name, 'time': time_val}
        if stats: entry.update(stats)
        self.scores[difficulty].append(entry)
        self.scores[difficulty].sort(key=lambda x: x['time'])
        self.scores[difficulty] = self.scores[difficulty][:5]
        self.save_scores()

    def is_highscore(self, difficulty, time_val):
        if difficulty not in DIFFICULTY: return False
        scores = self.scores.get(difficulty, [])
        if len(scores) < 5: return True
        return time_val < scores[-1]['time']

# --- TEKRAR İZLEME (REPLAY) ---
class ReplayManager:
    def __init__(self):
        self.moves = []
        self.start_time = 0
        self.recording = False
        self.playing = False
        self.play_index = 0
        self.play_start_time = 0

    def start_recording(self):
        self.moves = []
        self.start_time = time.time()
        self.recording = True
        self.playing = False

    def log_move(self, move_type, x, y):
        if self.recording:
            dt = time.time() - self.start_time
            self.moves.append((dt, move_type, x, y))

    def start_playback(self):
        if not self.moves: return False
        self.recording = False
        self.playing = True
        self.play_index = 0
        self.play_start_time = time.time()
        return True

    def get_next_move(self):
        if not self.playing or self.play_index >= len(self.moves):
            return None
        current_dt = (time.time() - self.play_start_time) * 2.0
        move_dt = self.moves[self.play_index][0]
        if current_dt >= move_dt:
            move = self.moves[self.play_index]
            self.play_index += 1
            return move
        return None

# --- ARAYÜZ SINIFLARI ---
class RetroMenu:
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 14)
        self.height = MENU_H
        self.menus = {
            "GAME": [], # Dinamik dolacak
            "MENU": []  # Sabit menü
        }
        self.menu_order = ["GAME", "MENU"]
        self.active_menu = None 
        self.rects = {} 
        self.current_lang = "EN"

    def refresh_items(self, app):
        # Dil metinlerini al
        txt = LOCALES[self.current_lang]
        
        # Yardımcı fonksiyonlar
        def on_off(v): return txt["ON"] if v else txt["OFF"]
        
        # GAME Menüsü (Çevirili)
        self.menus["GAME"] = [
            (txt["NEW"], "NEW"),
            ("-", None),
            (txt["BEG"], "LVL_BASLANGIC"),
            (txt["INT"], "LVL_ORTA"),
            (txt["EXP"], "LVL_UZMAN"),
            (txt["CUST"], "LVL_CUSTOM"),
            ("-", None),
            (txt["SCORES"], "SHOW_SCORES"),
            (txt["EXIT"], "EXIT")
        ]
        
        # MENU (Sabit Başlık) - İçerik çevirili ama "Language" sabit
        self.menus["MENU"] = [
            (f"Language: {self.current_lang}", "TOGGLE_LANG"), # SABİT KALAN KISIM
            ("-", None),
            (f"{txt['SOUND']}: {on_off(app.sounds.enabled)}", "TOGGLE_SOUND"),
            (f"{txt['PARTICLES']}: {on_off(app.particles.enabled)}", "TOGGLE_PARTICLES"),
            (f"{txt['QMARK']}: {on_off(app.use_qmark)}", "TOGGLE_QMARK"),
            (f"{txt['SAFE']}: {on_off(app.safe_start)}", "TOGGLE_SAFE_START"),
            (f"{txt['NOGUESS']}: {on_off(app.no_guess)}", "TOGGLE_NO_GUESS"),
            (f"{txt['TUTORIAL']}: {on_off(app.tutorial_mode)}", "TOGGLE_TUTORIAL"),
            (f"{txt['THEME']}: {app.current_theme}", "CYCLE_THEME"),
            (f"{txt['SCALE']}: {app.scale_factor}x", "CYCLE_SCALE"),
            (f"{txt['ANALYSIS']}: {on_off(app.show_analysis)}", "TOGGLE_ANALYSIS")
        ]

    def draw_bar(self, surface, screen_w):
        pygame.draw.rect(surface, C['bg'], (0, 0, screen_w, self.height))
        pygame.draw.line(surface, C['white'], (0, self.height-1), (screen_w, self.height-1), 1)
        
        x_pos = 6
        for key in self.menu_order:
            # Menü başlığını seç: GAME ise çevir, MENU ise sabit
            label = LOCALES[self.current_lang]["GAME_BTN"] if key == "GAME" else "MENU"
            
            text = self.font.render(label, True, C['black'])
            w = text.get_width() + 12
            rect = pygame.Rect(x_pos, 2, w, self.height - 4)
            self.rects[key] = rect
            
            if self.active_menu == key:
                pygame.draw.rect(surface, C['gray_dark'], rect, 1)
                text_rect = text.get_rect(center=(x_pos + w//2 + 1, self.height//2 + 1))
            else:
                text_rect = text.get_rect(center=(x_pos + w//2, self.height//2))

            surface.blit(text, text_rect)
            x_pos += w + 5

    def draw_dropdown(self, surface):
        if not self.active_menu: return

        items = self.menus[self.active_menu]
        max_w = 0
        row_h = 22
        # Genişlik hesapla
        for label, _ in items:
            w = self.font.render(label, True, C['black']).get_width()
            max_w = max(max_w, w)
        max_w += 30
        
        drop_x = self.rects[self.active_menu].x
        drop_y = self.height
        drop_h = len(items) * row_h + 4
        
        # Arkaplan çizimi
        rect = (drop_x, drop_y, max_w, drop_h)
        pygame.draw.rect(surface, C['bg'], rect)
        pygame.draw.line(surface, C['white'], (drop_x, drop_y), (drop_x+max_w, drop_y), 1)
        pygame.draw.line(surface, C['white'], (drop_x, drop_y), (drop_x, drop_y+drop_h), 1)
        pygame.draw.line(surface, C['black'], (drop_x+max_w, drop_y), (drop_x+max_w, drop_y+drop_h), 1)
        pygame.draw.line(surface, C['black'], (drop_x, drop_y+drop_h), (drop_x+max_w, drop_y+drop_h), 1)

        mouse_pos = pygame.mouse.get_pos()
        current_y = drop_y + 2
        self.current_dropdown_rects = [] 

        for label, action in items:
            item_rect = pygame.Rect(drop_x + 2, current_y, max_w - 4, row_h)
            if label == "-":
                mid_y = current_y + row_h//2
                pygame.draw.line(surface, C['gray_dark'], (drop_x+5, mid_y), (drop_x+max_w-5, mid_y), 1)
                pygame.draw.line(surface, C['white'], (drop_x+5, mid_y+1), (drop_x+max_w-5, mid_y+1), 1)
                self.current_dropdown_rects.append((item_rect, None))
            else:
                is_hover = item_rect.collidepoint(mouse_pos)
                if is_hover:
                    pygame.draw.rect(surface, C['blue_h'], item_rect) 
                    text = self.font.render(label, True, C['white']) 
                else:
                    text = self.font.render(label, True, C['black'])
                surface.blit(text, (drop_x + 10, current_y + 2))
                self.current_dropdown_rects.append((item_rect, action))
            current_y += row_h

    def handle_click(self, pos):
        if self.active_menu:
            for rect, action in self.current_dropdown_rects:
                if rect.collidepoint(pos):
                    self.active_menu = None
                    return action
            self.active_menu = None
        
        for title, rect in self.rects.items():
            if rect.collidepoint(pos):
                self.active_menu = title
                return "MENU_OPENED"
        return None

class InputDialog:
    def __init__(self, title, prompts):
        self.title = title
        self.prompts = prompts
        self.values = [p[1] for p in prompts]
        self.active_idx = 0
        self.font = pygame.font.SysFont('arial', 14, bold=True)
        self.done = False
        self.cancelled = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.active_idx < len(self.prompts) - 1:
                    self.active_idx += 1
                else:
                    self.done = True
            elif event.key == pygame.K_TAB:
                 self.active_idx = (self.active_idx + 1) % len(self.prompts)
            elif event.key == pygame.K_ESCAPE:
                self.cancelled = True
                self.done = True
            elif event.key == pygame.K_BACKSPACE:
                self.values[self.active_idx] = self.values[self.active_idx][:-1]
            else:
                if len(self.values[self.active_idx]) < 10: 
                    self.values[self.active_idx] += event.unicode

    def draw(self, surface, center_x, center_y, gfx):
        w, h = 200, 40 + len(self.prompts) * 40 + 40
        x, y = center_x - w//2, center_y - h//2
        
        pygame.draw.rect(surface, C['bg'], (x, y, w, h))
        gfx.draw_bevel(surface, (x, y, w, h), pressed=False)
        pygame.draw.rect(surface, C['blue_h'], (x+3, y+3, w-6, 20))
        title_surf = self.font.render(self.title, True, C['white'])
        surface.blit(title_surf, (x+5, y+4))
        
        curr_y = y + 35
        for i, (label, _) in enumerate(self.prompts):
            lbl_surf = self.font.render(label, True, C['black'])
            surface.blit(lbl_surf, (x+10, curr_y))
            
            box_rect = (x+10, curr_y + 18, w-20, 20)
            gfx.draw_bevel(surface, box_rect, pressed=True)
            pygame.draw.rect(surface, C['white'], (box_rect[0]+2, box_rect[1]+2, box_rect[2]-4, box_rect[3]-4))
            
            val_surf = self.font.render(self.values[i], True, C['black'])
            surface.blit(val_surf, (x+14, curr_y + 20))
            
            if i == self.active_idx and int(time.time()*2) % 2 == 0:
                cw = val_surf.get_width()
                pygame.draw.line(surface, C['black'], (x+14+cw, curr_y+20), (x+14+cw, curr_y+36))
            
            curr_y += 45
            
        info = self.font.render("[ENTER]", True, C['gray_dark'])
        surface.blit(info, (x + w//2 - info.get_width()//2, y + h - 20))

class AnalysisPanel:
    def __init__(self):
        self.messages = [] 
        self.font = None 
        self.scroll_offset = 0
        self.current_lang = "EN"

    def add_message(self, text, color=None):
        if color is None: color = C['black']
        self.messages.append({"text": text, "color": color})

    def check_death_reason(self, logic, x, y):
        # Mesajlar dile göre dinamik çekilir
        txt = LOCALES[self.current_lang]
        neighbors = logic.get_neighbor_coords(x, y)
        revealed_neighbors = [n for n in neighbors if logic.grid_revealed[n[1]][n[0]]]
        
        if not revealed_neighbors:
            self.add_message(txt["MSG_LUCK"], C['red'])
            return

        for nx, ny in revealed_neighbors:
            val = logic.get_neighbors(nx, ny)
            n_neighbors = logic.get_neighbor_coords(nx, ny)
            flags = sum(1 for tx, ty in n_neighbors if logic.grid_flags[ty][tx] == 1)
            if flags == val:
                self.add_message(f"{txt['MSG_ERR_FULL']} ({nx},{ny})", C['red'])
                return
        self.add_message(txt["MSG_HARD"], C['black'])

    def draw(self, surface, x, y, w, h, gfx):
        pygame.draw.rect(surface, C['bg'], (x, y, w, h))
        gfx.draw_bevel(surface, (x, y, w, h), pressed=True, border_width=2)
        inner_rect = (x+2, y+2, w-4, h-4)
        pygame.draw.rect(surface, C['white'], inner_rect)
        
        font_h = gfx.font.get_height() + 4
        max_lines = (h - 10) // font_h
        wrapped_lines = []
        char_w = gfx.font.size("A")[0] 
        max_chars = (w - 15) // char_w
        
        for msg in self.messages:
            text = msg['text']
            color = msg['color']
            while len(text) > max_chars:
                split_idx = text[:max_chars].rfind(" ")
                if split_idx == -1: split_idx = max_chars
                wrapped_lines.append((text[:split_idx], color))
                text = text[split_idx:].strip()
            wrapped_lines.append((text, color))
        
        visible_start = max(0, len(wrapped_lines) - max_lines)
        cur_y = y + 6
        for i in range(visible_start, len(wrapped_lines)):
            line_text, color = wrapped_lines[i]
            render = gfx.font.render(line_text, True, color)
            surface.blit(render, (x + 6, cur_y))
            cur_y += font_h

class GraphicsEngine:
    def __init__(self):
        self.font = None
        self.digit_font = None

    def update_font(self, scale):
        size = int(12 * scale)
        self.font = pygame.font.SysFont('couriernew', size, bold=True) 
        self.digit_font = pygame.font.SysFont('couriernew', int(20 * scale), bold=True)

    def draw_bevel(self, surface, rect, pressed=False, border_width=2):
        x, y, w, h = rect
        pygame.draw.rect(surface, C['bg'], rect)
        if pressed:
            pygame.draw.line(surface, C['gray_dark'], (x, y), (x+w-1, y), border_width)
            pygame.draw.line(surface, C['gray_dark'], (x, y), (x, y+h-1), border_width)
            pygame.draw.line(surface, C['black'], (x+1, y+1), (x+w-2, y+1), 1)
            pygame.draw.line(surface, C['black'], (x+1, y+1), (x+1, y+h-2), 1)
        else:
            pygame.draw.line(surface, C['white'], (x, y), (x+w-2, y), border_width)
            pygame.draw.line(surface, C['white'], (x, y), (x, y+h-2), border_width)
            pygame.draw.line(surface, C['gray_dark'], (x+w-border_width, y), (x+w-border_width, y+h-1), border_width)
            pygame.draw.line(surface, C['gray_dark'], (x, y+h-border_width), (x+w-1, y+h-border_width), border_width)

    def draw_digit_panel(self, surface, x, y, value, scale):
        w, h = int(40 * scale), int(24 * scale)
        pygame.draw.rect(surface, C['black'], (x, y, w, h)) 
        val_str = f"{max(-99, min(999, value)):03}"
        text = self.digit_font.render(val_str, True, C['red'])
        text_rect = text.get_rect(center=(x + w//2, y + h//2))
        surface.blit(text, text_rect)

    def draw_face(self, surface, rect, state, scale):
        self.draw_bevel(surface, rect, pressed=(state == 'ooh_click'), border_width=int(2*scale))
        cx, cy = rect.centerx, rect.centery
        r = int(8 * scale)
        pygame.draw.circle(surface, C['yellow'], (cx, cy), r)
        pygame.draw.circle(surface, C['black'], (cx, cy), r, 1)
        off = int(3 * scale)
        eye_r = int(1.5 * scale) if scale > 1 else 1
        if state == 'smile' or state == 'ooh_click':
            pygame.draw.circle(surface, C['black'], (cx-off, cy-2), eye_r)
            pygame.draw.circle(surface, C['black'], (cx+off, cy-2), eye_r)
            pygame.draw.arc(surface, C['black'], (cx-off-2, cy-off-2, off*2+4, off*2+4), 3.14, 6.28, 1)
        elif state == 'ooh':
            pygame.draw.circle(surface, C['black'], (cx-off, cy-2), eye_r)
            pygame.draw.circle(surface, C['black'], (cx+off, cy-2), eye_r)
            pygame.draw.circle(surface, C['black'], (cx, cy+off), int(2*scale), 1)
        elif state == 'dead':
            l = int(3 * scale)
            pygame.draw.line(surface, C['black'], (cx-off-l, cy-l-2), (cx-off+l, cy+l-2), 1)
            pygame.draw.line(surface, C['black'], (cx-off+l, cy-l-2), (cx-off-l, cy+l-2), 1)
            pygame.draw.line(surface, C['black'], (cx+off-l, cy-l-2), (cx+off+l, cy+l-2), 1)
            pygame.draw.line(surface, C['black'], (cx+off+l, cy-l-2), (cx+off-l, cy+l-2), 1)
            pygame.draw.arc(surface, C['black'], (cx-off-2, cy+1, off*2+4, off*2+4), 0, 3.14, 1)
        elif state == 'win':
             pygame.draw.line(surface, C['black'], (cx-off-2, cy-2), (cx+off+2, cy-2), int(2*scale))
             pygame.draw.arc(surface, C['black'], (cx-off-2, cy-off-2, off*2+4, off*2+4), 3.14, 6.28, 1)

    def draw_mine(self, surface, rect, bg_color=None):
        if bg_color is None: bg_color = C['bg']
        pygame.draw.rect(surface, bg_color, rect)
        cx, cy = rect.centerx, rect.centery
        r = rect.width // 4
        pygame.draw.circle(surface, C['black'], (cx, cy), r)
        l = rect.width // 2 - 2
        pygame.draw.line(surface, C['black'], (cx, cy-l), (cx, cy+l), 2)
        pygame.draw.line(surface, C['black'], (cx-l, cy), (cx+l, cy), 2)
        pygame.draw.line(surface, C['black'], (cx-l+2, cy-l+2), (cx+l-2, cy+l-2), 2)
        pygame.draw.line(surface, C['black'], (cx-l+2, cy+l-2), (cx+l-2, cy-l+2), 2)
        pygame.draw.rect(surface, C['white'], (cx-r//2, cy-r//2, 2, 2))

    def draw_flag(self, surface, rect):
        cx, cy = rect.centerx, rect.centery
        scale = rect.width / 16
        pygame.draw.line(surface, C['black'], (cx-2*scale, cy+5*scale), (cx+4*scale, cy+5*scale), 2) 
        pygame.draw.line(surface, C['black'], (cx, cy-4*scale), (cx, cy+5*scale), 2)
        points = [(cx, cy-4*scale), (cx-6*scale, cy-1*scale), (cx, cy+2*scale)]
        pygame.draw.polygon(surface, C['red'], points)

    def draw_qmark(self, surface, rect):
        cx, cy = rect.centerx, rect.centery
        scale = rect.width / 16
        font = pygame.font.SysFont('arial', int(12*scale), bold=True)
        txt = font.render("?", True, C['black'])
        surface.blit(txt, txt.get_rect(center=rect.center))

class GameLogic:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mine_count = mines
        self.safe_start_enabled = False 
        self.no_guess_mode = False
        self.reset()
        
        self.clicks = 0
        self.stat_3bv = 0 

    def reset(self):
        self.grid_mines = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.grid_revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.grid_flags = [[0 for _ in range(self.width)] for _ in range(self.height)] 
        self.first_click = True
        self.game_over = False
        self.won = False
        self.start_time = None
        self.end_time = None
        self.mines_left = self.mine_count
        self.exploded_mine = None
        self.clicks = 0
        self.stat_3bv = 0

    def calculate_3bv(self):
        # 3BV: Minimum tıklama sayısı metriği (Basitleştirilmiş)
        visited = set()
        tbv = 0
        
        # Boşluklar (Openings)
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid_mines[y][x] and self.get_neighbors(x, y) == 0 and (x, y) not in visited:
                    tbv += 1
                    stack = [(x, y)]
                    while stack:
                        cx, cy = stack.pop()
                        if (cx, cy) in visited: continue
                        visited.add((cx, cy))
                        for nx, ny in self.get_neighbor_coords(cx, cy):
                            if not self.grid_mines[ny][nx]:
                                if self.get_neighbors(nx, ny) == 0:
                                    stack.append((nx, ny))
                                else:
                                    visited.add((nx, ny)) 
        
        # Diğer sayılar
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid_mines[y][x] and (x, y) not in visited:
                    tbv += 1
        
        self.stat_3bv = tbv

    def place_mines(self, safe_x, safe_y):
        # Mayın yerleştirme (Şanssız modda tekrar dener)
        max_retries = 20 if self.no_guess_mode else 1
        
        for _ in range(max_retries):
            self.grid_mines = [[False for _ in range(self.width)] for _ in range(self.height)]
            
            safe_zone = []
            if self.safe_start_enabled:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        safe_zone.append((safe_x + dx, safe_y + dy))
            else:
                safe_zone.append((safe_x, safe_y))

            placed = 0
            max_mines = (self.width * self.height) - len(safe_zone)
            target_mines = min(self.mine_count, max_mines)
            
            while placed < target_mines:
                rx = random.randint(0, self.width - 1)
                ry = random.randint(0, self.height - 1)
                
                if (rx, ry) not in safe_zone and not self.grid_mines[ry][rx]:
                    self.grid_mines[ry][rx] = True
                    placed += 1
            
            self.calculate_3bv()
            break 

        self.start_time = time.time()

    def get_neighbor_coords(self, x, y):
        coords = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    coords.append((nx, ny))
        return coords

    def get_neighbors(self, x, y):
        count = 0
        for nx, ny in self.get_neighbor_coords(x, y):
            if self.grid_mines[ny][nx]:
                count += 1
        return count
    
    def get_tutorial_overlay(self):
        # Gelişmiş Kör Analiz: Sadece görünen sayılarla mantık yürütür
        overlay = [[0 for _ in range(self.width)] for _ in range(self.height)]
        changed = True
        
        while changed:
            changed = False
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid_revealed[y][x]:
                        val = self.get_neighbors(x, y)
                        if val > 0:
                            neighbors = self.get_neighbor_coords(x, y)
                            known_mines = []
                            known_safe = []
                            unknowns = []
                            
                            for nx, ny in neighbors:
                                if self.grid_revealed[ny][nx]: known_safe.append((nx, ny))
                                elif self.grid_flags[ny][nx] == 1: known_mines.append((nx, ny))
                                elif overlay[ny][nx] == 2: known_mines.append((nx, ny))
                                elif overlay[ny][nx] == 1: known_safe.append((nx, ny))
                                else: unknowns.append((nx, ny))
                            
                            remaining_mines_needed = val - len(known_mines)
                            
                            if remaining_mines_needed == len(unknowns) and len(unknowns) > 0:
                                for ux, uy in unknowns:
                                    if overlay[uy][ux] != 2:
                                        overlay[uy][ux] = 2 # Kırmızı (Kesin Mayın)
                                        changed = True
                            
                            elif remaining_mines_needed == 0 and len(unknowns) > 0:
                                for ux, uy in unknowns:
                                    if overlay[uy][ux] != 1:
                                        overlay[uy][ux] = 1 # Yeşil (Kesin Güvenli)
                                        changed = True

        # Sarı (Riskli) bölgeleri işaretle
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid_revealed[y][x] and self.grid_flags[y][x] != 1 and overlay[y][x] == 0:
                    neighbors = self.get_neighbor_coords(x, y)
                    if any(self.grid_revealed[ny][nx] for nx, ny in neighbors):
                        overlay[y][x] = 3 
                            
        return overlay

    def get_auto_move(self):
        overlay = self.get_tutorial_overlay()
        for y in range(self.height):
            for x in range(self.width):
                if overlay[y][x] == 1 and not self.grid_revealed[y][x]: 
                    return (x, y)
        return None

    def reveal(self, x, y):
        # Stack tabanlı açma (Recursion hatasını önler)
        if not (0 <= x < self.width and 0 <= y < self.height): return False
        if self.grid_revealed[y][x] or self.grid_flags[y][x] == 1 or self.game_over: return False

        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False
        
        self.clicks += 1
        stack = [(x, y)]
        hit_mine_result = False

        while stack:
            cx, cy = stack.pop()
            
            if not (0 <= cx < self.width and 0 <= cy < self.height): continue
            if self.grid_revealed[cy][cx]: continue
            if self.grid_flags[cy][cx] == 1: continue

            self.grid_revealed[cy][cx] = True
            
            if self.grid_mines[cy][cx]:
                self.game_over = True
                self.exploded_mine = (cx, cy)
                self.end_time = time.time()
                hit_mine_result = True
                break
            
            if self.get_neighbors(cx, cy) == 0:
                for nx, ny in self.get_neighbor_coords(cx, cy):
                    if not self.grid_revealed[ny][nx] and self.grid_flags[ny][nx] != 1:
                        stack.append((nx, ny))
        
        if not hit_mine_result:
            self.check_win()
        
        return hit_mine_result

    def toggle_flag(self, x, y, use_qmark=False):
        if self.game_over or self.grid_revealed[y][x]: return None
        current = self.grid_flags[y][x]
        if current == 0:
            self.grid_flags[y][x] = 1
            self.mines_left -= 1
            return 'flag'
        elif current == 1:
            self.grid_flags[y][x] = 2 if use_qmark else 0
            self.mines_left += 1
            return 'qmark' if use_qmark else 'empty'
        elif current == 2:
            self.grid_flags[y][x] = 0
            return 'empty'

    def check_win(self):
        revealed_count = sum(row.count(True) for row in self.grid_revealed)
        safe_cells = (self.width * self.height) - self.mine_count
        if revealed_count == safe_cells:
            self.won = True
            self.game_over = True
            self.end_time = time.time()
            self.mines_left = 0
            for y in range(self.height):
                for x in range(self.width):
                    if self.grid_mines[y][x]:
                        self.grid_flags[y][x] = 1
    
    def get_time(self):
        if self.first_click: return 0
        if self.game_over: return int(self.end_time - self.start_time) if self.start_time else 0
        return int(time.time() - self.start_time)

class MinesweeperApp:
    def __init__(self):
        pygame.init()
        self.sounds = SoundManager()
        self.scores = ScoreManager()
        self.replay = ReplayManager()
        self.particles = ParticleSystem()
        self.gfx = GraphicsEngine()
        self.menu = RetroMenu()
        self.analysis = AnalysisPanel()
        self.clock = pygame.time.Clock()
        
        # Varsayılan Ayarlar
        self.scale_factor = 1.5
        self.current_difficulty = 'BASLANGIC'
        self.show_analysis = False
        self.safe_start = False
        self.use_qmark = False
        self.no_guess = False
        self.current_theme = 'CLASSIC'
        self.paused = False
        self.tutorial_mode = False
        self.last_interaction_time = time.time()
        self.modal = None
        self.key_history = []
        self.cheat_end_time = 0
        
        self.apply_settings()
        
    def apply_settings(self):
        global C
        C = THEMES[self.current_theme]
        
        # Analysis panel dilini güncelle
        self.analysis.current_lang = self.menu.current_lang

        if self.current_difficulty == 'CUSTOM' and hasattr(self, 'logic'):
            pass
        else:
            conf = DIFFICULTY.get(self.current_difficulty, DIFFICULTY['BASLANGIC'])
            self.logic = GameLogic(conf['w'], conf['h'], conf['mines'])
        
        self.logic.safe_start_enabled = self.safe_start
        self.logic.no_guess_mode = self.no_guess
        
        self.cell_size = int(BASE_CELL_SIZE * self.scale_factor)
        self.gfx.update_font(self.scale_factor)

        self.board_w = self.logic.width * self.cell_size
        self.board_h = self.logic.height * self.cell_size
        
        self.analysis_w = int(ANALYSIS_WIDTH_BASE * self.scale_factor) if self.show_analysis else 0
        
        self.game_window_w = self.board_w + int(20 * self.scale_factor)
        self.window_w = self.game_window_w + self.analysis_w + (10 if self.show_analysis else 0)
        
        self.top_ui_h = int(TOP_UI_H * self.scale_factor)
        self.border_w = int(BORDER_W * self.scale_factor)
        
        self.window_h = MENU_H + self.top_ui_h + self.board_h + int(30 * self.scale_factor)
        
        self.screen = pygame.display.set_mode((self.window_w, self.window_h))
        
        # Başlık güncelle (Duruma göre)
        title = "Minesweeper" if self.menu.current_lang == "EN" else "Mayın Tarlası"
        if self.replay.playing: title += " [REPLAY]" if self.menu.current_lang == "EN" else " [TEKRAR]"
        if self.paused: title += f" [{LOCALES[self.menu.current_lang]['PAUSED']}]"
        pygame.display.set_caption(title)
        
        cx = self.game_window_w // 2
        face_s = int(FACE_SIZE * self.scale_factor)
        self.rect_face = pygame.Rect(cx - face_s//2, MENU_H + int(4*self.scale_factor), face_s, face_s)
        self.rect_replay = pygame.Rect(cx + face_s + 10, MENU_H + int(4*self.scale_factor), face_s, face_s)
        
        self.offset_x = int(10 * self.scale_factor)
        self.offset_y = MENU_H + self.top_ui_h + int(12 * self.scale_factor)
        
        self.analysis_rect = pygame.Rect(self.game_window_w + 5, MENU_H + 5, self.analysis_w - 10, self.window_h - MENU_H - 10)

        self.is_pressing = False
        self.pressed_cell = None
        self.face_state = 'smile'
        
        self.menu.refresh_items(self)

    def handle_menu_action(self, action):
        txt = LOCALES[self.menu.current_lang]
        
        if action == "NEW":
            self.replay.start_recording()
            self.logic.reset()
            self.particles.particles = []
            self.apply_settings()
        elif action == "EXIT":
            pygame.quit(); sys.exit()
        elif action.startswith("LVL_"):
            diff = action.split("_")[1]
            if diff == "CUSTOM":
                self.modal = InputDialog(txt["TIT_CUST"], [(txt["LBL_W"], "20"), (txt["LBL_H"], "20"), (txt["LBL_M"], "50")])
            else:
                self.current_difficulty = diff
                self.replay.start_recording()
                self.logic.reset()
                self.particles.particles = []
                self.apply_settings()
        elif action == "TOGGLE_SOUND":
            self.sounds.enabled = not self.sounds.enabled
            self.sounds.generate_retro_sounds()
            self.apply_settings()
        elif action == "TOGGLE_PARTICLES":
            self.particles.enabled = not self.particles.enabled
            self.apply_settings()
        elif action == "TOGGLE_SAFE_START":
            self.safe_start = not self.safe_start
            self.apply_settings()
        elif action == "TOGGLE_NO_GUESS":
            self.no_guess = not self.no_guess
            self.apply_settings()
        elif action == "TOGGLE_ANALYSIS":
            self.show_analysis = not self.show_analysis
            self.apply_settings()
        elif action == "CYCLE_SCALE":
            self.scale_factor = 2.0 if self.scale_factor == 1.5 else (1.5 if self.scale_factor == 1.0 else 1.0)
            self.apply_settings()
        elif action == "SHOW_SCORES":
            self.show_scores_modal()
        elif action == "TOGGLE_QMARK":
            self.use_qmark = not self.use_qmark
            self.apply_settings()
        elif action == "CYCLE_THEME":
            themes = list(THEMES.keys())
            idx = themes.index(self.current_theme)
            self.current_theme = themes[(idx + 1) % len(themes)]
            self.apply_settings()
        elif action == "TOGGLE_TUTORIAL":
            self.tutorial_mode = not self.tutorial_mode
            self.apply_settings()
        elif action == "TOGGLE_LANG":
            self.menu.current_lang = "TR" if self.menu.current_lang == "EN" else "EN"
            self.analysis.current_lang = self.menu.current_lang
            if self.show_analysis:
                self.analysis.add_message(LOCALES[self.menu.current_lang]["MSG_READY"])
            self.apply_settings()

    def show_scores_modal(self):
        if not self.show_analysis:
            self.show_analysis = True
            self.apply_settings()
        
        txt = LOCALES[self.menu.current_lang]
        self.analysis.add_message(f"--- {txt['SCORES']} ---", C['blue_h'])
        scores = self.scores.scores
        for diff in ['BASLANGIC', 'ORTA', 'UZMAN']:
            d_name = txt["BEG"] if diff=="BASLANGIC" else (txt["INT"] if diff=="ORTA" else txt["EXP"])
            self.analysis.add_message(f"[{d_name}]", C['gray_dark'])
            for s in scores.get(diff, []):
                line = f"{s['time']}s - {s['name']}"
                if '3bv' in s: line += f" (3BV:{s['3bv']})"
                self.analysis.add_message(line, C['black'])

    def handle_game_over(self):
        if self.replay.playing: return 
        txt = LOCALES[self.menu.current_lang]
        
        if self.logic.won:
            self.sounds.play('win')
            if self.particles.enabled:
                for _ in range(20):
                    rx = random.randint(0, self.window_w)
                    ry = random.randint(0, self.window_h)
                    self.particles.emit(rx, ry, C['blue_h'], 5)
                    
            if self.scores.is_highscore(self.current_difficulty, self.logic.get_time()):
                eff = 0
                if self.logic.clicks > 0:
                    eff = round(self.logic.stat_3bv / self.logic.clicks * 100)
                
                stats = {'clicks': self.logic.clicks, '3bv': self.logic.stat_3bv, 'eff': f"{eff}%"}
                self.modal = InputDialog(txt["TIT_SCORE"], [(txt["LBL_NAME"], "Player")])
                self.modal.extra_data = stats 
            
            if self.show_analysis: self.analysis.add_message(txt["MSG_WIN"], C['blue_h'])
        else:
            self.sounds.play('boom')
            if self.particles.enabled and self.logic.exploded_mine:
                ex, ey = self.logic.exploded_mine
                px = self.offset_x + ex * self.cell_size + self.cell_size//2
                py = self.offset_y + ey * self.cell_size + self.cell_size//2
                self.particles.emit(px, py, C['red'], 50)
                self.particles.emit(px, py, C['black'], 30)
            
            if self.show_analysis: self.analysis.add_message(txt["MSG_BOOM"], C['red'])

    def reset_timer(self):
        self.last_interaction_time = time.time()

    def handle_input(self):
        events = pygame.event.get()
        if any(e.type == pygame.MOUSEMOTION for e in events): self.reset_timer()

        # Modal Kontrolü
        if self.modal:
            for event in events:
                if event.type == pygame.QUIT: return False
                self.modal.handle_event(event)
            
            if self.modal.done:
                if not self.modal.cancelled:
                    txt = LOCALES[self.menu.current_lang]
                    if self.modal.title == txt["TIT_CUST"]:
                        try:
                            w = max(9, min(50, int(self.modal.values[0])))
                            h = max(9, min(30, int(self.modal.values[1])))
                            m = max(1, min(w*h-9, int(self.modal.values[2])))
                            self.logic = GameLogic(w, h, m)
                            self.current_difficulty = 'CUSTOM'
                            self.replay.start_recording()
                            self.particles.particles = []
                            self.apply_settings()
                        except: pass
                    elif self.modal.title == txt["TIT_SCORE"]:
                        name = self.modal.values[0]
                        stats = getattr(self.modal, 'extra_data', None)
                        self.scores.add_score(self.current_difficulty, name, self.logic.get_time(), stats)
                        self.show_scores_modal()
                self.modal = None
            return True

        # Replay Oynatma
        if self.replay.playing:
            move = self.replay.get_next_move()
            if move:
                _, mtype, mx, my = move
                if mtype == 'L': self.logic.reveal(mx, my)
                elif mtype == 'R': self.logic.toggle_flag(mx, my, self.use_qmark)
            
            for event in events: 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.replay.playing = False
                    self.replay.start_recording()
                    self.logic.reset()
                    self.particles.particles = []
                    self.apply_settings()
            return True

        # Oyun İçi Input
        for event in events:
            if event.type == pygame.QUIT: return False
            if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]: self.reset_timer()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    self.replay.start_recording()
                    self.logic.reset()
                    self.particles.particles = []
                    if self.show_analysis: 
                        self.analysis.add_message(LOCALES[self.menu.current_lang]["MSG_READY"])
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                    self.apply_settings() # Başlığı güncelle
                elif event.key == pygame.K_SPACE: # OTOPİLOT
                    if not self.logic.game_over and not self.paused:
                        move = self.logic.get_auto_move()
                        if move:
                            mx, my = move
                            self.logic.reveal(mx, my)
                            self.sounds.play('click')
                            self.replay.log_move('L', mx, my)
                            if self.logic.won: self.handle_game_over()

                # Hile
                self.key_history.append(event.key)
                if len(self.key_history) > 10: self.key_history.pop(0)
                if self.key_history[-5:] == [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
                    self.cheat_end_time = time.time() + 2.0
                    self.key_history = []

            if self.paused: continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                menu_action = self.menu.handle_click(mpos)
                if menu_action == "MENU_OPENED": continue
                if menu_action: self.handle_menu_action(menu_action); continue

                if event.button == 1:
                    if self.rect_face.collidepoint(mpos):
                        self.face_state = 'ooh_click'
                    elif self.logic.game_over and self.rect_replay.collidepoint(mpos):
                        if self.replay.start_playback():
                            self.logic.reset() 
                            self.apply_settings() # Başlığı güncelle
                    elif not self.logic.game_over:
                        cell = self.get_cell_at_pos(mpos)
                        if cell:
                            self.is_pressing = True
                            self.pressed_cell = cell
                            self.face_state = 'ooh'

                elif event.button == 3:
                    if not self.logic.game_over:
                        cell = self.get_cell_at_pos(mpos)
                        if cell:
                            action = self.logic.toggle_flag(cell[0], cell[1], self.use_qmark)
                            if action == 'flag': self.sounds.play('flag')
                            elif action == 'qmark': self.sounds.play('qmark')
                            self.replay.log_move('R', cell[0], cell[1])

            elif event.type == pygame.MOUSEBUTTONUP:
                mpos = pygame.mouse.get_pos()
                if event.button == 1:
                    if self.rect_face.collidepoint(mpos):
                        self.replay.start_recording()
                        self.logic.reset()
                        self.particles.particles = []
                        self.face_state = 'smile'
                    elif not self.logic.game_over and self.is_pressing:
                        cell = self.get_cell_at_pos(mpos)
                        if cell == self.pressed_cell:
                            hit = self.logic.reveal(cell[0], cell[1])
                            self.sounds.play('click')
                            self.replay.log_move('L', cell[0], cell[1])
                            
                            if hit: 
                                self.handle_game_over()
                                if self.show_analysis: self.analysis.check_death_reason(self.logic, cell[0], cell[1])
                            elif self.logic.won:
                                self.handle_game_over()
                    
                    self.is_pressing = False
                    self.pressed_cell = None
                    if not self.logic.game_over: self.face_state = 'smile'
        return True

    def get_cell_at_pos(self, pos):
        x, y = pos
        x -= self.offset_x
        y -= self.offset_y
        if 0 <= x < self.board_w and 0 <= y < self.board_h:
            return x // self.cell_size, y // self.cell_size
        return None

    def render(self):
        self.screen.fill(C['bg'])
        self.menu.draw_bar(self.screen, self.window_w)

        panel_y = MENU_H + int(4*self.scale_factor)
        pygame.draw.line(self.screen, C['gray_dark'], (0, panel_y-2), (self.game_window_w, panel_y-2), 2)
        pygame.draw.line(self.screen, C['white'], (0, panel_y + self.top_ui_h), (self.game_window_w, panel_y + self.top_ui_h), 2)

        counter_y = panel_y + int(4*self.scale_factor)
        self.gfx.draw_digit_panel(self.screen, self.offset_x, counter_y, self.logic.mines_left, self.scale_factor)
        self.gfx.draw_digit_panel(self.screen, self.game_window_w - self.offset_x - int(40*self.scale_factor), counter_y, self.logic.get_time(), self.scale_factor)
        
        mood = ('win' if self.logic.won else 'dead') if self.logic.game_over else self.face_state
        self.gfx.draw_face(self.screen, self.rect_face, mood, self.scale_factor)
        
        if self.logic.game_over and not self.replay.playing:
            self.gfx.draw_bevel(self.screen, self.rect_replay, pressed=False)
            font = pygame.font.SysFont('arial', int(12*self.scale_factor), bold=True)
            txt = font.render("R", True, C['blue_h'])
            self.screen.blit(txt, txt.get_rect(center=self.rect_replay.center))

        bx, by = self.offset_x, self.offset_y
        bw, bh = self.board_w, self.board_h
        border = self.border_w
        self.gfx.draw_bevel(self.screen, (bx-border, by-border, bw+border*2, bh+border*2), pressed=True, border_width=border)

        if self.paused:
            pygame.draw.rect(self.screen, C['black'], (bx, by, bw, bh))
            font = pygame.font.SysFont('arial', int(20*self.scale_factor), bold=True)
            txt_p = LOCALES[self.menu.current_lang]["PAUSED"]
            txt = font.render(txt_p, True, C['white'])
            self.screen.blit(txt, txt.get_rect(center=(bx + bw//2, by + bh//2)))
        else:
            is_cheat = time.time() < self.cheat_end_time
            
            show_tutorial = False
            tutorial_overlay = None
            if self.tutorial_mode and self.current_difficulty == 'BASLANGIC' and not self.logic.game_over and not self.replay.playing:
                if time.time() - self.last_interaction_time > 5.0:
                    show_tutorial = True
                    tutorial_overlay = self.logic.get_tutorial_overlay()

            for y in range(self.logic.height):
                for x in range(self.logic.width):
                    px = bx + x * self.cell_size
                    py = by + y * self.cell_size
                    rect = pygame.Rect(px, py, self.cell_size, self.cell_size)
                    
                    revealed = self.logic.grid_revealed[y][x]
                    flag_status = self.logic.grid_flags[y][x]
                    pressed = (self.pressed_cell == (x, y)) and (flag_status == 0)
                    
                    if revealed:
                        pygame.draw.rect(self.screen, C['gray_dark'], rect, 1)
                        if self.logic.grid_mines[y][x]:
                            bg = C['red'] if self.logic.exploded_mine == (x, y) else C['bg']
                            self.gfx.draw_mine(self.screen, rect, bg)
                        else:
                            neighbors = self.logic.get_neighbors(x, y)
                            if neighbors > 0:
                                color = C_NUMBERS.get(neighbors, C['black'])
                                text = self.gfx.font.render(str(neighbors), True, color)
                                self.screen.blit(text, text.get_rect(center=rect.center))
                    else:
                        if pressed:
                            pygame.draw.rect(self.screen, C['bg'], rect)
                            pygame.draw.rect(self.screen, C['gray_dark'], rect, 1)
                        else:
                            self.gfx.draw_bevel(self.screen, rect, pressed=False, border_width=int(2*self.scale_factor))
                            if flag_status == 1:
                                self.gfx.draw_flag(self.screen, rect)
                            elif flag_status == 2:
                                self.gfx.draw_qmark(self.screen, rect)
                            elif self.logic.game_over and not self.logic.won and self.logic.grid_mines[y][x]:
                                self.gfx.draw_mine(self.screen, rect)
                            
                            if self.logic.game_over and not self.logic.won and flag_status == 1 and not self.logic.grid_mines[y][x]:
                                 pygame.draw.line(self.screen, C['black'], rect.topleft, rect.bottomright, 2)
                                 pygame.draw.line(self.screen, C['black'], rect.topright, rect.bottomleft, 2)
                        
                        if is_cheat and self.logic.grid_mines[y][x]:
                            glow = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                            glow.fill((255, 0, 0, 100))
                            self.screen.blit(glow, (px, py))
                            
                        if show_tutorial and tutorial_overlay and flag_status != 1:
                            val = tutorial_overlay[y][x]
                            color = None
                            if val == 1: color = C['overlay_safe']
                            elif val == 2: color = C['overlay_mine']
                            elif val == 3: color = C['overlay_risk']
                            
                            if color:
                                tut_surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                                tut_surf.fill(color)
                                self.screen.blit(tut_surf, (px, py))

        if self.particles.enabled:
            self.particles.update()
            self.particles.draw(self.screen)

        if self.show_analysis:
            self.analysis.draw(self.screen, self.analysis_rect.x, self.analysis_rect.y, self.analysis_rect.w, self.analysis_rect.h, self.gfx)

        if self.modal:
            self.modal.draw(self.screen, self.window_w//2, self.window_h//2, self.gfx)

        self.menu.draw_dropdown(self.screen)
        pygame.display.flip()

    def run(self):
        self.replay.start_recording()
        while True:
            if not self.handle_input(): break
            self.render()
            self.clock.tick(60)
        pygame.quit(); sys.exit()

if __name__ == "__main__":
    app = MinesweeperApp()
    app.run()
