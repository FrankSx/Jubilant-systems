#!/usr/bin/env python3
"""
Adversarial ML Content Generator
Generates synthetic user data with adversarial perturbations for testing.

🦀 13th Hour Testing Suite 🦀
"""

import random
import string
import unicodedata
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import hashlib
import json


class AttackType(Enum):
    """Types of adversarial attacks supported."""
    HOMOGLYPH = "homoglyph"
    INVISIBLE = "invisible"
    ZWJ = "zwj"
    RTL = "rtl"
    CASE = "case"
    LEET = "leet"
    GLITCH = "glitch"
    NORMALIZE = "normalize"
    PUNYCODE = "punycode"
    EMOJI = "emoji"


@dataclass
class UserProfile:
    """Synthetic user profile with adversarial capabilities."""
    username: str
    first_name: str
    last_name: str
    address: str
    description: str
    profile_pic_prompt: str
    attack_vectors: List[AttackType]
    raw_bytes: bytes

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "description": self.description,
            "profile_pic_prompt": self.profile_pic_prompt,
            "attack_vectors": [a.value for a in self.attack_vectors],
            "byte_hash": hashlib.sha256(self.raw_bytes).hexdigest()[:16]
        }


class AdversarialStringGenerator:
    """Generate strings with adversarial perturbations."""

    # Homoglyph mappings
    HOMOGLYPHS = {
        'a': ['а', 'а', 'ɑ', 'α', 'ａ', 'â', 'ä'],
        'b': ['Ь', 'β', 'ᖯ', 'ｂ'],
        'c': ['с', 'с', 'ᴄ', 'ⅽ', 'ｃ', 'ç'],
        'd': ['ԁ', 'ⅾ', 'ｄ', 'ð'],
        'e': ['е', 'е', 'ɛ', 'ε', 'ｅ', 'ê', 'ë', 'é'],
        'f': ['ғ', 'ｆ', 'ſ'],
        'g': ['ɡ', 'ɢ', 'ｇ', 'ց'],
        'h': ['һ', 'ʜ', 'ｈ'],
        'i': ['і', 'і', 'ɪ', 'ⅰ', 'ｉ', 'í', 'ï'],
        'j': ['ј', 'ｊ', 'ʝ'],
        'k': ['κ', 'ｋ', 'к'],
        'l': ['ⅼ', 'ｌ', 'ӏ', 'ł'],
        'm': ['ｍ', 'ɱ', 'м'],
        'n': ['ո', 'ｎ', 'η', 'ñ'],
        'o': ['о', 'о', 'ο', 'σ', 'ｏ', 'ô', 'ö', 'ó'],
        'p': ['р', 'р', 'ρ', 'ｐ'],
        'q': ['ｑ', 'զ'],
        'r': ['ｒ', 'ʀ', 'г'],
        's': ['ѕ', 'ѕ', 'ꜱ', 'ｓ', 'š'],
        't': ['ｔ', 'τ', 'т'],
        'u': ['υ', 'μ', 'ｕ', 'ü', 'ú', 'û'],
        'v': ['ｖ', 'ν', 'ѵ'],
        'w': ['ｗ', 'ω', 'ѡ'],
        'x': ['х', 'х', 'χ', 'ｘ'],
        'y': ['у', 'у', 'ｙ', 'ý', 'ÿ', 'ü'],
        'z': ['ｚ', 'ᴢ', 'ž'],
    }

    # Invisible characters
    ZWS = '\u200b'      # Zero width space
    ZWNJ = '\u200c'     # Zero width non-joiner
    ZWJ = '\u200d'      # Zero width joiner
    RTL = '\u202e'      # Right-to-left override
    POP = '\u202c'      # Pop directional formatting

    # Leet speak
    LEET_MAP = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0',
        's': '5', 't': '7', 'l': '1', 'g': '9',
        'b': '8', 'z': '2'
    }

    def __init__(self, seed: Optional[int] = None):
        """Initialize generator with optional seed."""
        if seed:
            random.seed(seed)

    def homoglyph_attack(self, text: str, probability: float = 0.3) -> str:
        """Replace characters with visually similar unicode."""
        result = []
        for char in text:
            lower_char = char.lower()
            if lower_char in self.HOMOGLYPHS and random.random() < probability:
                replacement = random.choice(self.HOMOGLYPHS[lower_char])
                # Preserve case if possible
                if char.isupper() and replacement.islower():
                    replacement = replacement.upper() if replacement.upper() != replacement else replacement
                result.append(replacement)
            else:
                result.append(char)
        return ''.join(result)

    def invisible_attack(self, text: str, count: int = 3, position: str = 'random') -> str:
        """Insert zero-width characters."""
        chars = list(text)
        invisibles = [self.ZWS, self.ZWNJ, self.ZWJ] * (count // 3 + 1)
        invisibles = invisibles[:count]

        for inv in invisibles:
            if position == 'start':
                chars.insert(0, inv)
            elif position == 'end':
                chars.append(inv)
            elif position == 'middle':
                mid = len(chars) // 2
                chars.insert(mid, inv)
            else:  # random
                idx = random.randint(0, len(chars))
                chars.insert(idx, inv)

        return ''.join(chars)

    def zwj_attack(self, text: str) -> str:
        """Insert zero-width joiner to create emoji-like sequences."""
        return self.ZWJ.join(text)

    def rtl_attack(self, text: str) -> str:
        """Wrap text in RTL override for visual spoofing."""
        return f"{self.RTL}{text}{self.POP}"

    def case_attack(self, text: str, mode: str = 'random') -> str:
        """Randomize case."""
        if mode == 'random':
            return ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in text)
        elif mode == 'alternate':
            return ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(text))
        elif mode == 'toggle':
            return ''.join(c.lower() if c.isupper() else c.upper() for c in text)
        return text

    def leet_attack(self, text: str, probability: float = 0.4) -> str:
        """Apply leet speak substitution."""
        return ''.join(
            self.LEET_MAP.get(c.lower(), c) if random.random() < probability else c
            for c in text
        )

    def glitch_attack(self, text: str, intensity: int = 3) -> str:
        """Apply combining diacritical marks."""
        combining = [chr(c) for c in range(0x0300, 0x036F)]
        result = []
        for char in text:
            result.append(char)
            marks = random.choices(combining, k=intensity)
            result.extend(marks)
        return ''.join(result)

    def normalize_attack(self, text: str, form: str = 'NFD') -> str:
        """Apply unicode normalization."""
        return unicodedata.normalize(form, text)

    def punycode_attack(self, text: str) -> str:
        """Convert to punycode representation."""
        try:
            return text.encode('idna').decode('ascii')
        except UnicodeError:
            return text

    def emoji_attack(self, text: str, density: float = 0.3) -> str:
        """Insert emoji between characters."""
        emojis = ['🦀', '👻', '🔥', '💀', '⚡', '🌈', '🎭', '👁️', '🧠', '💎']
        result = []
        for char in text:
            result.append(char)
            if random.random() < density:
                result.append(random.choice(emojis))
        return ''.join(result)


class ContentGenerator:
    """Generate synthetic user content with adversarial perturbations."""

    FIRST_NAMES = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra"
    ]

    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson"
    ]

    STREETS = [
        "Main St", "Oak Ave", "Maple Rd", "Cedar Ln", "Pine Dr", "Elm St", "Washington Ave",
        "Lake Shore Dr", "Park Ave", "Broadway", "5th Ave", "Sunset Blvd", "Rodeo Dr",
        "Beverly Dr", "Mission St", "Market St", "Peachtree St", "Michigan Ave", "Wall St"
    ]

    CITIES = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
        "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
        "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle"
    ]

    DESCRIPTION_TEMPLATES = [
        "Hi, I'm {first}. I love {hobby} and {activity}.",
        "Professional {job} based in {city}. Passionate about {topic}.",
        "Just a {adj} person trying to make it in {industry}.",
        "{first} here. {verb} enthusiast and {noun} collector.",
        "Living life in {city}. Working as {job}. Dreaming of {dream}.",
        "Not your average {noun}. I {verb} differently.",
        "{adj}, {adj2}, and ready to {verb}. Let's connect!",
        "Former {job} turned {job2}. Currently exploring {topic}."
    ]

    HOBBIES = ["coding", "gaming", "hiking", "cooking", "reading", "traveling", "photography", "music"]
    ACTIVITIES = ["building things", "solving problems", "helping others", "learning new skills"]
    JOBS = ["developer", "designer", "manager", "analyst", "engineer", "consultant", "artist"]
    TOPICS = ["AI", "blockchain", "sustainability", "education", "healthcare", "space"]
    ADJECTIVES = ["creative", "ambitious", "curious", "driven", "passionate", "weird"]
    VERBS = ["code", "create", "explore", "build", "design", "think"]
    NOUNS = ["human", "nerd", "dreamer", "maker", "thinker", "builder"]
    INDUSTRIES = ["tech", "finance", "healthcare", "education", "entertainment"]
    DREAMS = ["changing the world", "making a difference", "building the future", "finding peace"]

    def __init__(self, seed: Optional[int] = None):
        self.adv = AdversarialStringGenerator(seed)
        if seed:
            random.seed(seed)

    def generate_username(self, base: Optional[str] = None, 
                         attacks: List[AttackType] = None) -> str:
        """Generate adversarial username."""
        if base is None:
            base = f"{random.choice(self.FIRST_NAMES)}{random.randint(1,9999)}"

        if attacks is None:
            attacks = random.sample(list(AttackType), k=random.randint(1, 3))

        username = base
        for attack in attacks:
            if attack == AttackType.HOMOGLYPH:
                username = self.adv.homoglyph_attack(username, 0.4)
            elif attack == AttackType.INVISIBLE:
                username = self.adv.invisible_attack(username, 2)
            elif attack == AttackType.ZWJ:
                username = self.adv.zwj_attack(username)
            elif attack == AttackType.RTL:
                username = self.adv.rtl_attack(username)
            elif attack == AttackType.CASE:
                username = self.adv.case_attack(username, 'random')
            elif attack == AttackType.LEET:
                username = self.adv.leet_attack(username, 0.5)
            elif attack == AttackType.GLITCH:
                username = self.adv.glitch_attack(username, 2)
            elif attack == AttackType.PUNYCODE:
                username = self.adv.punycode_attack(username)
            elif attack == AttackType.EMOJI:
                username = self.adv.emoji_attack(username, 0.2)

        return username[:32]  # Truncate to reasonable length

    def generate_name(self, attacks: List[AttackType] = None) -> Tuple[str, str]:
        """Generate adversarial first and last name."""
        first = random.choice(self.FIRST_NAMES)
        last = random.choice(self.LAST_NAMES)

        if attacks:
            for attack in attacks:
                if attack == AttackType.HOMOGLYPH:
                    first = self.adv.homoglyph_attack(first, 0.3)
                    last = self.adv.homoglyph_attack(last, 0.3)
                elif attack == AttackType.INVISIBLE:
                    first = self.adv.invisible_attack(first, 1)
                    last = self.adv.invisible_attack(last, 1)
                elif attack == AttackType.GLITCH:
                    first = self.adv.glitch_attack(first, 1)
                    last = self.adv.glitch_attack(last, 1)

        return first, last

    def generate_address(self, attacks: List[AttackType] = None) -> str:
        """Generate adversarial address."""
        number = random.randint(1, 9999)
        street = random.choice(self.STREETS)
        city = random.choice(self.CITIES)
        state = "CA"  # Simplified
        zip_code = f"{random.randint(10000, 99999)}"

        address = f"{number} {street}, {city}, {state} {zip_code}"

        if attacks:
            for attack in attacks:
                if attack == AttackType.HOMOGLYPH:
                    address = self.adv.homoglyph_attack(address, 0.2)
                elif attack == AttackType.INVISIBLE:
                    address = self.adv.invisible_attack(address, 1, 'random')
                elif attack == AttackType.LEET:
                    address = self.adv.leet_attack(address, 0.3)

        return address

    def generate_description(self, first_name: str, city: str,
                           attacks: List[AttackType] = None) -> str:
        """Generate adversarial profile description."""
        template = random.choice(self.DESCRIPTION_TEMPLATES)

        description = template.format(
            first=first_name,
            city=city,
            hobby=random.choice(self.HOBBIES),
            activity=random.choice(self.ACTIVITIES),
            job=random.choice(self.JOBS),
            topic=random.choice(self.TOPICS),
            adj=random.choice(self.ADJECTIVES),
            adj2=random.choice(self.ADJECTIVES),
            verb=random.choice(self.VERBS),
            noun=random.choice(self.NOUNS),
            industry=random.choice(self.INDUSTRIES),
            dream=random.choice(self.DREAMS),
            job2=random.choice(self.JOBS),
            verb2=random.choice(self.VERBS)
        )

        if attacks:
            for attack in attacks:
                if attack == AttackType.HOMOGLYPH:
                    description = self.adv.homoglyph_attack(description, 0.2)
                elif attack == AttackType.INVISIBLE:
                    description = self.adv.invisible_attack(description, 3)
                elif attack == AttackType.EMOJI:
                    description = self.adv.emoji_attack(description, 0.1)
                elif attack == AttackType.GLITCH:
                    description = self.adv.glitch_attack(description, 1)

        return description

    def generate_profile_pic_prompt(self, description: str) -> str:
        """Generate prompt for profile picture generation."""
        styles = [
            "professional headshot", "casual outdoor photo", "artistic portrait",
            "minimalist avatar", "vibrant illustration", "monochrome sketch",
            "3D rendered character", "anime style", "vintage polaroid"
        ]

        adjectives = ["confident", "mysterious", "friendly", "serious", "creative"]

        prompt = f"{random.choice(styles)} of a {random.choice(adjectives)} person, "
        prompt += f"{random.choice(self.ADJECTIVES)} vibe, "
        prompt += f"background suggesting {random.choice(self.TOPICS)}, "
        prompt += "high quality, detailed"

        return prompt

    def generate_profile(self, attack_probability: float = 0.7) -> UserProfile:
        """Generate complete adversarial user profile."""
        # Decide which attacks to apply
        all_attacks = list(AttackType)
        num_attacks = random.randint(1, 4) if random.random() < attack_probability else 0
        selected_attacks = random.sample(all_attacks, k=num_attacks) if num_attacks > 0 else []

        # Generate base content
        first, last = self.generate_name(selected_attacks)
        city = random.choice(self.CITIES)

        profile = UserProfile(
            username=self.generate_username(None, selected_attacks),
            first_name=first,
            last_name=last,
            address=self.generate_address(selected_attacks),
            description=self.generate_description(first, city, selected_attacks),
            profile_pic_prompt=self.generate_profile_pic_prompt(""),
            attack_vectors=selected_attacks,
            raw_bytes=b''  # Will be populated
        )

        # Generate raw bytes representation
        profile.raw_bytes = json.dumps(profile.to_dict()).encode('utf-8')

        return profile


if __name__ == "__main__":
    # Demo usage
    gen = ContentGenerator(seed=13)

    print("🦀 Adversarial ML Content Generator Demo 🦀\n")

    for i in range(5):
        profile = gen.generate_profile()
        print(f"--- Profile {i+1} ---")
        print(f"Username: {profile.username}")
        print(f"Name: {profile.first_name} {profile.last_name}")
        print(f"Address: {profile.address}")
        print(f"Description: {profile.description[:80]}...")
        print(f"Attacks: {[a.value for a in profile.attack_vectors]}")
        print()
